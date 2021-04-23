from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):

    # Signals
    logout_switch = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Window')
        layout = QtWidgets.QGridLayout()

        # Logout button
        self.logout_button = QtWidgets.QPushButton('Logout')
        self.logout_button.clicked.connect(self.logout)

        # Add widgets
        layout.addWidget(self.logout_button)

        # Set layout
        self.setLayout(layout)

    def logout(self):
        self.logout_switch.emit()
