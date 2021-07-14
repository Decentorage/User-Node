from PyQt5 import QtWidgets
import sys
from controllers import PageController
from utils import Settings, init_decentorage, init_file_transfer_user


def main():
    app = QtWidgets.QApplication(sys.argv)
    settings = Settings()
    settings.reset_directories()
    init_decentorage(settings)
    init_file_transfer_user(settings)
    page_controller = PageController(settings)
    app.aboutToQuit.connect(page_controller.cleanup)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
