from PyQt5 import QtCore, QtWidgets


class Login(QtWidgets.QWidget):

    login_switch = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        # Login button
        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        # Add components to layout
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        self.login_switch.emit()
