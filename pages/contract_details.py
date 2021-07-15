from PyQt5 import QtCore, QtWidgets
import os
from utils import create_file, get_price


class ContractDetails(QtWidgets.QWidget):

    go_to_upload_main_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        self.contract_details = {}
        self.file_path = None
        # Connectors
        self.ui.contract_details_cancel_pb.clicked.connect(self.cancel_contract_details)
        self.ui.contract_details_request_pb.clicked.connect(self.request_contract)
        self.ui.contract_details_download_counts_spin_box.valueChanged.connect(self.calculate_price)
        self.ui.contract_details_months_spin_box.valueChanged.connect(self.calculate_price)

    def cancel_contract_details(self):
        self.go_to_upload_main_switch.emit()

    def load_file_details(self, file_path):
        self.contract_details['file_size'] = os.stat(file_path).st_size
        self.file_path = file_path
        unit = ["B", "KB", "MB", "GB"]
        index = 0
        file_size = self.contract_details['file_size']
        while int(file_size/self.settings.kilobyte) > 0 and index < 3:
            index += 1
            file_size = file_size/self.settings.kilobyte
        self.ui.contract_details_file_size_label.setText("File Size: " + "{:.3f}".format(file_size) + " " + unit[index])
        self.calculate_price()

    def calculate_price(self):
        self.contract_details['download_count'] = self.ui.contract_details_download_counts_spin_box.value()
        self.contract_details['duration_in_months'] = self.ui.contract_details_months_spin_box.value()
        price = get_price(self.contract_details)
        if price == self.settings.min_price:
            self.ui.contract_details_price_label.setText("Minimum price:" + str(self.settings.min_price) + " $")
        else:
            self.ui.contract_details_price_label.setText("Price:" + str(float(price)) + " $")

    def request_contract(self):
        self.contract_details['download_count'] = self.ui.contract_details_download_counts_spin_box.value()
        self.contract_details['duration_in_months'] = self.ui.contract_details_months_spin_box.value()
        self.contract_details['filename'] = os.path.basename(self.file_path)
        self.contract_details['segments'], self.contract_details['segments_count'] = \
            self.settings.get_file_metadata(self.contract_details['file_size'])
        # If file is created successfully go to upload main page
        if create_file(self.contract_details):
            self.go_to_upload_main_switch.emit()
