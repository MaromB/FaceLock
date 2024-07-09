import time
import cv2
import face_recognition
from PyQt5 import QtGui
from firebase_DB import db


def apply_zoom(frame, zoom_fact):
    h, w, _ = frame.shape
    centerX, centerY = w // 2, h // 2
    newW, newH = int(w/zoom_fact), int(h/zoom_fact)

    x1, y1 = centerX - newW // 2, centerY - newH // 2
    x2, y2 = centerX + newW // 2, centerY + newH // 2
    cropped_frame = frame[y1:y2, x1:x2]
    return cropped_frame


class imageCapture:
    def __init__(self, image, face_register_screen, app):
        self.db = db
        self.cap = cv2.VideoCapture(0)
        self.image = image
        self.face_register_screen = face_register_screen
        self.app = app
        self.count = 11
        self.timer = 8

    def update_frame(self):
        zoom_fact = 1.6
        ret, frame = self.cap.read()
        if ret:
            frame = apply_zoom(frame, zoom_fact)
            frame = cv2.resize(frame, (480, 360))
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to QImage format
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            # Set the QImage to the QLabel
            timer = self.timer - time.time()
            timer_seconds = "{:.0f}".format(timer)
            self.face_register_screen.update_labels(self.count, timer_seconds)
            self.image.setPixmap(QtGui.QPixmap.fromImage(image))
            if timer <= 0:
                self.update_time()
            if self.count == 0:
                self.app.reset_app()

    def update_time(self):
        self.timer = time.time() + 10
        self.count -= 1

    def release_capture(self):
        self.cap.release()


