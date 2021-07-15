from PyQt5 import QtCore, QtWidgets
from utils import get_user_state, process_file
import time
import json


class UploadMain(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()
    contract_details_switch = QtCore.pyqtSignal(str)

    def __init__(self, ui, helper):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.helper = helper
        self.filename = None
        self.key = None
        # Connectors
        self.ui.upload_main_back_pb.clicked.connect(self.back_to_main)
        self.ui.upload_main_initiate_contract_pb.clicked.connect(self.set_contract_details)
        self.ui.upload_main_start_uploading_pb.clicked.connect(self.start_uploading)
        self.ui.upload_main_encryption_key_line_edit.textChanged[str].connect(self.check_start_upload_conditions)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def set_contract_details(self):
        self.browse()
        if self.filename:
            self.contract_details_switch.emit(self.filename)

    def browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.filename = filename

    def start_uploading(self):
        with open(self.helper.upload_connection_file) as json_file:
            file_path = json.load(json_file)
        process_file(file_path, self.key)

    def poll_state(self):
        self.filename = None
        while not self.ui.about_to_close and self.ui.stackedWidget.currentWidget() == self.ui.upload_main_page:
            state = get_user_state()

            if state == self.helper.state_upload_file:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(True)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.helper.state_upload_file_text)

            elif state == self.helper.state_initiate_contract_instance:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(True)
                self.ui.upload_main_status_label.setText(self.helper.state_initiate_contract_instance_text)

            else:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.helper.state_recharge_text)

            time.sleep(self.helper.upload_polling_time)

    def check_start_upload_conditions(self):
        self.key = self.ui.upload_main_encryption_key_line_edit.text()
        if (len(self.key) > 32) or (len(self.key) <= 0):
            self.ui.upload_main_start_uploading_pb.setEnabled(False)
        else:
            self.ui.upload_main_start_uploading_pb.setEnabled(True)
