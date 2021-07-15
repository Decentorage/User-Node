from PyQt5 import QtWidgets
import sys
from controllers import PageController
from utils import Helper, init_decentorage, init_file_transfer_user


def main():
    app = QtWidgets.QApplication(sys.argv)
    helper = Helper()
    init_decentorage(helper)
    init_file_transfer_user(helper)
    page_controller = PageController(helper)
    app.aboutToQuit.connect(page_controller.cleanup)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
