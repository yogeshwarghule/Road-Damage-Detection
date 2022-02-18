import cv2
import numpy as np
import time

class Model:
    def __init__(self):
        self.net = cv2.dnn.readNet("Model/model_4_7.weights", "Model/yolo_608.cfg")
        # congigure cuda driver
        self.classes = []
        with open("Model/obj.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = self.net.getUnconnectedOutLayersNames()
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        # Loading camera
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.starting_time = time.time()
        self.frame_id = 0

    def getPrediction(self, frame):
        self.frame_id = self.frame_id + 1
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.05:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        label = str(self.classes[class_ids[i]])
                        confidence = confidences[i]
                        color = self.colors[class_ids[i]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                        cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), self.font, 3,(255, 255, 255), 3)
                        elapsed_time = time.time() - self.starting_time
                        fps = self.frame_id / elapsed_time
                        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), self.font, 3, (0, 0, 0), 3)
        damages = []
        for x in class_ids:
            damages.append(self.classes[x])
        return frame, damages, confidences
