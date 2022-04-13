import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import random
from config import settings
from log import logger
from utils import on_connect, on_disconnect, on_log


client_id = f'lucas-python-mqtt-sub-{random.randint(0, 100)}'


def on_message(client, userdata, msg):
    logger.info(
        f"Received message: {msg.payload.decode()} from topic: {msg.topic}")


def setup_listeners(client: Client):
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.on_message = on_message


def connect() -> Client:
    client = mqtt.Client(client_id=client_id)

    setup_listeners(client)

    client.connect(
        host=settings.HOST,
        port=settings.PORT,
        keepalive=60)

    return client


def subscribe(client: Client):
    client.subscribe(settings.TOPIC)


def run():
    client = connect()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()
