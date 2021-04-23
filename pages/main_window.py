from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):

    # Signals
    logout_switch = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Window')
        layout = QtWidgets.QGridLayout()

        # Add Page widgets
        self.download_button = QtWidgets.QPushButton("Download")
        self.browse_button = QtWidgets.QPushButton("Browse File")
        self.upload_button = QtWidgets.QPushButton("Upload")
        self.logout_button = QtWidgets.QPushButton('Logout')
        self.label_1 = QtWidgets.QLabel("Stored files:")
        self.label_2 = QtWidgets.QLabel("Stored files:")
        self.label_3 = QtWidgets.QLabel("Encryption Key:")
        self.file_selected_label = QtWidgets.QLabel()
        self.file_selected_label.setText("")
        self.key_editor = QtWidgets.QLineEdit()
        self.stored_files = QtWidgets.QListView()
        # Buttons function
        self.logout_button.clicked.connect(self.logout)
        self.upload_button.clicked.connect(self.upload)
        self.download_button.clicked.connect(self.download)
        self.browse_button.clicked.connect(self.browse)
        # Add widgets
        layout.addWidget(self.logout_button, 6, 0)
        layout.addWidget(self.download_button, 1, 1)
        layout.addWidget(self.browse_button, 3, 1)
        layout.addWidget(self.upload_button, 5, 1)
        layout.addWidget(self.file_selected_label, 3, 0)
        layout.addWidget(self.label_1, 2, 0)
        layout.addWidget(self.label_2, 0, 0)
        layout.addWidget(self.label_3, 4, 0)
        layout.addWidget(self.key_editor, 5, 0)
        layout.addWidget(self.stored_files, 1, 0)

        # Set layout
        self.setLayout(layout)

    def logout(self):
        self.logout_switch.emit()

    def start_processing(self):
        pass

    def retrieve_file(self):
        pass
