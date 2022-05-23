# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from Compiler.LL1GUI import Ui_LL1
from Compiler.MCGeneration import MCG
from Compiler.OCGeneration import OCG
from Compiler.aboutGUI import Ui_about
from Compiler.Parser import Parser, LL1
from Compiler.helpGUI import Ui_help
from Compiler.mainGUI import Ui_MainWindow
from Compiler.Lex import Lex, dfaGUI


# 继承主界面
class PerGUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PerGUI, self).__init__(parent)
        self.setupUi(self)
        # 打开文件的内容
        self.data = None
        # 另存为文件的内容
        self.result = None
        # 打开文件的绝对路径
        self.Apath = None
        # 字符串形式的文件内容
        self.strdata = None
        # 用于衔接词法分析与语法分析
        self.tochen = []
        # 用于衔接词法分析与语法分析中的函数（错误分析）
        self.rows = {}
        # 语法树
        self.treeData = ""
        # 常量表
        self.constTbale = []
        # 函数表
        self.funTable = []
        # 变量表
        self.varTable = []
        # 中间代码表
        self.ICT = []

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
            # f = open(self.Apath, 'r', encoding='utf-8')
            f = open(self.Apath, 'r')
            with f:
                self.data = f.readlines()
                self.strdata = ''
                r = 1
                for i in self.data:
                    self.strdata = self.strdata + str(r) + "\t" + i
                    r = r + 1
                self.textEdit_3.setText(self.strdata)
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
        lex = Lex()
        lex.data = self.data
        lex.lexfun()
        self.tochen = lex.tochen
        self.rows = lex.rows
        print("tochen串如下：")
        print(self.tochen)
        print("tochen串对应的行列关系如下：")
        print(self.rows)
        text1 = '\t\t\ttochen串\n'
        text2 = '\t\t\t编译结果\n'
        for i in lex.tochen:
            if '有不合法的' in i:
                text2 = text2 + i + '\n'
                self.textEdit_2.setText(text2)
            else:
                text1 = text1 + i + '\n'
                self.textEdit.setText(text1)
                self.textEdit_2.setText("词法分析通过，正确程序")

    # 有穷自动机
    def DFA(self):
        self.dfa = dfaGUI()
        self.dfa.show()

    # 语法分析
    def P(self):
        parser = Parser()
        parser.tochen = self.tochen
        parser.rows = self.rows
        parser.pro()
        if parser.pos == len(parser.tochen) - 1 and parser.errorflag == 0:
            for i in parser.syntaxTree:
                self.treeData += i
                self.treeData += "\n"
            self.textEdit.setText(self.treeData)
            self.textEdit_2.setText("语法分析通过，正确程序")
        else:
            e = ""
            for i in parser.error:
                e += i + '\n'
            self.textEdit.setText(e)
            self.textEdit_2.setText("错误程序")

    # LL1
    def LL1(self):
        self.ll1 = LL1GUI()
        self.ll1.show()

    # 中间代码
    def M(self):
        mcg = MCG()
        mcg.tochen = self.tochen
        mcg.pro()
        self.constTbale = mcg.constTbale
        self.varTable = mcg.varTable
        self.funTable = mcg.funTable
        self.ICT = mcg.ICT
        print("中间代码生成：")
        print("常量表：" + str(mcg.constTbale))
        print("函数表：" + str(mcg.funTable))
        print("变量表：" + str(mcg.varTable))
        print("中间代码表：" + str(mcg.ICT))
        ict = ""
        for i in mcg.ICT:
            ict += '(' + str(i["number"]) + ',' + str(i["op"]) + ',' + str(i["arg1"]) + ',' + str(
                i["arg2"]) + ',' + str(i["result"]) + ')' '\n'
        # for i in mcg.ICT:
        #     print(i)
        if mcg.pos == len(mcg.tochen) - 1:
            self.textEdit.setText(ict)
            self.textEdit_2.setText("中间代码如上")
        else:
            print("错误程序")

    # 目标代码
    def O(self):
        ocg = OCG()
        ocg.constTbale = self.constTbale
        ocg.varTable = self.varTable
        ocg.funTable = self.funTable
        ocg.MCG = self.ICT
        print("常量表：" + str(ocg.constTbale))
        print("函数表：" + str(ocg.funTable))
        print("变量表：" + str(ocg.varTable))
        print("中间代码表：" + str(ocg.MCG))
        ocg.ASMinint()
        ocg.target()
        ocg.ASMend()

        print(ocg.ASM)
        asm = ""
        for i in ocg.ASM:
            if i[0] != '_':
                asm += "\t" + i + "\n"
            else:
                asm += i + "\n"

        self.textEdit.setText(asm)
        self.textEdit_2.setText("目标代码如上")

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
        file = open("./readme.md", "r", encoding='utf-8')
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


class LL1GUI(Ui_LL1, QMainWindow):
    def __init__(self):
        super(LL1GUI, self).__init__()
        self.setupUi(self)
        self.ll1 = LL1()
        self.count = 0  # 辅助单步显示

    def open(self):
        gra = self.ll1.openfile()
        temp = ""
        for i in gra:
            temp += i
        self.textEdit.setText(temp)

    def save(self):
        result = self.textEdit.toPlainText()
        filename = QFileDialog.getSaveFileName(self, 'save file')
        with open(filename[0], 'w', encoding='utf-8') as f:
            f.write(result)

    def confirm(self):
        self.ll1.judge()
        self.lineEdit.setText(str(self.ll1.judge()))

    def FATable(self):
        self.ll1.FATable()
        f = ""
        for fat in self.ll1.FAT.keys():
            f += str(fat) + " " + str(self.ll1.FAT[fat]) + '\n'
        self.textEdit_4.setText(f)

    def askFirst(self):
        temp = ""
        for key in self.ll1.grammer.keys():
            temp += key + str(self.ll1.First(key)) + '\n'
        self.textEdit_2.setText(temp)

    def askFollow(self):
        temp = ""
        for key in self.ll1.grammer.keys():
            temp += key + str(self.ll1.Follow(key)) + '\n'
        self.textEdit_3.setText(temp)

    def OS(self):
        print("单步显示")
        # self.ll1.Input = self.lineEdit_2.text()
        self.ll1.FA()
        print(self.ll1.process)
        pos = 1
        self.count = self.count + 1
        t1 = "步骤  分析栈  剩余字符串  推导所用产生式或匹配\n"
        for i in self.ll1.process:
            if self.count >= len(self.ll1.process) + 2:
                self.count = 0
            if pos >= self.count:
                break
            else:
                t1 += str(i["步骤"]) + "  " + str(i["分析栈"]) + "  " + str(i["剩余字符串"]) + "  " + str(i["推导所用产生式或匹配"]) + '\n'
                pos = pos + 1
        self.textEdit_5.setText(t1)

    def MS(self):
        print("多步显示")
        # self.ll1.Input = self.lineEdit_2.text()][[']
        self.ll1.FA()
        print(self.ll1.process)
        t2 = "步骤  分析栈  剩余字符串  推导所用产生式或匹配\n"
        for i in self.ll1.process:
            t2 += str(i["步骤"]) + "  " + str(i["分析栈"]) + "  " + str(i["剩余字符串"]) + "  " + str(i["推导所用产生式或匹配"]) + '\n'
        self.textEdit_5.setText(t2)


# 有重写
def fun():
    app = QApplication(sys.argv)
    per = PerGUI()
    per.show()
    sys.exit(app.exec_())


def fun1():
    app = QApplication(sys.argv)
    help = LL1GUI()
    help.show()
    sys.exit(app.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fun()
