from PyQt5.QtCore import QThreadPool

from pages import MainWindow, Login
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow


class PageController:

    # Page indices
    login_index = 0
    main_window_index = 1

    def __init__(self):

        self.application_window = QtWidgets.QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.application_window)
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
        self.ui.thread_pool = QThreadPool()
        self.ui.waiting_spinner.start()
        # Pages
        self.login = Login(self.ui)
        # Add widgets
        # Events handler
        # self.login.login_switch.connect(self.switch_to_main)
        # self.main_window.logout_switch.connect(self.switch_to_login)

        self.application_window.show()

    def switch_to_main(self):
        self.application_window.setWindowTitle("Welcome to Decentorage")
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    def switch_to_login(self):
        self.application_window.setWindowTitle("Login")
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
