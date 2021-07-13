from PyQt5.QtCore import QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
from pages import Main, Login, UploadMain, ContractDetails, ShowFiles
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow
from .worker import call_worker
import os


class PageController:

    def __init__(self, settings):
        self.application_window = QtWidgets.QWidget()
        self.application_window.setWindowTitle("Welcome to Decentorage")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.application_window)
        self.ui.thread_pool = QThreadPool()
        self.ui.worker_waiting = False
        self.ui.waiting_spinner.start()
        self.settings = settings

        if self.settings.is_user_logged_in():
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

        # Pages
        self.login = Login(self.ui, self.settings)
        self.main = Main(self.ui, self.settings)
        self.upload_main = UploadMain(self.ui, self.settings)
        self.show_files = ShowFiles(self.ui, self.settings)
        self.contract_details = ContractDetails(self.ui, self.settings)

        # Error page button
        self.ui.error_ok_pb.clicked.connect(lambda: return_from_error_page(self.ui))

        # Event handlers
        self.main.logout_switch.connect(self.switch_to_login)
        self.main.show_my_files_switch.connect(self.switch_show_files)
        self.main.upload_files_switch.connect(self.switch_upload_main)
        self.show_files.back_to_main_switch.connect(self.switch_to_main)
        self.show_files.logout_switch.connect(self.switch_to_login)
        self.upload_main.back_to_main_switch.connect(self.switch_to_main)

        # Show window
        self.application_window.show()

    def switch_to_main(self):
        self.application_window.setWindowTitle("Welcome to Decentorage")
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    def switch_to_login(self):
        self.application_window.setWindowTitle("Login")
        self.logout()
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def switch_upload_main(self):
        self.application_window.setWindowTitle("Upload main page")
        self.ui.stackedWidget.setCurrentWidget(self.ui.upload_main_page)
        call_worker(self.upload_main.poll_status, self.ui)

    def switch_show_files(self):
        self.application_window.setWindowTitle("My files")
        call_worker(self.show_files.show_user_files, self.ui, self.ui.show_files_page, "loading Files..")

    def logout(self):
        try:
            # Remove cached file
            os.remove(self.settings.cache_filename)
        except:
            return


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