from PyQt5 import QtWidgets
import sys
from controllers import PageController
from utils import Settings, init_decentorage


def main():
    app = QtWidgets.QApplication(sys.argv)
    settings = Settings()
    settings.reset_directories()
    init_decentorage(settings)
    page_controller = PageController(settings)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
