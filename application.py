from PyQt5 import QtWidgets
import sys
from screens import MainScreen, LoginScreen, RegisterScreen, FaceRegisterScreen


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FaceLock')
        self.setGeometry(500, 500, 500, 500)

        self.stacked_widget = QtWidgets.QStackedWidget()

        self.main_screen = MainScreen(self.switch_to_login_screen, self.switch_to_register_screen)
        self.login_screen = LoginScreen(self.switch_to_main_screen)
        self.register_screen = RegisterScreen(self.switch_to_main_screen, self.switch_to_face_registration_screen)
        self.face_registration_screen = FaceRegisterScreen(self.switch_to_main_screen)

        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.face_registration_screen)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def switch_to_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def switch_to_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_register_screen(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def switch_to_face_registration_screen(self):
        self.stacked_widget.setCurrentWidget(self.face_registration_screen)


def main():
    app = QtWidgets.QApplication(sys.argv)
    face_auth_app = App()
    face_auth_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()