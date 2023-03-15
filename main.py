import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from pages.mainpage import Ui_MainWindow

class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        # self.login_pushButton.clicked.connect(self.display)
        # 添加退出按钮信号和槽。调用close函数
        # self.cancel_pushButton.clicked.connect(self.close)

    # def display(self):
        # username = self.un_lineEdit.text()
        # password = self.pw_lineEdit.text()

        # self.textBrowser.setText("Success!\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = mainpage.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    myMainPage = MainPage()
    myMainPage.show()
    sys.exit(app.exec_())