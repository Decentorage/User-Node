from PyQt5 import QtWidgets
import sys
from controllers import PageController


def main():
    app = QtWidgets.QApplication(sys.argv)
    page_controller = PageController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
