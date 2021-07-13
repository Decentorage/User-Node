from PyQt5 import QtCore, QtWidgets
from utils import get_user_state
import time


class UploadMain(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()
    contract_details = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
        self.ui.upload_main_back_pb.clicked.connect(self.back_to_main)
        self.ui.upload_main_initiate_contract_pb.clicked.connect(self.set_contract_details)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def set_contract_details(self):
        self.contract_details.emit()

    def poll_state(self):
        while not self.ui.about_to_close and self.ui.stackedWidget.currentWidget() == self.ui.upload_main_page:
            state = get_user_state()

            if state == self.settings.state_upload_file:
                self.ui.upload_main_start_uploading_pb.setEnabled(True)
                self.ui.upload_main_initiae_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.settings.state_upload_file_text)

            elif state == self.settings.state_initiate_contract_instance:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(True)
                self.ui.upload_main_status_label.setText(self.settings.state_initiate_contract_instance_text)

            else:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.settings.state_recharge_text)

            time.sleep(self.settings.upload_polling_time)
