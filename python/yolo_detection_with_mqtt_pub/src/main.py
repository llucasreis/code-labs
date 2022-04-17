import time
from services.mqtt.mqtt import Mqtt
from services.model.yolo import Yolo
import os

host = "broker.emqx.io"
port = 1883
topic = "lucas/mqtt/test"


def run():
    image_path = os.path.join(os.path.dirname(
        __file__), 'data', 'images', 'test_4.jpg')
    mqtt = Mqtt()

    mqtt.client.connect(
        host=host,
        port=port,
        keepalive=60,
    )

    mqtt.client.loop_start()

    time.sleep(2)

    yolo = Yolo()

    predicted_labels = yolo.predict_labels(image_path)

    danger_situtation = 'adult' not in predicted_labels

    if danger_situtation:
        print("Danger")
        mqtt.publish(topic, 'danger')

    mqtt.client.loop_stop()


if __name__ == "__main__":
    run()
