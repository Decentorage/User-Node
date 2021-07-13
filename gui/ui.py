# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'decentorage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(759, 631)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
        self.stackedWidget.setObjectName("stackedWidget")
        self.loading_page = QtWidgets.QWidget()
        self.loading_page.setObjectName("loading_page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.loading_page)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.loading_text = QtWidgets.QLabel(self.loading_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.loading_text.setFont(font)
        self.loading_text.setAlignment(QtCore.Qt.AlignCenter)
        self.loading_text.setObjectName("loading_text")
        self.verticalLayout_14.addWidget(self.loading_text)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem1)
        self.waiting_spinner = QtWaitingSpinner(self.loading_page)
        self.waiting_spinner.setObjectName("waiting_spinner")
        self.horizontalLayout_15.addWidget(self.waiting_spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.horizontalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.setStretch(1, 2)
        self.horizontalLayout_15.setStretch(2, 1)
        self.verticalLayout_14.addLayout(self.horizontalLayout_15)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem3)
        self.verticalLayout_14.setStretch(0, 15)
        self.verticalLayout_14.setStretch(1, 1)
        self.verticalLayout_14.setStretch(2, 15)
        self.verticalLayout_14.setStretch(3, 15)
        self.verticalLayout_6.addLayout(self.verticalLayout_14)
        self.stackedWidget.addWidget(self.loading_page)
        self.contract_details_page = QtWidgets.QWidget()
        self.contract_details_page.setObjectName("contract_details_page")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.contract_details_page)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.contract_details_price_label = QtWidgets.QLabel(self.contract_details_page)
        self.contract_details_price_label.setObjectName("contract_details_price_label")
        self.verticalLayout_15.addWidget(self.contract_details_price_label)
        self.contract_details_file_size_label = QtWidgets.QLabel(self.contract_details_page)
        self.contract_details_file_size_label.setObjectName("contract_details_file_size_label")
        self.verticalLayout_15.addWidget(self.contract_details_file_size_label)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.contract_details_download_counts_label = QtWidgets.QLabel(self.contract_details_page)
        self.contract_details_download_counts_label.setObjectName("contract_details_download_counts_label")
        self.horizontalLayout_5.addWidget(self.contract_details_download_counts_label)
        self.contract_details_download_counts_spin_box = QtWidgets.QSpinBox(self.contract_details_page)
        self.contract_details_download_counts_spin_box.setMinimum(5)
        self.contract_details_download_counts_spin_box.setMaximum(550)
        self.contract_details_download_counts_spin_box.setObjectName("contract_details_download_counts_spin_box")
        self.horizontalLayout_5.addWidget(self.contract_details_download_counts_spin_box)
        self.verticalLayout_15.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.contract_details_duration_label = QtWidgets.QLabel(self.contract_details_page)
        self.contract_details_duration_label.setObjectName("contract_details_duration_label")
        self.horizontalLayout_6.addWidget(self.contract_details_duration_label)
        self.contract_details_months_spin_box = QtWidgets.QSpinBox(self.contract_details_page)
        self.contract_details_months_spin_box.setMinimum(1)
        self.contract_details_months_spin_box.setMaximum(120)
        self.contract_details_months_spin_box.setObjectName("contract_details_months_spin_box")
        self.horizontalLayout_6.addWidget(self.contract_details_months_spin_box)
        self.verticalLayout_15.addLayout(self.horizontalLayout_6)
        self.contract_details_request_pb = QtWidgets.QPushButton(self.contract_details_page)
        self.contract_details_request_pb.setObjectName("contract_details_request_pb")
        self.verticalLayout_15.addWidget(self.contract_details_request_pb)
        self.contract_details_cancel_pb = QtWidgets.QPushButton(self.contract_details_page)
        self.contract_details_cancel_pb.setObjectName("contract_details_cancel_pb")
        self.verticalLayout_15.addWidget(self.contract_details_cancel_pb)
        self.verticalLayout_16.addLayout(self.verticalLayout_15)
        self.stackedWidget.addWidget(self.contract_details_page)
        self.error_page = QtWidgets.QWidget()
        self.error_page.setObjectName("error_page")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.error_page)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem4)
        self.error_title = QtWidgets.QLabel(self.error_page)
        self.error_title.setAlignment(QtCore.Qt.AlignCenter)
        self.error_title.setObjectName("error_title")
        self.verticalLayout_13.addWidget(self.error_title)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem5)
        self.error_body = QtWidgets.QLabel(self.error_page)
        self.error_body.setAlignment(QtCore.Qt.AlignCenter)
        self.error_body.setWordWrap(True)
        self.error_body.setObjectName("error_body")
        self.verticalLayout_13.addWidget(self.error_body)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem6)
        self.error_ok_pb = QtWidgets.QPushButton(self.error_page)
        self.error_ok_pb.setObjectName("error_ok_pb")
        self.verticalLayout_13.addWidget(self.error_ok_pb)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem7)
        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.stackedWidget.addWidget(self.error_page)
        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.main_page)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem8)
        self.main_welcome_label = QtWidgets.QLabel(self.main_page)
        self.main_welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_welcome_label.setWordWrap(False)
        self.main_welcome_label.setObjectName("main_welcome_label")
        self.verticalLayout_8.addWidget(self.main_welcome_label)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem9)
        self.main_show_files_pb = QtWidgets.QPushButton(self.main_page)
        self.main_show_files_pb.setObjectName("main_show_files_pb")
        self.verticalLayout_8.addWidget(self.main_show_files_pb)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem10)
        self.main_upload_files_pb = QtWidgets.QPushButton(self.main_page)
        self.main_upload_files_pb.setObjectName("main_upload_files_pb")
        self.verticalLayout_8.addWidget(self.main_upload_files_pb)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem11)
        self.main_logout_pb = QtWidgets.QPushButton(self.main_page)
        self.main_logout_pb.setObjectName("main_logout_pb")
        self.verticalLayout_8.addWidget(self.main_logout_pb)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.stackedWidget.addWidget(self.main_page)
        self.show_files_page = QtWidgets.QWidget()
        self.show_files_page.setObjectName("show_files_page")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.show_files_page)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.groupbox_showfiles = QtWidgets.QGroupBox(self.show_files_page)
        self.groupbox_showfiles.setObjectName("groupbox_showfiles")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.groupbox_showfiles)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.show_files_list_widget = QtWidgets.QListWidget(self.groupbox_showfiles)
        self.show_files_list_widget.setAlternatingRowColors(True)
        self.show_files_list_widget.setObjectName("show_files_list_widget")
        self.verticalLayout_5.addWidget(self.show_files_list_widget)
        self.show_files_file_information_label = QtWidgets.QLabel(self.groupbox_showfiles)
        self.show_files_file_information_label.setText("")
        self.show_files_file_information_label.setScaledContents(False)
        self.show_files_file_information_label.setWordWrap(True)
        self.show_files_file_information_label.setObjectName("show_files_file_information_label")
        self.verticalLayout_5.addWidget(self.show_files_file_information_label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.show_files_decryption_key_label = QtWidgets.QLabel(self.groupbox_showfiles)
        self.show_files_decryption_key_label.setObjectName("show_files_decryption_key_label")
        self.horizontalLayout_3.addWidget(self.show_files_decryption_key_label)
        self.show_files_decryption_key_line_edit = QtWidgets.QLineEdit(self.groupbox_showfiles)
        self.show_files_decryption_key_line_edit.setEnabled(True)
        self.show_files_decryption_key_line_edit.setObjectName("show_files_decryption_key_line_edit")
        self.horizontalLayout_3.addWidget(self.show_files_decryption_key_line_edit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.show_files_download_pb = QtWidgets.QPushButton(self.groupbox_showfiles)
        self.show_files_download_pb.setEnabled(False)
        self.show_files_download_pb.setObjectName("show_files_download_pb")
        self.verticalLayout_5.addWidget(self.show_files_download_pb)
        self.show_files_back_pb = QtWidgets.QPushButton(self.groupbox_showfiles)
        self.show_files_back_pb.setObjectName("show_files_back_pb")
        self.verticalLayout_5.addWidget(self.show_files_back_pb)
        self.verticalLayout_5.setStretch(0, 10)
        self.verticalLayout_5.setStretch(1, 5)
        self.verticalLayout_5.setStretch(2, 5)
        self.verticalLayout_32.addLayout(self.verticalLayout_5)
        self.verticalLayout_10.addWidget(self.groupbox_showfiles)
        self.stackedWidget.addWidget(self.show_files_page)
        self.upload_main_page = QtWidgets.QWidget()
        self.upload_main_page.setObjectName("upload_main_page")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.upload_main_page)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.upload_main_status_label = QtWidgets.QLabel(self.upload_main_page)
        self.upload_main_status_label.setText("")
        self.upload_main_status_label.setObjectName("upload_main_status_label")
        self.verticalLayout_11.addWidget(self.upload_main_status_label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.upload_main_request_contract_pb = QtWidgets.QPushButton(self.upload_main_page)
        self.upload_main_request_contract_pb.setObjectName("upload_main_request_contract_pb")
        self.horizontalLayout_4.addWidget(self.upload_main_request_contract_pb)
        self.upload_main_initiate_contract_pb = QtWidgets.QPushButton(self.upload_main_page)
        self.upload_main_initiate_contract_pb.setObjectName("upload_main_initiate_contract_pb")
        self.horizontalLayout_4.addWidget(self.upload_main_initiate_contract_pb)
        self.verticalLayout_11.addLayout(self.horizontalLayout_4)
        self.upload_main_start_uploading_pb = QtWidgets.QPushButton(self.upload_main_page)
        self.upload_main_start_uploading_pb.setObjectName("upload_main_start_uploading_pb")
        self.verticalLayout_11.addWidget(self.upload_main_start_uploading_pb)
        self.upload_main_back_pb = QtWidgets.QPushButton(self.upload_main_page)
        self.upload_main_back_pb.setObjectName("upload_main_back_pb")
        self.verticalLayout_11.addWidget(self.upload_main_back_pb)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.stackedWidget.addWidget(self.upload_main_page)
        self.login_page = QtWidgets.QWidget()
        self.login_page.setObjectName("login_page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.login_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.login_page)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.login_information_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_information_label.sizePolicy().hasHeightForWidth())
        self.login_information_label.setSizePolicy(sizePolicy)
        self.login_information_label.setObjectName("login_information_label")
        self.verticalLayout_3.addWidget(self.login_information_label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.login_username_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_username_label.sizePolicy().hasHeightForWidth())
        self.login_username_label.setSizePolicy(sizePolicy)
        self.login_username_label.setObjectName("login_username_label")
        self.horizontalLayout_2.addWidget(self.login_username_label)
        self.login_username_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.login_username_line_edit.setObjectName("login_username_line_edit")
        self.horizontalLayout_2.addWidget(self.login_username_line_edit)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.login_password_label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_password_label.sizePolicy().hasHeightForWidth())
        self.login_password_label.setSizePolicy(sizePolicy)
        self.login_password_label.setObjectName("login_password_label")
        self.horizontalLayout.addWidget(self.login_password_label)
        self.login_password_line_edit = QtWidgets.QLineEdit(self.groupBox)
        self.login_password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_password_line_edit.setObjectName("login_password_line_edit")
        self.horizontalLayout.addWidget(self.login_password_line_edit)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 10)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.login_pb = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_pb.sizePolicy().hasHeightForWidth())
        self.login_pb.setSizePolicy(sizePolicy)
        self.login_pb.setObjectName("login_pb")
        self.verticalLayout_3.addWidget(self.login_pb, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.stackedWidget.addWidget(self.login_page)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.logo_widget = QtWidgets.QWidget(MainWindow)
        self.logo_widget.setMinimumSize(QtCore.QSize(1, 0))
        self.logo_widget.setObjectName("logo_widget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.logo_widget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.logo = QtWidgets.QLabel(self.logo_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(18)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(180, 40))
        self.logo.setMaximumSize(QtCore.QSize(360, 80))
        self.logo.setSizeIncrement(QtCore.QSize(18, 4))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/gui/decentorage.png"))
        self.logo.setScaledContents(True)
        self.logo.setWordWrap(False)
        self.logo.setObjectName("logo")
        self.horizontalLayout_7.addWidget(self.logo)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem13)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.logo_widget)
        self.verticalLayout_17.addLayout(self.verticalLayout)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loading_text.setText(_translate("MainWindow", "Loading text"))
        self.contract_details_price_label.setText(_translate("MainWindow", "TextLabel"))
        self.contract_details_file_size_label.setText(_translate("MainWindow", "File size:"))
        self.contract_details_download_counts_label.setText(_translate("MainWindow", "Download Counts"))
        self.contract_details_duration_label.setText(_translate("MainWindow", "Duration in months"))
        self.contract_details_request_pb.setText(_translate("MainWindow", "Request Contract"))
        self.contract_details_cancel_pb.setText(_translate("MainWindow", "Cancel"))
        self.error_title.setText(_translate("MainWindow", "ERROR_TITLE"))
        self.error_body.setText(_translate("MainWindow", "ERROR_BODY"))
        self.error_ok_pb.setText(_translate("MainWindow", "OK"))
        self.main_welcome_label.setText(_translate("MainWindow", "Welcome to Decentorage"))
        self.main_show_files_pb.setText(_translate("MainWindow", "Show My Files"))
        self.main_upload_files_pb.setText(_translate("MainWindow", "Upload Files"))
        self.main_logout_pb.setText(_translate("MainWindow", "Logout"))
        self.groupbox_showfiles.setTitle(_translate("MainWindow", "Files stored on Decentorage"))
        self.show_files_decryption_key_label.setText(_translate("MainWindow", "Decryption key"))
        self.show_files_download_pb.setText(_translate("MainWindow", "Download"))
        self.show_files_back_pb.setText(_translate("MainWindow", "Back To Main"))
        self.upload_main_request_contract_pb.setText(_translate("MainWindow", "Request Contract Instance"))
        self.upload_main_initiate_contract_pb.setText(_translate("MainWindow", "Initiate Contract Instance"))
        self.upload_main_start_uploading_pb.setText(_translate("MainWindow", "Start Uploading"))
        self.upload_main_back_pb.setText(_translate("MainWindow", "Back To Main"))
        self.login_information_label.setText(_translate("MainWindow", "Please log in to your Decentorage account"))
        self.login_username_label.setText(_translate("MainWindow", "Username"))
        self.login_password_label.setText(_translate("MainWindow", "Password"))
        self.login_pb.setText(_translate("MainWindow", "log in"))
from gui.QtWaitingSpinner import QtWaitingSpinner
import decentorage_logo_rc
