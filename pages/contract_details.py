import random
from PyQt5 import QtCore, QtWidgets
import os
from utils import create_file


class ContractDetails(QtWidgets.QWidget):

    cancel_contract_details_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        self.contract_details = {}
        self.file_path = None
        # Connectors
        self.ui.contract_details_cancel_pb.clicked.connect(self.cancel_contract_details)
        self.ui.contract_details_request_pb.clicked.connect(self.request_contract)

    def cancel_contract_details(self):
        self.cancel_contract_details_switch.emit()

    def load_file_details(self, file_path):
        self.contract_details['file_size'] = os.stat(file_path).st_size
        self.file_path = file_path
        self.ui.contract_details_file_size_label.setText("File Size: " + "{:.2f}".format(
            self.contract_details['file_size']/self.settings.megabyte) + " MB")
        self.calculate_price()

    def calculate_price(self):
        price = random.randint(0, 1000)
        self.ui.contract_details_price_label.setText("Price:" + str(price))

    def request_contract(self):
        self.contract_details['download_count'] = self.ui.contract_details_download_counts_spin_box.value()
        self.contract_details['duration_in_months'] = self.ui.contract_details_months_spin_box.value()
        self.contract_details['filename'] = os.path.basename(self.file_path)
        self.contract_details['segments'], self.contract_details['segments_count'] = \
            self.settings.get_file_metadata(self.contract_details['file_size'])
        # create_file(self.contract_details)
