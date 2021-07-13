from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem
from utils import get_user_files


class ShowFiles(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
        self.ui.show_files_back_pb.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def show_user_files(self):
        files = get_user_files(self.settings.token)
        list_widget = self.ui.show_files_list_widget
        list_widget.clear()
        QListWidgetItem("File Name" + ' \t\t| ' + "Size" + ' \t\t| ' + "Download Counts", list_widget)
        for file in files:
            QListWidgetItem(file["filename"] + ' \t\t| ' + str(file['size']) + ' \t\t| ' + str(file['download_counts'])
                            , list_widget)
