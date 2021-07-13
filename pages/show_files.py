from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from utils import get_user_files, retrieve_original_file


class ShowFiles(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()
    logout_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        self.index = None
        self.files = None
        self.key = None

        # Connectors
        self.ui.show_files_back_pb.clicked.connect(self.back_to_main)
        self.ui.show_files_decryption_key_line_edit.textChanged[str].connect(self.check_download_conditions)
        self.ui.show_files_download_pb.clicked.connect(self.download)
        self.ui.show_files_list_widget.clicked.connect(self.item_selected)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def show_user_files(self):
        self.index = None
        response = get_user_files()
        if response == self.settings.redirect_to_login:
            self.logout_switch.emit()
        self.files = response
        list_widget = self.ui.show_files_list_widget
        list_widget.clear()
        if not self.files:
            self.ui.show_files_download_pb.setEnabled(False)
            self.ui.show_files_decryption_key_line_edit.setEnabled(False)
            QListWidgetItem("No Files stored", list_widget).setFlags(Qt.NoItemFlags)
            return
        QListWidgetItem("File Name" + ' \t\t| ' + "Size" + ' \t\t| ' + "Download Counts", list_widget)\
            .setFlags(Qt.NoItemFlags)
        for file in self.files:
            QListWidgetItem(file["filename"] + ' \t\t| ' + str(file['size']) + ' \t\t| ' + str(file['download_counts'])
                            , list_widget)

    def check_download_conditions(self):
        self.key = self.ui.show_files_decryption_key_line_edit.text()
        if (len(self.key) > 32) or (len(self.key) <= 0):
            self.ui.show_files_download_pb.setEnabled(False)
        else:
            if self.index:
                self.ui.show_files_download_pb.setEnabled(True)

    def item_selected(self):
        self.index = self.ui.show_files_list_widget.currentRow() - 1

    def download(self):
        print("downloading", self.index, self.files[self.index]['filename'])
        # Sequence download shard for all file segments in download directory then decode and decrypt.
        # TODO: Download

        file_metadata = {}
        # After files have been downloaded => decode and decrypt.
        retrieve_original_file(self.key, file_metadata)
