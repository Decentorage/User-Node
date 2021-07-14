from PyQt5.QtCore import QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from pages import Main, Login, UploadMain, ContractDetails, ShowFiles
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow
from .worker import call_worker
import os


class PageController:

    def __init__(self, settings):
        self.application_window = QtWidgets.QWidget()
        self.application_window.setWindowIcon(QIcon(settings.icon_path))
        self.ui = Ui_MainWindow()
        self.ui.about_to_close = False
        self.ui.setupUi(self.application_window)
        self.application_window.setWindowTitle("Decentorage Client Application")
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
        self.ui.error_ok_pb.clicked.connect(self.return_from_error_page)

        # Event handlers
        self.main.logout_switch.connect(self.switch_to_login)
        self.main.show_my_files_switch.connect(self.switch_show_files)
        self.main.upload_files_switch.connect(self.switch_upload_main)
        self.show_files.back_to_main_switch.connect(self.switch_to_main)
        self.show_files.logout_switch.connect(self.switch_to_login)
        self.upload_main.back_to_main_switch.connect(self.switch_to_main)
        self.upload_main.contract_details_switch.connect(self.switch_contract_details)
        self.contract_details.cancel_contract_details_switch.connect(self.switch_upload_main)

        # Show window
        self.application_window.show()

    def switch_to_main(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    def switch_to_login(self):
        self.logout()
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def switch_upload_main(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.upload_main_page)
        call_worker(self.upload_main.poll_state, self.ui)

    def switch_show_files(self):
        call_worker(self.show_files.show_user_files, self.ui, self.ui.show_files_page, "loading Files..")

    def switch_contract_details(self, file_path):
        call_worker(lambda: self.contract_details.load_file_details(file_path), self.ui,
                    self.ui.contract_details_page, "loading File details..")

    def logout(self):
        try:
            # Remove cached file
            os.remove(self.settings.cache_file)
        except:
            return

    def cleanup(self):
        self.ui.about_to_close = True
        # os._exit(0)

    def return_from_error_page(self):
        self.change_current_page(self.ui.error_source_page)
        self.ui.worker_waiting = False

    def change_current_page(self, target_page):
        class ChangePageSignalEmitter(QObject):
            change_page_trigger = pyqtSignal(QWidget)

            def change_page(self, stacked_widget, target):
                self.change_page_trigger.connect(stacked_widget.setCurrentWidget)
                self.change_page_trigger.emit(target)
        change_page_signal_emitter = ChangePageSignalEmitter()
        change_page_signal_emitter.change_page(self.ui.stackedWidget, target_page)