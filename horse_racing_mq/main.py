import json
import logging
import logging.config
import os
import subprocess

import pika

logging.config.fileConfig("logging.ini")
L = logging.getLogger("horse_racing.mq")


def mq_callback(ch, method, properties, body):
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
        result = subprocess.run(["scrapy", "crawl", "netkeiba_spider", "-a", f"start_url={start_url}"], env=new_env)
        L.debug(f"クロール結果コード: {result.returncode=}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    mq_credentials = pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASS"])

    mq_parameters = pika.ConnectionParameters(os.environ["RABBITMQ_HOST"], os.environ["RABBITMQ_PORT"], "/", mq_credentials)

    mq_connection = None
    try:
        mq_connection = pika.BlockingConnection(mq_parameters)
        mq_channel = mq_connection.channel()

        mq_channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"], durable=True)

        mq_channel.basic_qos(prefetch_count=1)

        mq_channel.basic_consume(queue=os.environ["RABBITMQ_QUEUE"], on_message_callback=mq_callback)

        L.info("waiing for messages")
        mq_channel.start_consuming()

    finally:
        mq_connection.close()
