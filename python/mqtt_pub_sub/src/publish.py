import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import random
from config import settings
from log import logger
import time
from utils import on_connect, on_disconnect, on_log

client_id = f'lucas-python-mqtt-pub-{random.randint(0, 100)}'


def setup_listeners(client: Client):
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_disconnect = on_disconnect


def connect() -> Client:
    client = mqtt.Client(client_id=client_id)

    setup_listeners(client)

    client.connect(
        host=settings.HOST,
        port=settings.PORT,
        keepalive=60)

    return client


def publish(client: Client):
    msg_count = 0
    topic = settings.TOPIC

    while True:
        time.sleep(3)
        msg = f'Publishing message {msg_count}'
        result = client.publish(topic, msg)

        status = result[0]
        if status == 0:
            logger.info(f'Published message: {msg} to topic {topic}')
        else:
            logger.error(f'Failed to publish message to topic {topic}')
        msg_count += 1


def run():
    client = connect()
    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()
