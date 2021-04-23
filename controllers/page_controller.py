from pages import MainWindow, Login
from PyQt5 import QtWidgets


class PageController:

    # Page indices
    login_index = 0
    main_window_index = 1

    def __init__(self):
        width = 800
        height = 600

        self.application_window = QtWidgets.QStackedWidget()
        self.application_window.resize(width, height)
        self.application_window.setWindowTitle("Login")
        # Pages
        login = Login()
        main_window = MainWindow()
        # Add widgets
        self.application_window.addWidget(login)
        self.application_window.addWidget(main_window)
        # Events handler
        login.login_switch.connect(self.switch_to_main)
        main_window.logout_switch.connect(self.switch_to_login)

        self.application_window.show()

    def switch_to_main(self):
        self.application_window.setWindowTitle("Welcome to Decentorage")
        self.application_window.setCurrentIndex(self.main_window_index)

    def switch_to_login(self):
        self.application_window.setWindowTitle("Login")
        self.application_window.setCurrentIndex(self.login_index)
