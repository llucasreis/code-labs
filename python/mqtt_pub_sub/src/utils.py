from log import logger


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker")
    else:
        logger.error("Failed to connect, return code: %d\n", rc)


def on_log(client, userdata, level, buf):
    logger.debug(buf)


def on_disconnect(client, userdata, rc):
    logger.info("Client disconnected, return code: %d\n", rc)
