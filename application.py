from PyQt5 import QtWidgets
import sys
from screens import MainScreen, LoginScreen, RegisterScreen, FaceRegisterScreen


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FaceLock')
        self.setGeometry(500, 500, 500, 500)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.create_screens()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def create_screens(self):

        self.main_screen = MainScreen(self)
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.face_registration_screen = FaceRegisterScreen(self)

        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.face_registration_screen)

    def reset_app(self):
        self.stacked_widget.removeWidget(self.main_screen)
        # self.stacked_widget.removeWidget(self.login_screen)
        self.stacked_widget.removeWidget(self.register_screen)
        self.stacked_widget.removeWidget(self.face_registration_screen)

        self.main_screen.deleteLater()
        # self.login_screen.cleanup()
        self.register_screen.deleteLater()
        self.face_registration_screen.cleanup()

        self.create_screens()
        self.switch_to_main_screen()

    def switch_to_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def switch_to_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)
        # self.login_screen.start_login_capture()

    def switch_to_register_screen(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def switch_to_face_registration_screen(self, register_screen):
        self.stacked_widget.setCurrentWidget(self.face_registration_screen)
        self.face_registration_screen.start_face_registration(register_screen)

    def closeEvent(self, event):
        try:
            # Ensure proper cleanup when closing the application
            if hasattr(self, 'face_registration_screen'):
                self.face_registration_screen.timer.stop()
                self.face_registration_screen.image_cap.cleanup()
        except Exception as e:
            print(f"Exception during closeEvent: {e}")
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    face_auth_app = App()
    face_auth_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()