import os
from typing import List
import cv2
import numpy as np


class Yolo:
    def __init__(self) -> None:
        config_path = os.path.join(os.path.dirname(
            __file__), 'resources', 'yolov4-tiny_custom.cfg')
        weights_path = os.path.join(os.path.dirname(
            __file__), 'resources', 'yolov4-tiny_custom_4000.weights')
        labels_path = os.path.join(os.path.dirname(
            __file__), 'resources', 'obj.names')

        self.model = cv2.dnn.readNetFromDarknet(config_path, weights_path)

        self.labels = open(labels_path).read().strip().split("\n")

        np.random.seed(42)
        self.colors = np.random.randint(
            0, 255, size=(len(self.labels), 3), dtype="uint8")

        self.default_confidence = 0.5
        self.default_threshold = 0.3

    def predict_labels(self, image_path: str) -> List[str]:
        image = cv2.imread(image_path)

        (H, W) = image.shape[:2]

        ln = self.model.getLayerNames()
        ln = [ln[i - 1] for i in self.model.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(
            image, 1/255.0, (406, 406), swapRB=True, crop=False)

        self.model.setInput(blob)
        layerOutputs = self.model.forward(ln)

        boxes, confidences, classIds = [], [], []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.default_confidence:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (center_x, center_y, width, height) = box.astype("int")

                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIds.append(classID)

        idxs = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            self.default_confidence,
            self.default_threshold)

        predicted_labels = []

        if len(idxs) > 0:
            predicted_labels = [self.labels[classIds[i]]
                                for i in idxs.flatten()]

        return predicted_labels
