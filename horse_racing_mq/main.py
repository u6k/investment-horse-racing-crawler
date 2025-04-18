import json
import logging
import logging.config
import os
import subprocess
import threading
import time

import pika

logging.config.fileConfig("logging.ini")
L = logging.getLogger("horse_racing.mq")


class MQTriggeredCrawler:
    def __init__(self, mq_host, mq_port, mq_user, mq_pass, mq_queue):
        self._mq_host = mq_host
        self._mq_port = mq_port
        self._mq_user = mq_user
        self._mq_pass = mq_pass
        self._mq_queue = mq_queue

        self._connection = None
        self._channel = None

        self._lock_channel = threading.Lock()

    def start(self):
        mq_credentials = pika.PlainCredentials(self._mq_user, self._mq_pass)
        mq_parameters = pika.ConnectionParameters(self._mq_host, self._mq_port, "/", mq_credentials, heartbeat=60)

        self._connection = pika.SelectConnection(mq_parameters, on_open_callback=self.on_connected, on_close_callback=self.on_disconnected)
        self._connection.ioloop.start()

    def on_connected(self, conn):
        L.info("on_connected")

        self._connection.channel(on_open_callback=self.on_channel_opened)

    def on_disconnected(self, conn, reason):
        L.info(f"on_disconnected: {reason=}")

        self._connection.ioloop.stop()
        self.start()

    def on_channel_opened(self, ch):
        L.info("on_channel_opened")

        with self._lock_channel:
            self._channel = ch
            self._channel.add_on_close_callback(callback=self.on_channel_closed)
            self._channel.queue_declare(queue=self._mq_queue, durable=True, callback=self.on_queue_declared)

    def on_channel_closed(self, ch, reason):
        L.warning(f"on_channel_closed: {reason=}")

        self._connection.ioloop.stop()
        self.start()

    def on_queue_declared(self, frame):
        L.info("on_queue_declared")

        with self._lock_channel:
            self._channel.basic_qos(prefetch_count=1, callback=self.on_qos_set)

    def on_qos_set(self, frame):
        L.info("on_qos_set")

        with self._lock_channel:
            self._channel.basic_consume(queue=self._mq_queue, on_message_callback=self.process)

        L.debug("waiting message")

    def process(self, ch, method, properties, body):
        L.info(f"process: {method=}, {body=}")

        # 開始URLを取得する
        msg = json.loads(body.decode())
        start_url = msg["start_url"]

        # 環境変数を取得する
        crawl_env = os.environ.copy()
        for k, v in msg.items():
            crawl_env[k] = v

        # クロール用のスレッドを開始する
        th = threading.Thread(target=self.crawl, args=(start_url, crawl_env, method))
        th.start()

    def crawl(self, start_url, crawl_env, mq_method):
        L.debug(f"crawl start: {start_url=}")
        try:
            # クロール用プロセスを開始する
            result = subprocess.run(["scrapy", "crawl", "netkeiba_spider", "-a", f"start_url={start_url}"], env=crawl_env)
            L.debug(f"crawl finish: {result.returncode=}")
        finally:
            # MQにACKを返す
            while True:
                with self._lock_channel:
                    if self._channel.is_open:
                        self._channel.basic_ack(delivery_tag=mq_method.delivery_tag)
                        L.debug("basic_ack")
                        break

                L.debug("channel not opening. sleep...")
                time.sleep(1)


if __name__ == "__main__":
    mq_host = os.environ["RABBITMQ_HOST"]
    mq_port = int(os.environ["RABBITMQ_PORT"])
    mq_user = os.environ["RABBITMQ_USER"]
    mq_pass = os.environ["RABBITMQ_PASS"]
    mq_queue = os.environ["RABBITMQ_QUEUE"]

    L.info(f"{mq_host=}")
    L.info(f"{mq_port=}")
    L.info(f"{mq_user=}")
    L.info(f"{mq_queue=}")

    crawler = MQTriggeredCrawler(mq_host, mq_port, mq_user, mq_pass, mq_queue)
    crawler.start()
