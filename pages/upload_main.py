from PyQt5 import QtCore, QtWidgets


class UploadMain(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()

    def __init__(self, ui):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        # Connectors
        self.ui.upload_main_back_pb.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.back_to_main_switch.emit()