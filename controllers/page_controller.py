import json
from PyQt5.QtCore import QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from pages import Main, Login, UploadMain, ContractDetails, ShowFiles, Transition
from PyQt5 import QtWidgets
from gui.ui import Ui_MainWindow
from .worker import call_worker
from .progress_bar import ProgressBar
import os


class PageController:

    def __init__(self, helper):
        self.application_window = QtWidgets.QWidget()
        self.application_window.setWindowIcon(QIcon(helper.icon_path))
        self.ui = Ui_MainWindow()
        self.ui.about_to_close = False
        self.ui.setupUi(self.application_window)
        self.application_window.setWindowTitle("Decentorage Client Application")
        self.ui.thread_pool = QThreadPool()
        self.ui.worker_waiting = False
        self.ui.waiting_spinner.start()
        self.helper = helper

        if self.helper.is_user_logged_in():
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

        # Pages
        self.login = Login(self.ui, self.helper)
        self.main = Main(self.ui, self.helper)
        self.upload_main = UploadMain(self.ui, self.helper)
        self.show_files = ShowFiles(self.ui, self.helper)
        self.contract_details = ContractDetails(self.ui, self.helper)
        self.transition = Transition(self.ui, self.helper)

        # Error page button
        self.ui.error_ok_pb.clicked.connect(self.return_from_error_page)

        # Event handlers
        self.main.logout_switch.connect(self.switch_to_login)
        self.main.show_my_files_switch.connect(self.switch_show_files)
        self.main.upload_files_switch.connect(self.switch_upload_main)
        self.show_files.back_to_main_switch.connect(self.switch_to_main)
        self.show_files.logout_switch.connect(self.switch_to_login)
        self.show_files.download_switch.connect(lambda: self.switch_start_download("Downloading File.."))
        self.upload_main.back_to_main_switch.connect(self.switch_to_main)
        self.upload_main.contract_details_switch.connect(self.switch_contract_details)
        self.upload_main.start_uploading_switch.connect(lambda: self.switch_start_upload("Uploading file.."))
        self.contract_details.go_to_upload_main_switch.connect(self.switch_upload_main)
        self.contract_details.request_contract_switch.connect(self.switch_create_contract)
        self.transition.okay_switch.connect(self.switch_to_main)

        if os.path.exists(self.helper.transfer_file):
            with open(self.helper.transfer_file) as json_file:
                transfer_file = json.load(json_file)
                start_flag = transfer_file['start_flag']
                if not start_flag and transfer_file['key'] and os.path.exists(self.helper.cache_file):
                    self.switch_start_upload("Resume Uploading file..")

        if os.path.exists(self.helper.download_transfer_file):
            with open(self.helper.download_transfer_file) as json_file:
                transfer_file = json.load(json_file)
                start_flag = transfer_file['start_flag']
                if not start_flag and transfer_file['key'] and os.path.exists(self.helper.cache_file):
                    self.switch_start_download("Resume Downloading file..")

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

    def switch_start_upload(self, msg):
        self.ui.progress_bar_page_label.setText(msg)
        self.ui.progress_bar_page_progress_bar.setValue(0)
        self.ui.stackedWidget.setCurrentWidget(self.ui.progress_bar_page)
        call_worker(lambda: self.upload_main.start_uploading(ProgressBar(self.ui.progress_bar_page_progress_bar)),
                    self.ui)

    def switch_create_contract(self):
        call_worker(self.contract_details.request_contract, self.ui, self.ui.upload_main_page, "Creating contract..")

    def switch_start_download(self, msg):
        self.ui.progress_bar_page_label.setText(msg)
        self.ui.stackedWidget.setCurrentWidget(self.ui.progress_bar_page)
        self.ui.progress_bar_page_progress_bar.setValue(0)
        call_worker(lambda: self.show_files.download(ProgressBar(self.ui.progress_bar_page_progress_bar)), self.ui)

    def logout(self):
        try:
            # Remove cached file
            os.remove(self.helper.cache_file)
        except:
            return

    def cleanup(self):
        self.ui.about_to_close = True
        os._exit(0)

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
