from PyQt5.QtCore import QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

from pages import MainWindow, Login
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow


class PageController:

    # Page indices
    login_index = 0
    main_window_index = 1

    def __init__(self):

        self.application_window = QtWidgets.QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.application_window)
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
        self.ui.thread_pool = QThreadPool()
        self.ui.worker_waiting = False
        self.ui.waiting_spinner.start()
        # Pages
        self.login = Login(self.ui)
        # Error page button
        self.ui.error_ok_pb.clicked.connect(lambda: return_from_error_page(self.ui))
        # Add widgets

        self.application_window.show()

    def switch_to_main(self):
        self.application_window.setWindowTitle("Welcome to Decentorage")
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)


@pyqtSlot(QWidget)
def return_from_error_page(ui):
    change_current_page(ui, ui.error_source_page)
    ui.worker_waiting = False


def change_current_page(ui, target_page):
    class ChangePageSignalEmitter(QObject):
        change_page_trigger = pyqtSignal(QWidget)

        def change_page(self, stacked_widget, target):
            self.change_page_trigger.connect(stacked_widget.setCurrentWidget)
            self.change_page_trigger.emit(target)

    change_page_signal_emitter = ChangePageSignalEmitter()
    change_page_signal_emitter.change_page(ui.stackedWidget, target_page)