from PyQt5 import QtWidgets, QtCore
from imageCapture import imageCapture
import firebase_DB


class MainScreen(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self.login_button = None
        self.register_button = None
        self.username_input = None
        self.username_label = None
        self.setWindowTitle('FaceLock')
        self.setGeometry(300, 300, 300, 200)
        layout1 = QtWidgets.QVBoxLayout(self)
        layout2 = QtWidgets.QHBoxLayout()
        self.app = app

        self.login_button = QtWidgets.QPushButton('Sign in', self)
        self.login_button.clicked.connect(self.app.switch_to_login_screen)
        layout2.addWidget(self.login_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom |
                          QtCore.Qt.AlignLeft)

        self.register_button = QtWidgets.QPushButton('Sign out', self)
        self.register_button.clicked.connect(self.app.switch_to_register_screen)
        layout2.addWidget(self.register_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom |
                          QtCore.Qt.AlignRight)

        layout1.addLayout(layout2)
        layout1.setAlignment(layout2, QtCore.Qt.AlignCenter)


class FaceRegisterScreen(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self.register_screen = None
        self.image_cap = None
        layout = QtWidgets.QVBoxLayout()
        label_layout = QtWidgets.QHBoxLayout()
        self.app = app

        self.main_label = QtWidgets.QLabel('Face Registration \nPlease look at the camera and tilt your head to let '
                                           'the system recognize your facial features', self)
        label_layout.addWidget(self.main_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        layout.addLayout(label_layout)

        self.image = QtWidgets.QLabel(self)
        self.image.resize(480, 360)
        self.image.frameSize()
        layout.addWidget(self.image, alignment=QtCore.Qt.AlignCenter)

        self.images_label = QtWidgets.QLabel('', self)
        layout.addWidget(self.images_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.back_button = QtWidgets.QPushButton("Go to Main Screen")
        self.back_button.clicked.connect(self.app.switch_to_main_screen)
        layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        layout.addLayout(label_layout)
        self.setLayout(layout)

    def update_labels(self, count, timer):
        self.images_label.setText(f'Number of images required:  {count}  Timer: {timer}  \n')

    def timer_start(self, event):
        self.image_cap.update_time()

    def start_face_registration(self, register_screen):
        self.register_screen = register_screen
        self.image_cap = imageCapture(self.app, None, self, self.register_screen)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.image_cap.update_frame_registration)
        self.showEvent = self.timer_start
        self.show()
        self.timer.start(30)

    def cleanup(self):
        self.timer.stop()
        self.image_cap.release_capture()


class RegisterScreen(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self.db = None
        self.app = app
        layout = QtWidgets.QVBoxLayout()

        # spacer = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # layout.addSpacerItem(spacer)

        username_layout = QtWidgets.QHBoxLayout()
        self.username_label = QtWidgets.QLabel('Username:', self)
        self.username_input = QtWidgets.QLineEdit(self)
        username_layout.addWidget(self.username_label, alignment=QtCore.Qt.AlignLeft)
        username_layout.addWidget(self.username_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(username_layout)

        password_layout = QtWidgets.QHBoxLayout()
        self.password_label = QtWidgets.QLabel('Password:', self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setText('123123Rr!')
        password_layout.addWidget(self.password_label, alignment=QtCore.Qt.AlignLeft)
        password_layout.addWidget(self.password_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(password_layout)

        password_validation_layout = QtWidgets.QHBoxLayout()
        self.password_validation_label = QtWidgets.QLabel('Password again:', self)
        self.password_validation_input = QtWidgets.QLineEdit(self)
        self.password_validation_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_validation_input.setText('123123Rr!')
        password_validation_layout.addWidget(self.password_validation_label, alignment=QtCore.Qt.AlignLeft)
        password_validation_layout.addWidget(self.password_validation_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(password_validation_layout)

        Fname_layout = QtWidgets.QHBoxLayout()
        self.Fname_label = QtWidgets.QLabel('First name:', self)
        self.Fname_input = QtWidgets.QLineEdit(self)
        Fname_layout.addWidget(self.Fname_label, alignment=QtCore.Qt.AlignLeft)
        Fname_layout.addWidget(self.Fname_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(Fname_layout)

        Lname_layout = QtWidgets.QHBoxLayout()
        self.Lname_label = QtWidgets.QLabel('Last name:', self)
        self.Lname_input = QtWidgets.QLineEdit(self)
        Lname_layout.addWidget(self.Lname_label, alignment=QtCore.Qt.AlignLeft)
        Lname_layout.addWidget(self.Lname_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(Lname_layout)

        Email_layout = QtWidgets.QHBoxLayout()
        self.Email_label = QtWidgets.QLabel('Email:', self)
        self.Email_input = QtWidgets.QLineEdit(self)
        Email_layout.addWidget(self.Email_label, alignment=QtCore.Qt.AlignLeft)
        Email_layout.addWidget(self.Email_input, alignment=QtCore.Qt.AlignLeft)
        layout.addLayout(Email_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.Next_button = QtWidgets.QPushButton("Next")
        self.Next_button.clicked.connect(self.password_verification_check)
        button_layout.addWidget(self.Next_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft |
                                QtCore.Qt.AlignBottom)

        self.back_button = QtWidgets.QPushButton("Go to Main Screen")
        self.back_button.clicked.connect(self.app.switch_to_main_screen)
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight |
                                QtCore.Qt.AlignBottom)

        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def password_verification_check(self):
        password = self.password_input.text()
        password_validation = self.password_validation_input.text()
        special_characters = "!@#$%^&*()+=-/?><"

        if password != password_validation:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if len(password) <= 8:
            QtWidgets.QMessageBox.warning(self, "Error", "Password must be longer than 8 characters.")
            return

        if not any(char.islower() for char in password):
            QtWidgets.QMessageBox.warning(self, "Error", "Password must contain at least one lowercase character.")
            return

        if not any(char.isupper() for char in password):
            QtWidgets.QMessageBox.warning(self, "Error", "Password must contain at least one uppercase character.")
            return

        if not any(char in special_characters for char in password):
            QtWidgets.QMessageBox.warning(self, "Error",
                                          "Password must contain at least one special character (!@#$%^&*+=-/?><).")
            return
        self.db = firebase_DB.Database(self.username_input.text(), password, self.Fname_input.text(),
                                       self.Lname_input.text(), self.Email_input.text())
        success, message = self.db.register_user()

        if not success:
            QtWidgets.QMessageBox.warning(self, "Error", message)
        else:
            self.app.switch_to_face_registration_screen(self)


class LoginScreen(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self.db = None
        self.image_cap = QtWidgets
        layout = QtWidgets.QVBoxLayout()
        self.app = app
        username_layout = QtWidgets.QHBoxLayout()
        self.username_label = QtWidgets.QLabel('Username:', self)
        username_layout.addWidget(self.username_label, alignment=QtCore.Qt.AlignLeft)
        self.username_input = QtWidgets.QLineEdit(self)
        username_layout.addWidget(self.username_input, alignment=QtCore.Qt.AlignLeft)

        spacer = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addSpacerItem(spacer)
        layout.addLayout(username_layout)

        self.image = QtWidgets.QLabel(self)
        self.image.resize(480, 360)
        self.image.frameSize()
        layout.addWidget(self.image, alignment=QtCore.Qt.AlignCenter)
        self.image_cap = imageCapture(self.app, self, None, None)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.image_cap.update_frame_login)
        self.timer.start(30)

        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Login")
        answer = self.login_button.clicked.connect(lambda: self.handle_login())
        button_layout.addWidget(self.login_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft |
                                QtCore.Qt.AlignBottom)
        print(answer)
        
        self.back_button = QtWidgets.QPushButton("Go to Main Screen")
        self.back_button.clicked.connect(self.app.switch_to_main_screen)
        button_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight |
                                QtCore.Qt.AlignBottom)

        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_authenticate_clicked(self):
        self.image_capture_instance.authenticate_user()

    def start_login_capture(self):
        self.image_cap = imageCapture(self.app, self, None, None)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.image_cap.update_frame_login)
        self.timer.start(30)
    
    def handle_login(self):
        self.db = firebase_DB.Database(self.username_input.text(), None, None, None, None)
        self.db.login_into_system(self.image_cap.frame)
        

