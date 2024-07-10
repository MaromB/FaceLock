import time
from io import BytesIO

import cv2
import face_recognition
from PyQt5 import QtGui, QtMultimedia, QtCore
import firebase_DB


def apply_zoom(frame, zoom_fact):
    h, w, _ = frame.shape
    centerX, centerY = w // 2, h // 2
    newW, newH = int(w/zoom_fact), int(h/zoom_fact)

    x1, y1 = centerX - newW // 2, centerY - newH // 2
    x2, y2 = centerX + newW // 2, centerY + newH // 2
    cropped_frame = frame[y1:y2, x1:x2]
    return cropped_frame


class imageCapture:
    def __init__(self, image, screen, app, db=None):
        self.face_encodings = None
        self.frame = None
        self.cap = cv2.VideoCapture(0)
        self.image = image
        self.screen = screen
        self.app = app
        self.count = 10
        self.timer = time.time() + 3
        self.player = QtMultimedia.QMediaPlayer()
        self.db = db
        self.images = []

    def update_frame_registration(self):
        zoom_fact = 1.6
        ret, self.frame = self.cap.read()
        if ret:
            self.frame = apply_zoom(self.frame, zoom_fact)
            self.frame = cv2.resize(self.frame, (480, 360))
            # Convert the frame to RGB format
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to QImage format
            image = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0],
                                 QtGui.QImage.Format_RGB888)
            # Set the QImage to the QLabel
            timer = self.timer - time.time()
            timer_seconds = "{:.0f}".format(timer)
            self.screen.update_labels(self.count, timer_seconds)
            self.image.setPixmap(QtGui.QPixmap.fromImage(image))
            if timer <= 0:
                self.images.append(self.frame)
                self.play_sound('C:/Users/Administrator/Downloads/FaceLock/sound_of_capture_camera.wma')
                self.update_time()
            if self.count == 0:
                self.db.save_images_in_db(self.images)
                self.app.reset_app()

    def update_time(self):
        self.timer = time.time() + 3
        self.count -= 1

    def play_sound(self, sound_file):
        url = QtCore.QUrl.fromLocalFile(sound_file)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def release_capture(self):
        self.cap.release()

    def update_frame_login(self):
        zoom_fact = 1.6
        ret, self.frame = self.cap.read()
        if ret:
            self.frame = apply_zoom(self.frame, zoom_fact)
            self.frame = cv2.resize(self.frame, (480, 360))
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

            image = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0],
                                 QtGui.QImage.Format_RGB888)
            self.image.setPixmap(QtGui.QPixmap.fromImage(image))

            self.face_encodings = firebase_DB.get_encoded_face(self.frame)

    def login_into_system(self, username):
        list_of_faces = firebase_DB.taking_faces_from_db(username)
        list_of_answers = face_recognition.api.compare_faces(list_of_faces, self.face_encodings, tolerance=0.6)
        return any(list_of_answers)

