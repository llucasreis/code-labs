import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import random
from config.log import logger


class Mqtt:
    def __init__(self) -> None:
        client_id = f'lucas-python-mqtt-sub-{random.randint(0, 100)}'

        self.client = mqtt.Client(client_id=client_id)

        self.client.on_connect = self.__on_connect__
        self.client.on_log = self.__on_log__
        self.client.on_disconnect = self.__on_disconnect__

    def __on_connect__(self, client, userdata, flags, rc) -> None:
        if rc == 0:
            logger.info("Connected to MQTT Broker")
        else:
            logger.error("Failed to connect, return code: %d\n", rc)

    def __on_log__(self, client, userdata, level, buf) -> None:
        logger.debug(buf)

    def __on_disconnect__(self, client, userdata, rc):
        logger.info("Client disconnected, return code: %d\n", rc)

    def publish(self, topic: str, message: str) -> None:
        result = self.client.publish(topic, message)

        status = result[0]

        if status == 0:
            logger.info(f'Published message: {message} to topic {topic}')
        else:
            logger.error(f'Failed to publish message to topic {topic}')
