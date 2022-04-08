# -*- coding:utf-8 -*-
# @Time : 2022/3/16 16:32
# @Author : 西~南~北
# @File : Test.py
# @Software: PyCharm


# 词法分析类
import re
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene

from Compiler.dfaGUI import Ui_DFA

# 设置字体为楷体
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']


class Lex:
    def __init__(self):
        # 'integer': 整数, 'character': 字符, 'charstr': 字符串, 'identifier': 标识符', 'realnum': 实数（float） sample语言单词的种别码
        self.sample = {'char': 101, 'int': 102, 'float': 103, 'break': 104, 'const': 105, 'return': 106, 'void': 107,
                       'continue': 108, 'do': 109, 'while': 110, 'if': 111, 'else': 112, 'for': 113, 'string': 114,
                       'bool': 115, 'scanf': 116, 'printf': 117, 'include': 118, '{': 301, '}': 302, ';': 303, ',': 304,
                       'integer': 400,
                       'character': 500, 'charstr': 600, 'identifier': 700, 'realnum': 800, '(': 201, ')': 202,
                       '[': 203, ']': 204, '!': 205, '*': 206, '/': 207, '%': 208, '+': 209, '-': 210, '<': 211,
                       '<=': 212, '>': 213, '>=': 214, '==': 215, '!=': 216, '&&': 217, '||': 218, '=': 219, '.': 220,
                       '++': 221, '+=': 222, '--': 223, '-=': 224, '&': 225, '#': 226}
        self.tochen = []  # 最终输出的tochen串
        self.data = []
        self.flag = 0  # 多行注释标志
        self.a = 0  # 单词起点
        self.b = 0  # 单词终点
        self.flagword = 0  # lagword=1:正确单词可以裁剪；flagword==0:不合法的单词不可裁剪

    # 裁剪函数：line:裁剪的哪一行;num：裁剪出单词的种别码
    def cut(self, line, num):
        temp = ''
        if self.flagword == 1:
            for t in range(self.a, self.b):
                temp = temp + line[t]
            if temp in self.sample.keys():
                self.tochen.append('(' + str(self.sample[temp]) + ',"' + temp + '")')
            else:
                self.tochen.append('(' + str(num) + ',"' + temp + '")')
            self.flagword = 0
        else:
            self.tochen.append(
                '第' + str(self.data.index(line) + 1) + '行有不合法的' + list(self.sample.keys())[
                    list(self.sample.values()).index(num)])

    # 词法分析函数
    def lexfun(self):
        for line in self.data:
            # 删除多行注释
            if self.flag == 1:
                if "*/" in line:
                    self.flag = 0
                continue

            i = 0  # 下标：定位每一行的位置
            while i < len(line) - 1:
                # 判断标识符
                if line[i].isalpha() or line[i] == '_':
                    self.a = i
                    i = i + 1
                    while line[i].isalnum() or line[i] == '_':
                        i = i + 1
                    if line[i] in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                        self.flagword = 1
                    self.b = i
                    self.cut(line, 700)

                # 判断十进制整数
                elif line[i] > '0' and line[i] <= '9':
                    self.a = i
                    i = i + 1
                    while line[i].isdigit():
                        i = i + 1
                    if line[i] == '.':
                        i = i + 1
                    while line[i].isdigit():
                        i = i + 1
                    if line[i] in ['E', 'e']:
                        i = i + 1
                        if line[i] in ['+', "-"]:
                            i = i + 1
                        while line[i].isdigit():
                            i = i + 1
                    if line[i] in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                        if line[i] != '.':
                            self.flagword = 1
                    else:
                        while line[i] not in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                            i = i + 1
                    self.b = i
                    self.cut(line, 102)

                # 判断八进制和十六进制
                elif line[i] == '0':
                    self.a = i
                    i = i + 1
                    if line[i] == '.':
                        i = i + 1
                        while line[i].isdigit():
                            i = i + 1
                        if line[i] in ['e', 'E']:
                            i = i + 1
                            if line[i] in ['+', "-"]:
                                i = i + 1
                            while line[i].isdigit():
                                i = i + 1
                        if line[i] in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                            self.flagword = 1
                        self.b = i
                        self.cut(line, 102)

                    elif line[i].isdigit():
                        if line[i] in ['0', '8', '9']:
                            while line[i] not in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                                i = i + 1
                            self.flagword = 0
                            self.cut(line, 102)
                        else:
                            i = i + 1
                            while line[i] >= '0' and line[i] <= '7':
                                i = i + 1
                            if line[i] in [' ', '\t', '\n'] or line[i] in self.sample.keys() and line[i] != '.':
                                self.flagword = 1
                            else:
                                while line[i] not in [' ', '\t', '\n']:
                                    i = i + 1
                            self.b = i
                            self.cut(line, 102)

                    elif line[i] in ['X', 'x']:
                        i = i + 1
                        while line[i].isdigit() or line[i] in ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E',
                                                               'F']:
                            i = i + 1
                        if line[i] in [' ', '\t', '\n'] or line[i] in self.sample.keys():
                            self.flagword = 1
                        else:
                            while line[i] not in [' ', '\t', '\n']:
                                i = i + 1
                        self.b = i
                        self.cut(line, 102)

                    elif line[i] in self.sample.keys():
                        self.tochen.append('(102,"0")')
                        i = i + 1
                    else:
                        while line[i] not in [' ', '\t', '\n']:
                            i = i + 1

                # 判断注释和除法
                elif line[i] == '/':
                    i = i + 1
                    if line[i] == '/':
                        break
                    elif line[i] == '*':
                        i = i + 1
                        if "*/" in line:
                            while line[i] != '*' and line[i + 1] != '/':
                                i = i + 1
                            i = i + 2
                        else:
                            self.flag = 1
                            break
                    elif line[i].isalnum() or line[i] == '_':
                        self.tochen.append('(207,"/")')

                # 判断空格
                elif line[i] in [' ', '\t']:
                    i = i + 1

                # 判断字符常数
                elif line[i] in ['\'']:
                    self.a = i
                    i = i + 1
                    while line[i] not in ['\n', ';']:
                        while line[i] != '\'':
                            i = i + 1
                            self.flagword = 1
                            if line[i] == ';':
                                self.flagword = 0
                                break
                        break
                    i = i + 1
                    self.b = i
                    self.cut(line, 500)

                # 判断字符串常数
                elif line[i] in ['\"']:
                    self.a = i
                    i = i + 1
                    while line[i] not in ['\n', ';']:
                        while line[i] != '\"':
                            i = i + 1
                            self.flagword = 1
                            if line[i] == ';':
                                self.flagword = 0
                                break
                        break
                    i = i + 1
                    self.b = i
                    self.cut(line, 600)

                # 其他：分界符、运算符
                else:
                    # 运算符
                    if line[i] in self.sample.keys() and line[i] not in ['/', '<', '>', '=', '!', '&', '+', '-', '{',
                                                                         '}', ';', ',']:
                        if line[i] == '.' and line[i + 1].isdigit():
                            while line[i] not in [' ', '\t', '\n']:
                                i = i + 1
                        else:
                            self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                            i = i + 1

                    elif line[i] in ['<', '>', '=', '!']:
                        self.a = i
                        i = i + 1
                        if line[i] in ['=']:
                            i = i + 1
                            self.b = i
                            self.flagword = 1
                            if line[i - 2] == '>':
                                self.cut(line, 214)
                            elif line[i - 2] == '<':
                                self.cut(line, 212)
                            elif line[i - 2] == '=':
                                self.cut(line, 215)
                            elif line[i - 2] == '!':
                                self.cut(line, 216)
                        else:
                            i = i - 1
                            self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                            i = i + 1
                    elif line[i] in ['+']:
                        self.a = i
                        i = i + 1
                        if line[i] in ['=', '+']:
                            i = i + 1
                            self.b = i
                            self.flagword = 1
                            if line[i - 1] == '=':
                                self.cut(line, 222)
                            elif line[i - 1] == '+':
                                self.cut(line, 221)
                        else:
                            i = i - 1
                            self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                            i = i + 1
                    elif line[i] in ['-']:
                        self.a = i
                        i = i + 1
                        if line[i] in ['=', '-']:
                            i = i + 1
                            self.b = i
                            self.flagword = 1
                            if line[i - 1] == '=':
                                self.cut(line, 224)
                            elif line[i - 1] == '-':
                                self.cut(line, 223)
                        else:
                            i = i - 1
                            self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                            i = i + 1
                    elif line[i] == '&':
                        self.a = i
                        i = i + 1
                        if line[i] in ['&']:
                            i = i + 1
                            self.b = i
                            self.flagword = 1
                            self.cut(line, 217)
                        else:
                            i = i - 1
                            self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                            i = i + 1
                    # 界符
                    elif line[i] in ['{', '}', ';', ',']:
                        self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                        i = i + 1
                    # 其他
                    else:
                        self.tochen.append('第' + str(self.data.index(line) + 1) + '行有不合法的单词')
                        while line[i] not in [' ', '\n', '\t']:
                            i = i + 1


# 有穷自动机类
class dfaGUI(Ui_DFA, QMainWindow):
    def __init__(self):
        super(dfaGUI, self).__init__()
        self.setupUi(self)
        self.regular = None
        # self.regular = "01*|1"
        self.nfalist = []  # nfa的三元组
        self.dfalist = []  # dfa的三元组
        self.mfalist = []  # mfa的三元组

        # dfa
        self.dfacount = 0  # 记录现在在第几行（状态转换表）
        self.Input = []  # 记录输入字母表
        self.dfadic = {}  # 记录每一行的数据（状态转换表）
        self.dictemp = {}  # 记录第一列对应的字母（状态转换表）

        # mfa
        self.mfacount = 1  # 记录区分的状态
        self.mfaflag = 0  # 记录是否递归   0：递归    1：不递归
        self.mfatemp = {}  # 记录区分的状态

    # 验证正则表达式
    def check(self):
        self.regular = self.lineEdit.text()
        try:
            re.compile(self.regular)  # 编译——如果不是合法的正则表达式会抛出错误
            self.lineEdit_2.setText("合法的正则表达式")
            for i in self.regular:  # 生成输入字母表
                if i not in ['*', '|', '(', ')']:
                    self.Input.append(i)
            self.Input = list(set(self.Input))
            return True
        except:
            self.lineEdit_2.setText("不合法的正则表达式")
            return False

    # 正则表达式到NFA的转换
    def nfa(self):
        self.nfalist.clear()
        count = 0  # 记录状态转换图的状态
        count1 = 0  # 记录开始状态
        count3 = 0  # 记录（的后面字符状态
        count4 = 0  # 记录）的前面字符状态
        if self.check():  # 开始转换
            if len(self.regular) == 0:
                tuple = ('x', 'y', '$')
                self.dfalist.append(tuple)
            for i in range(len(self.regular)):
                if self.regular[i] not in ['|', '*', '(', ')']:
                    tuple = (count, count + 1, self.regular[i])
                    count = count + 1
                    self.nfalist.append(tuple)
                elif self.regular[i] == '|':
                    tuple = ('x', count1, '$')
                    self.nfalist.append(tuple)
                    tuple = (count, 'y', '$')
                    self.nfalist.append(tuple)
                    count = count + 1
                    count1 = count  # 更新count1
                    continue
                elif self.regular[i] == '*':
                    if self.regular[i - 1] == ')':
                        tuple = (count4, count3, '$')
                        self.nfalist.append(tuple)
                        tuple = (count4, count4 + 1, '$')
                        self.nfalist.append(tuple)
                        tuple = (count3, count4 + 1, '$')
                        self.nfalist.append(tuple)
                    else:
                        tuple = (count, count - 1, '$')
                        self.nfalist.append(tuple)
                        tuple = (count, count + 1, '$')
                        self.nfalist.append(tuple)
                        tuple = (count - 1, count + 1, '$')
                        self.nfalist.append(tuple)
                        count = count + 1
                elif self.regular[i] == '(':
                    count = count + 1
                    count3 = count
                elif self.regular[i] == ')':
                    count4 = count
            tuple = ('x', count1, '$')
            self.nfalist.append(tuple)
            tuple = (count, 'y', '$')
            self.nfalist.append(tuple)

            # 图的可视化
            plt.figure()
            G = nx.DiGraph()
            start = []
            end = []
            edge_labels = []
            for i in self.nfalist:
                start.append(i[0])
                end.append(i[1])
                edge_labels.append(i[2])
            for i in range(len(start)):
                G.add_edges_from([(start[i], end[i], {'attr': str(edge_labels[i])})])
            edge_labels = nx.get_edge_attributes(G, 'attr')  # 获取边的name属性，
            nx.draw_networkx_edge_labels(G, pos=nx.spectral_layout(G), edge_labels=edge_labels,
                                         font_size=7)  # 将name属性，显示在边上
            nx.draw(G, with_labels=True, pos=nx.spectral_layout(G))
            plt.savefig("./file/NFA.jpg")

            # 显示图片
            frame = QImage("./file/NFA.jpg")
            pix = QPixmap.fromImage(frame)
            item = QGraphicsPixmapItem(pix)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.graphicsView.setScene(scene)
            # self.graphicsView.fitInView(item)  # 图像自适应
        else:
            print('该正则表达式不合法！')

    # NFA到DFA的转换
    def dfa(self):
        self.dfalist.clear()
        listI = []  # 记录首列的值（状态转换表）
        l = ['x']
        for i in self.nfalist:  # 生成首行首列的值（状态转换表）
            if i[0] == 'x' and i[2] == '$':
                l.append(i[1])
        listI.append(l)
        # 递归调用——生成转台转换表self.dfadic
        self.recursion_c(listI)

        temp = 'A'
        lkey = list(self.dfadic.keys())
        self.dictemp[lkey[0]] = 'S'
        del lkey[0]
        for i in range(len(lkey)):
            self.dictemp[lkey[i]] = temp
            temp = chr(ord(temp) + 1)

        # for i in self.dfadic.keys():
        #     print(str(i) + str(self.dfadic[i]))

        # 生成self.dfalist
        for i in self.dfadic.keys():
            for j in self.dictemp.keys():
                if i == j:  # 判断dfadic.keys()对应的字母
                    for k in range(len(self.dfadic[i])):
                        for l in self.dictemp.keys():
                            if tuple(self.dfadic[i][k]) == l:
                                t = [self.dictemp[j], self.dictemp[l], k]
                                self.dfalist.append(t)

        # 图的可视化
        plt.figure()
        G = nx.DiGraph()
        start = []
        end = []
        edge_labels = []
        for i in self.dfalist:
            start.append(i[0])
            end.append(i[1])
            edge_labels.append(i[2])
        for i in range(len(start)):
            G.add_edges_from([(start[i], end[i], {'attr': str(edge_labels[i])})])
        edge_labels = nx.get_edge_attributes(G, 'attr')  # 获取边的name属性，
        nx.draw_networkx_edge_labels(G, pos=nx.spectral_layout(G), edge_labels=edge_labels,
                                     font_size=7)  # 将name属性，显示在边上
        nx.draw(G, with_labels=True, pos=nx.spectral_layout(G))
        plt.savefig("./file/DFA.jpg")

        # 显示图片
        frame = QImage("./file/DFA.jpg")
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.graphicsView_2.setScene(scene)
        # self.graphicsView_2.fitInView(item)  # 图像自适应

    # DFA到MFA的转换
    def mfa(self):
        t1 = []
        t2 = []
        for i in self.dictemp.keys():
            if 'y' in i:  # 区分终态集和非终态集    1：非终态集  0：终态集
                t1.append(self.dictemp[i])
            else:
                t2.append(self.dictemp[i])
            self.mfatemp['0'] = t1
            self.mfatemp['1'] = t2

        # self.mfatemp = {'0': ['A', 'C'], '1': ['S', 'B']}
        # self.dfalist = [['S', 'A', '0'], ['S', 'B', '1'], ['B', 'C', '0'], ['C', 'C', '0']]
        self.recursion_d()
        T = []
        for i, j in self.mfatemp.items():
            if len(j) == 0:
                T.append(i)
        for t in T:
            del self.mfatemp[t]
        self.Rmfa()

    # l:一个列表（状态转换表中的第一列中的值）
    # ch:输入字母表中的一个字母
    # 返回$_Closure(move(l，ch))
    def closure(self, l, ch):
        l1 = []
        # move(l,ch)
        for i in l:
            for j in self.nfalist:
                if j[0] == i and j[2] == ch:
                    l1.append(j[1])
        # $_Closure(move(l，ch))
        for i in l1:
            for j in self.nfalist:
                if i == j[0] and j[2] == '$':
                    l1.append(j[1])
        return list(set(l1))

    # 递归实现求状态转换表的$_Closure(move(l，ch))
    def recursion_c(self, listI):
        if self.dfacount < len(listI):
            valves = []
            for i in self.Input:
                t = self.closure(listI[self.dfacount], i)
                if t not in listI and len(t) != 0:
                    listI.append(t)
                valves.append(t)
            # 字典的键可以是数字、字符串、元组
            tu = tuple(listI[self.dfacount])
            self.dfadic[tu] = valves
            self.dfacount = self.dfacount + 1
            self.recursion_c(listI)

    # 递归实现求区分不同的不等价字迹
    def recursion_d(self):
        self.mfaflag = 1
        t = []
        for i in self.mfatemp.keys():
            if i != '0':  # 终态不用继续划分
                self.mfacount = self.mfacount + 1
                for j in self.mfatemp[i]:
                    for k in self.Input:
                        for l in self.dfalist:
                            if j == l[0] and k == l[2]:
                                if l[1] not in self.mfatemp[i]:
                                    t.append(l[0])
                                    self.mfatemp[i].remove(l[0])
                                    self.mfaflag = 0
                self.mfatemp[str(self.mfacount)] = t
                break
        if self.mfaflag == 0:
            self.recursion_d()

    # 生成self.mfa
    def Rmfa(self):
        self.mfalist.clear()
        l1 = []
        for i in self.mfatemp.keys():
            if 'S' in self.mfatemp[i]:
                l1.append('S')
            else:
                l1.append(self.mfatemp[i][0])
        for i in l1:
            for j in l1:
                for k in self.dfalist:
                    if i == k[0] and j == k[1]:
                        self.mfalist.append(k)

        # 图的可视化
        plt.figure()
        G = nx.DiGraph()
        start = []
        end = []
        edge_labels = []
        for i in self.mfalist:
            start.append(i[0])
            end.append(i[1])
            edge_labels.append(i[2])
        for i in range(len(start)):
            G.add_edges_from([(start[i], end[i], {'attr': str(edge_labels[i])})])
        edge_labels = nx.get_edge_attributes(G, 'attr')  # 获取边的name属性，
        nx.draw_networkx_edge_labels(G, pos=nx.spectral_layout(G), edge_labels=edge_labels,
                                     font_size=7)  # 将name属性，显示在边上
        nx.draw(G, with_labels=True, pos=nx.spectral_layout(G))
        plt.savefig("./file/MFA.jpg")

        # 显示图片
        frame = QImage("./file/MFA.jpg")
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.graphicsView_3.setScene(scene)
        # self.graphicsView_3.fitInView(item)  # 图像自适应
