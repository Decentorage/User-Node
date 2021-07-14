import random
from PyQt5 import QtCore, QtWidgets
import os


class ContractDetails(QtWidgets.QWidget):

    cancel_contract_details_switch = QtCore.pyqtSignal()

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
        self.ui.contract_details_cancel_pb.clicked.connect(self.cancel_contract_details)

    def cancel_contract_details(self):
        self.cancel_contract_details_switch.emit()

    def load_file_details(self, file_path):
        file_size = os.stat(file_path).st_size
        self.ui.contract_details_file_size_label.setText("File Size: " +
                                                         "{:.2f}".format(file_size/self.settings.megabyte) + " MB")
        self.calculate_price()

    def calculate_price(self):
        price = random.randint(0, 1000)
        self.ui.contract_details_price_label.setText("Price:" + str(price))
