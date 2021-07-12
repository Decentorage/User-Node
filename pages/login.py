from PyQt5 import QtCore, QtWidgets
from controllers.worker import call_worker
from utils import client_login
import time


class Login(QtWidgets.QWidget):

    login_switch = QtCore.pyqtSignal()

    def __init__(self, ui):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')
        self.ui = ui
        self.ui.login_pb.clicked.connect(lambda: call_worker(self.login, ui, ui.main_page, "Logging in.."))

    def login(self):
        # time.sleep(10)
        username = self.ui.login_username_line_edit.text()
        password = self.ui.login_password_line_edit.text()
        if username == '' or password == '':
            raise Exception('please fill username and password fields.')
        else:
            client_login(username, password)
        self.login_switch.emit()
