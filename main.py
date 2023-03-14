import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow

import mainpage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainpage.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())