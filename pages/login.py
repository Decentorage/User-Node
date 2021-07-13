from PyQt5 import QtWidgets
from controllers.worker import call_worker
from utils import user_login


class Login(QtWidgets.QWidget):

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
        self.ui.login_pb.clicked.connect(lambda: call_worker(self.login, ui, ui.main_page, "Logging in.."))

    def login(self):
        username = self.ui.login_username_line_edit.text()
        password = self.ui.login_password_line_edit.text()
        if username == '' or password == '':
            raise Exception('please fill username and password fields.')
        else:
            user_login(username, password)
        self.settings.get_token()
