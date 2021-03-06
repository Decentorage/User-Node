from PyQt5 import QtCore, QtWidgets
from utils import get_user_state, process_file
import time
import json
import os
import webbrowser


class UploadMain(QtWidgets.QWidget):
    # Signals
    back_to_main_switch = QtCore.pyqtSignal()
    contract_details_switch = QtCore.pyqtSignal(str)
    start_uploading_switch = QtCore.pyqtSignal()

    def __init__(self, ui, helper):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.helper = helper
        self.filename = None
        self.key = None
        # Connectors
        self.ui.upload_main_back_pb.clicked.connect(self.back_to_main)
        self.ui.upload_main_initiate_contract_pb.clicked.connect(self.set_contract_details)
        self.ui.upload_main_start_uploading_pb.clicked.connect(self.start_uploading_switch.emit)
        self.ui.upload_main_encryption_key_line_edit.textChanged[str].connect(self.check_start_upload_conditions)
        self.ui.upload_main_request_contract_pb.clicked.connect(self.request_contract)
        self.ui.upload_main_pay_contract_pb.clicked.connect(self.request_contract)

    def back_to_main(self):
        self.back_to_main_switch.emit()

    def set_contract_details(self):
        self.browse()
        if self.filename:
            self.contract_details_switch.emit(self.filename)

    def request_contract(self):
        webbrowser.open_new(self.helper.frontend_url)

    def browse(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.filename = filename

    def start_uploading(self, progress_bar):
        if self.key:
            with open(self.helper.transfer_file) as json_file:
                transfer_obj = json.load(json_file)
                file_path = transfer_obj['file_path']
                progress_bar.set_size(transfer_obj['total_size_to_upload'])
            process_file(file_path, self.key, self.ui, progress_bar)
        else:
            if os.path.exists(self.helper.transfer_file):
                with open(self.helper.transfer_file) as json_file:
                    transfer_obj = json.load(json_file)
                    self.key = transfer_obj["key"]
                    file_path = transfer_obj['file_path']
                    progress_bar.set_size(transfer_obj['total_size_to_upload'])
                process_file(file_path, self.key, self.ui, progress_bar)
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    def poll_state(self):
        self.filename = None
        while not self.ui.about_to_close and self.ui.stackedWidget.currentWidget() == self.ui.upload_main_page:
            state = get_user_state(self.ui)
            # State: there is a pending contract paid
            if state == self.helper.state_upload_file:
                key_size = len(self.ui.upload_main_encryption_key_line_edit.text())
                if 0 < key_size < 32:
                    self.ui.upload_main_start_uploading_pb.setEnabled(True)
                else:
                    self.ui.upload_main_start_uploading_pb.setEnabled(False)
                # If there is a pending upload resume else start
                if os.path.exists(self.helper.transfer_file):
                    with open(self.helper.transfer_file) as json_file:
                        start_flag = json.load(json_file)['start_flag']
                    if not start_flag:
                        self.ui.upload_main_start_uploading_pb.setText("Resume Uploading")
                    else:
                        if 0 < key_size < 32:
                            self.ui.upload_main_start_uploading_pb.setText("Start Uploading")
                            self.ui.upload_main_start_uploading_pb.setEnabled(True)
                else:
                    self.ui.upload_main_start_uploading_pb.setText("Start Uploading")
                self.ui.upload_main_encryption_key_line_edit.setEnabled(True)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_pay_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.helper.state_upload_file_text)
            # State: no pending contract instance and there are seeds
            elif state == self.helper.state_create_contract:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(True)
                self.ui.upload_main_pay_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.helper.state_create_contract_text)
            # State: no pending contract instance and no seeds
            elif state == self.helper.state_no_seeds:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_pay_contract_pb.setEnabled(False)
                self.ui.upload_main_status_label.setText(self.helper.state_no_seeds_text)
            # State: there is a pending contract but not paid
            else:
                self.ui.upload_main_start_uploading_pb.setEnabled(False)
                self.ui.upload_main_encryption_key_line_edit.setEnabled(False)
                self.ui.upload_main_initiate_contract_pb.setEnabled(False)
                self.ui.upload_main_pay_contract_pb.setEnabled(True)
                self.ui.upload_main_status_label.setText(self.helper.state_unpaid_pending_contract_text)

            time.sleep(self.helper.upload_polling_time)

    def check_start_upload_conditions(self):
        self.key = self.ui.upload_main_encryption_key_line_edit.text()
        if (len(self.key) > 32) or (len(self.key) <= 0):
            self.ui.upload_main_start_uploading_pb.setEnabled(False)
        else:
            self.ui.upload_main_start_uploading_pb.setEnabled(True)
