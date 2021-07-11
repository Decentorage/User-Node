from PyQt5 import QtCore, QtWidgets
from controllers.worker import call_worker
import time


class Login(QtWidgets.QWidget):

    login_switch = QtCore.pyqtSignal()

    def __init__(self, ui):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')
        ui.login_pb.clicked.connect(lambda: call_worker(self.login, ui, ui.main_page, "Logging in.."))

    def login(self):
        time.sleep(10)
        # print("HII")
        # self.login_switch.emit()
