from PyQt5 import QtWidgets


class ContractDetails(QtWidgets.QWidget):

    def __init__(self, ui, settings):
        QtWidgets.QWidget.__init__(self)
        self.ui = ui
        self.settings = settings
        # Connectors
