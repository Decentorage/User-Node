from PyQt5 import QtCore, QtWidgets
import time


class UploadMain(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
        self.ui.upload_main_back_pb.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def poll_status(self):
        while self.ui.stackedWidget.currentWidget() == self.ui.upload_main_page:
            time.sleep(self.settings.upload_polling_time)
            print("Polling state")
            # TODO: get state of the user
