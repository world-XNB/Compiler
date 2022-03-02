# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from Compiler.aboutGUI import Ui_about
from Compiler.helpGUI import Ui_help
from Compiler.mainGUI import Ui_MainWindow


class PerGUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(PerGUI, self).__init__()
        self.setupUi(self)
        # 打开文件的内容
        self.data = None

    # 打开文件
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, "open file", '.')
        if fname[0]:
            f = open(fname[0], 'r', encoding='utf-8')
            with f:
                self.data = f.read()
                self.textEdit_3.setText(self.data)
                self.textEdit_2.setText('')
                self.textEdit.setText('')

    # 词法分析
    def W(self):
        self.textEdit.setText(self.data)
        self.textEdit_2.setText(self.data)

    # 语法分析
    def P(self):
        self.textEdit.setText(self.data)
        self.textEdit_2.setText(self.data)

    # 中间代码
    def M(self):
        self.textEdit.setText(self.data)
        self.textEdit_2.setText(self.data)

    # 目标代码
    def O(self):
        self.textEdit.setText(self.data)
        self.textEdit_2.setText(self.data)

    # 帮助
    def H(self):
        self.help = helpGUI()
        file = open("./file/help.txt", "r", encoding='utf-8')
        with file:
            d = file.read()
            self.help.textEdit.setText(d)
        self.help.show()

    # 关于compiler
    def A(self):
        self.about = aboutGUI()
        file = open("./file/about.txt", "r", encoding='utf-8')
        with file:
            d = file.read()
            self.about.textEdit.setText(d)
        self.about.show()


class helpGUI(Ui_help, QMainWindow):
    def __init__(self):
        super(helpGUI, self).__init__()
        self.setupUi(self)


class aboutGUI(Ui_about, QMainWindow):
    def __init__(self):
        super(aboutGUI, self).__init__()
        self.setupUi(self)


# 有重写
def fun():
    app = QApplication(sys.argv)
    per = PerGUI()
    per.show()
    sys.exit(app.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fun()
