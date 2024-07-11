import time
import cv2
from PyQt5 import QtGui, QtMultimedia, QtCore, QtWidgets
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
    def __init__(self, app, login_screen=None, face_register_screen=None, register_screen=None):
        self.face_encodings = None
        self.frame = None
        self.cap = cv2.VideoCapture(0)
        self.face_register_screen = face_register_screen
        self.register_screen = register_screen
        self.app = app
        self.login_screen = login_screen
        self.count = 10
        self.timer = time.time() + 3
        self.player = QtMultimedia.QMediaPlayer()
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
            self.face_register_screen.update_labels(self.count, timer_seconds)
            image_face_screen = self.face_register_screen.image
            image_face_screen.setPixmap(QtGui.QPixmap.fromImage(image))
            if timer <= 0:
                self.images.append(self.frame)
                self.play_sound('C:/Users/Administrator/Downloads/FaceLock/sound_of_capture_camera.wma')
                self.update_time()
                firebase_DB.embeddings_vector(self.frame, self.register_screen.username_input.text())
            if self.count == 0:
                db = self.register_screen.db
                db.save_images_in_db(self.images)
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
            image_login_screen = self.login_screen.image
            image_login_screen.setPixmap(QtGui.QPixmap.fromImage(image))

