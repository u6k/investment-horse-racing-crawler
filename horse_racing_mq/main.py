import json
import logging
import logging.config
import os
import subprocess
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

    def start(self):
        mq_credentials = pika.PlainCredentials(self._mq_user, self._mq_pass)
        mq_parameters = pika.ConnectionParameters(self._mq_host, self._mq_port, "/", mq_credentials, heartbeat=10)

        try:
            while True:
                try:
                    self._connection = pika.BlockingConnection(mq_parameters)
                    break
                except pika.exceptions.AMQPConnectionError:
                    L.debug("connection fail. retry...")
                    time.sleep(1)

            mq_channel = self._connection.channel()

            mq_channel.queue_declare(queue=self._mq_queue, durable=True)

            mq_channel.basic_qos(prefetch_count=1)

            mq_channel.basic_consume(queue=self._mq_queue, on_message_callback=self.process)

            L.info("waiting for messages")
            mq_channel.start_consuming()

        finally:
            self._connection.close()

    def process(self, ch, method, properties, body):
        try:
            msg = json.loads(body.decode())
            L.info(f"callback start: {msg}")

            # 開始URLを取得する
            start_url = msg["start_url"]

            # 環境変数を取得する
            new_env = os.environ.copy()
            for k, v in msg.items():
                new_env[k] = v

            L.debug(f"クロール開始: {start_url=}")
            with subprocess.Popen(["scrapy", "crawl", "netkeiba_spider", "-a", f"start_url={start_url}"], env=new_env) as proc:
                while True:
                    return_code = proc.poll()
                    if return_code is not None:
                        break
                    time.sleep(1)
            L.debug(f"クロール結果コード: {return_code=}")
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)


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
