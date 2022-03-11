# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from Compiler.aboutGUI import Ui_about
from Compiler.helpGUI import Ui_help
from Compiler.mainGUI import Ui_MainWindow
from Compiler.Lex import Lex


class PerGUI(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(PerGUI, self).__init__()
        self.setupUi(self)
        # 打开文件的内容
        self.data = None
        # 另存为文件的内容
        self.result = None
        # 打开文件的绝对路径
        self.Apath = None

    # 新建
    def new(self):
        self.textEdit.setText('')
        self.textEdit_2.setText('')
        self.textEdit_3.setText('')

    # 打开文件
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, "open file", '.')
        self.Apath = fname[0]  # 记录绝对路径，后面保存要用
        if fname[0]:
            f = open(self.Apath, 'r', encoding='utf-8')
            with f:
                self.data = f.read()
                self.textEdit_3.setText(self.data)
                self.textEdit_2.setText('')
                self.textEdit.setText('')

    # 保存
    def save(self):
        if self.Apath is not None:
            self.result = self.textEdit_3.toPlainText()
            self.data = self.result
            with open(self.Apath, 'w', encoding='utf-8') as f:
                f.write(self.result)
        else:
            self.S()

    # 另存为
    def S(self):
        self.result = self.textEdit_3.toPlainText()
        filename = QFileDialog.getSaveFileName(self, 'save file')
        with open(filename[0], 'w', encoding='utf-8') as f:
            f.write(self.result)

    # 词法分析
    def W(self):
        self.data = self.textEdit_3.toPlainText()  # 更新输入框中的内容
        self.textEdit.setText(self.data)
        self.textEdit_2.setText(self.data)

    # 识别单词
    def D(self):
        self.data = self.textEdit_3.toPlainText()  # 更新输入框中的内容
        lex = Lex()
        self.textEdit.setText(lex.fun(self.data))
        print(lex.tochen)
        self.textEdit_2.setText(str(lex.tochen))

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
