from PyQt5.QtCore import QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

from pages import Main, Login
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow


class PageController:

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
        self.main = Main(self.ui)

        # Error page button
        self.ui.error_ok_pb.clicked.connect(lambda: return_from_error_page(self.ui))

        # Event handlers
        self.main.logout_switch.connect(self.switch_to_login)
        self.main.show_my_files_switch.connect(self.switch_show_files)
        self.main.upload_switch.connect(self.switch_upload_main)

        self.application_window.show()

    def switch_to_login(self):
        self.application_window.setWindowTitle("Login")
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def switch_upload_main(self):
        self.application_window.setWindowTitle("Upload main page")
        self.ui.stackedWidget.setCurrentWidget(self.ui.upload_main_page)

    def switch_show_files(self):
        self.application_window.setWindowTitle("My files")
        self.ui.stackedWidget.setCurrentWidget(self.ui.show_files_page)


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