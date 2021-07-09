from PyQt5 import QtCore, QtWidgets
import os
from utils import process_file, divide_file_and_process, retrieve_original_file
from psutil import virtual_memory


class MainWindow(QtWidgets.QWidget):
    # Signals
    logout_switch = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Window')
        layout = QtWidgets.QGridLayout()
        self.filename = None

        # Add Page widgets
        self.download_button = QtWidgets.QPushButton("Download")
        self.browse_button = QtWidgets.QPushButton("Browse File")
        self.upload_button = QtWidgets.QPushButton("Upload")
        self.logout_button = QtWidgets.QPushButton('Logout')
        self.label_1 = QtWidgets.QLabel("Stored files:")
        self.label_2 = QtWidgets.QLabel("Stored files:")
        self.label_3 = QtWidgets.QLabel("Encryption Key:")
        self.file_selected_label = QtWidgets.QLabel("")
        self.status = QtWidgets.QLabel("")
        self.key_editor = QtWidgets.QLineEdit()
        self.stored_files = QtWidgets.QListView()

        # Buttons function
        self.logout_button.clicked.connect(self.logout)
        self.upload_button.clicked.connect(self.upload)
        self.download_button.clicked.connect(self.download)
        self.browse_button.clicked.connect(self.browse)

        # Add widgets
        layout.addWidget(self.label_2, 0, 0)
        layout.addWidget(self.stored_files, 1, 0)
        layout.addWidget(self.download_button, 1, 1)
        layout.addWidget(self.label_1, 2, 0)
        layout.addWidget(self.file_selected_label, 3, 0)
        layout.addWidget(self.browse_button, 3, 1)
        layout.addWidget(self.label_3, 4, 0)
        layout.addWidget(self.key_editor, 5, 0)
        layout.addWidget(self.upload_button, 5, 1)
        layout.addWidget(self.logout_button, 6, 1)

        # Set layout
        self.setLayout(layout)

    def logout(self):
        self.logout_switch.emit()

    def start_processing(self):
        file_path = os.path.realpath(self.filename)
        file_size = os.stat(file_path).st_size
        needs_segmentation = False
        mem = virtual_memory()
        if file_size > mem.total:
            needs_segmentation = True

        key = self.key_editor.text()
        if len(key) > 32:
            return

        if needs_segmentation:
            divide_file_and_process(self.filename, key)
        else:
            process_file(self.filename, key, 1)

        self.status.setText("Processing Done")

    def retrieve_file(self):
        # meta data needed
        output_filename = os.path.realpath("lost.mp4.enc")
        segments_directory = os.path.realpath("output")
        file_segmented = False
        key = self.key_editor.text()
        if len(key) > 32:
            return
        retrieve_original_file(segments_directory, output_filename, key, file_segmented)

    def upload(self):
        if not self.filename:
            return
        self.start_processing()
        print("Processing Done")

    def download(self):
        pass

    def browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.filename = filename
        self.file_selected_label.setText("Chosen file: " + filename)
