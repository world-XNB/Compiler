# -*- coding:utf-8 -*-
# @Time : 2022/4/3 14:28
# @Author : 西~南~北
# @File : Parser.py
# @Software: PyCharm

import os

import tkinter as tk
from tkinter import filedialog


# LL1的实现类
class LL1:
    def __init__(self):
        self.grammer = {}  # 用字典存储文法,键——开始符号  值——产生式（'$'——ε(发音：伊普西隆)）
        self.temp = []  # 用于消除在求非终结符A的后随符号集时的递归

    # 读取文法文件，初始化grammer
    def openfile(self):
        root = tk.Tk()
        root.withdraw()
        # 获取文件夹路径
        f_path = filedialog.askopenfilename()
        f = open(f_path, 'r', encoding='utf-8')
        with f:
            data = f.readlines()

            for line in data:  # 逐行操作
                l = []
                values = []
                key = None
                for i in range(3, len(line)):  # 处理候选式
                    if line[1] != '-' and line[2] != '>':
                        print("不是文法！")
                        return
                    key = line[0]
                    if line[i] not in ['|', '\n']:
                        l.append(line[i])
                    elif line[i] in ['|', '\n']:
                        l1 = l.copy()
                        values.append(l1)
                        l.clear()
                if len(values) > 1:
                    self.grammer[key] = values
                else:
                    self.grammer[key] = l1

    # 判断文法是否为LL(1)文法
    def judge(self):
        # 不含左递归
        for g in self.grammer.keys():
            for i in self.grammer[g]:
                if g == i[0]:
                    print("该文发有左递归!")
                    return False
                break
            break

        # 每个非终结符A的各个候选式的首终结符集两两不想交
        for key in self.grammer.keys():
            if type(self.grammer[key][0]) == list:  # 多个候选式
                for p1 in self.grammer[key]:
                    for p2 in self.grammer[key]:
                        if p1 != p2:
                            if len(list(set(self.PFirst(key, p1)) & set(self.PFirst(key, p2)))) > 0:  # 判断是否有交集
                                print("每个非终结符A的各个候选式的首终结符集不符合两两不想交!")
                                return False

        # 如果非终结符A的某个候选式的首终结符包含$，则First(A)交Follow(A)为空集
        for key in self.grammer.keys():
            for l in self.grammer[key]:
                if type(self.grammer[key][0]) == list:  # 多个候选式
                    if '$' in self.PFirst(key, l):
                        self.temp.clear()
                        if len(list(set(self.First(key)) & set(self.Follow(key)))) > 0:  # 判断是否有交集
                            print("如果非终结符A的某个候选式的首终结符包含$，则First(A)交Follow(A)不为为空集")
                            return False

        return True

    # 求非终结符A的首终结符集
    def First(self, A):
        first = []  # 存储非终结符A的首终结符集
        for key in self.grammer.keys():
            if A == key:
                if type(self.grammer[key][0]) == list:  # 区分候选式多个与一个（处理方式不同）
                    for i in self.grammer[A]:
                        if i[0].islower():
                            first.append(i[0])
                        elif i[0].isupper():
                            first.extend(self.First(i[0]))
                        else:
                            first.append(i[0])
                else:
                    if self.grammer[A][0].islower():
                        first.append(self.grammer[A][0])
                    elif self.grammer[A][0].isupper():
                        first.extend(self.First(self.grammer[A][0]))
                    else:
                        first.append(self.grammer[A][0])
        return list(set(first))

    # 求非终结符A的各个候选式list的首终结符集
    def PFirst(self, A, L):
        pfirst = []
        for key in self.grammer.keys():
            if A == key:
                if type(self.grammer[key][0]) == list:  # 候选式有多个
                    for l in self.grammer[key]:
                        if L == l:
                            if l[0].isupper() == False:  # 终结符
                                pfirst.append(l[0])
                            else:
                                pfirst.extend(self.First(l[0]))
                elif L == self.grammer[key]:  # 候选式只有一个
                    if L[0].isupper() == False:
                        pfirst.append(L[0])
                    else:
                        pfirst.extend(self.First(L[0]))
                else:
                    print("没有找到该候选式！")

        return list(set(pfirst))

    # 求非终结符A的后随符号集  调用该函数记得清空self.temp
    def Follow(self, A):
        self.temp.append(A)
        follow = []  # 存储非终结符A的后随符号集
        if A == list(self.grammer.keys())[0]:  # 如果A是开始符号
            follow.append('#')

        flag = 0  # 用于判断A在哪一对键值对
        for key in self.grammer.keys():
            # 判断A在哪一对键值对里面
            if type(self.grammer[key][0]) == list:  # 区分候选式多个与一个（处理方式不同）
                for i in self.grammer[key]:
                    if A in i:
                        flag = 1  # 1——A在self.grammer[key[0]]
                        break
            else:
                if A in self.grammer[key]:
                    flag = 2  # 2——A在self.grammer[key]

            if flag == 1:  # 候选式多个list
                flag = 0
                for val in self.grammer[key]:
                    for i in range(len(val)):
                        if val[i] == A:
                            if i + 1 < len(val):
                                if val[i + 1].isupper() == False:  # B->aAa
                                    follow.append(val[i + 1])
                                    break
                                elif val[i + 1].isupper():  # B->aAXa
                                    if '$' in self.First(val[i + 1]):  # B->aAβ且β*->ε
                                        follow.extend(self.Follow(val[i + 1]))
                                    f = []
                                    for j in self.First(val[i + 1]):
                                        if j != '$':
                                            f.append(j)
                                    follow.extend(f)
                            else:  # B->aA,
                                if key != A and key not in self.temp:
                                    follow.extend(self.Follow(key))
            elif flag == 2:  # 候选式一个list
                flag = 0
                for i in range(len(self.grammer[key])):
                    if self.grammer[key][i] == A:
                        if i + 1 < len(self.grammer[key]):
                            if self.grammer[key][i + 1].isupper() == False:  # B->aAa
                                follow.append(self.grammer[key][i + 1])
                                break
                            elif self.grammer[key][i + 1].isupper():  # B->aAXa
                                if '$' in self.First(self.grammer[key][i + 1]):  # B->aAβ且β*->ε
                                    follow.extend(self.Follow(self.grammer[key][i + 1]))
                                f = []
                                for j in self.First(self.grammer[key][i + 1]):
                                    if j != '$':
                                        f.append(j)
                                follow.extend(f)
                        else:  # B->aA
                            if key != A and key not in self.temp:
                                follow.extend(self.Follow(key))
            elif flag == 0:  # 该键值对没有非终结符A
                continue
        return list(set(follow))


# 语法分析器的实现类
class Parser:
    def __init__(self):
        # self.tochen = ['(201,"(")', '(700,"e")', '(210,"-")', '(700,"f")', '(206,"*")', '(700,"a")', '(202,")")',
        #                '(209,"+")', '(700,"b")', '(209,"+")', '(700,"c")', '(206,"*")', '(700,"d")']  # 测试算术表达式

        # self.tochen = ['(700,"a")', '(217,"&&")', '(700,"b")']  # 测试布尔表达式——&&
        # self.tochen = ['(700,"a")', '(217,"&&")', '(700,"b")', '(218,"||")', '(700,"c")']  # 测试布尔表达式——||
        # self.tochen = ['(205,"!")', '(700,"c")', '(217,"&&")', '(700,"b")', '(218,"||")', '(700,"a")']  # 测试布尔表达式——！

        # self.tochen = ['(700,"a")', '(213,">")', '(700,"b")']  # 测量关系表达式

        # self.tochen = ['(700,"a")', '(213,">")', '(700,"b")', '(217,"&&")', '(700,"b")']  # 测试布尔表达式——&&
        # self.tochen = ['(205,"!")', '(700,"c")''(700,"a")', '(213,">")', '(700,"b")', '(217,"&&")',
        #                '(700,"b")']  # 测试布尔表达式包含关系表达式

        # self.tochen = ['(700,"a")', '(219,"=")', '(700,"b")']  # 测试赋值表达式
        self.tochen = ['(700,"a")', '(219,"=")', '(201,"(")', '(700,"e")', '(210,"-")', '(700,"f")', '(206,"*")',
                       '(700,"a")', '(202,")")', '(209,"+")', '(700,"b")', '(209,"+")', '(700,"c")', '(206,"*")',
                       '(700,"d")']  # 测试赋值表达式

        self.pos = -1  # 记录访问tochen的位置

    # 获取下一个tochen串的种别码
    def getnexttochen(self):
        if self.pos < len(self.tochen) - 1:
            self.pos = self.pos + 1
            s = self.tochen[self.pos].split(',')
            return s[0].strip('(')
        else:
            self.pos = self.pos + 1
            return self.tochen[len(self.tochen) - 1].split(',')[0].strip('(')  # 返回最后一个种别码

    # 算术表达式（状态转换图实现）~~~~~~~~~~~~~~~~~~~~~~~~
    def aexpr(self):
        self.pos = self.pos - 1  # 单独调试算术表达式时要注释此行代码
        str = self.getnexttochen()
        self.term()  # 处理乘除，取负和括号部分
        while True:
            str = self.getnexttochen()
            if str in ['209', '210']:  # //处理 +,-
                str = self.getnexttochen()
                self.term()  # 处理 + - 之后的部分
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 处理乘除，取负和括号部分
    def term(self):
        self.pos = self.pos - 1
        str = self.getnexttochen()
        self.factor()  # 处理因子
        while True:
            str = self.getnexttochen()
            if str in ['206', '207']:  # 处理 * /
                str = self.getnexttochen()
                self.factor()  # 递归调用，* / 之后跟随的另一个项
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 处理单个因子: 括号和单目取负、单个常量、变量
    def factor(self):
        self.pos = self.pos - 1
        str = self.getnexttochen()
        if str == '201':  # 处理括号
            str = self.getnexttochen()
            self.aexpr()  # 调用表达式的分析
            str = self.getnexttochen()
            if str != '202':
                print("ERROR，缺少 ） ")
        elif str == '-':  # 处理弹幕取负
            str = self.getnexttochen()
            self.aexpr()
        elif str not in ['101', '102', '103', '400', '500', '600', '700', '800']:  # 单个常量、变量
            print("ERROR,语法错误")

    # 布尔表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def bexpr(self):
        self.pos = self.pos - 1  # 单独调试布尔表达式需要注释此行
        str = self.getnexttochen()
        self.andt()
        if self.pos == len(self.tochen) - 1:
            return
        self.boolt()

    # 布尔项
    def boolt(self):
        self.pos = self.pos - 1
        str = self.getnexttochen()
        self.andt()  # 处理与运算部分
        while True:
            str = self.getnexttochen()
            if str == '218':  # //处理||
                str = self.getnexttochen()
                self.andt()  # 处理 ||之后的部分
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 调用处理与运算部分
    def andt(self):
        self.boolf()
        if self.pos == len(self.tochen) - 1:
            return
        self.andfun()

    # 处理布尔因子
    def boolf(self):
        self.pos = self.pos - 1
        str = self.getnexttochen()
        if str == '205':  # 处理非运算
            self.bexpr()  # 处理 ! 之后的布尔表达式
        else:
            self.aexpr()  # 处理算术表达式
            if self.pos == len(self.tochen) - 1:
                return
            self.regufun()

    # 处理与运算部分
    def andfun(self):
        self.pos = self.pos - 1
        str = self.getnexttochen()
        self.boolf()  # 处理布尔因子部分
        while True:
            str = self.getnexttochen()
            if str == '217':  # //处理&&
                str = self.getnexttochen()
                self.boolf()  # 处理 && 之后的部分
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 调用关系表达式部分
    def regufun(self):
        # self.pos = self.pos - 1
        str = self.getnexttochen()
        if str in ['211', '212', '213', '214', '215', '216']:
            str = self.getnexttochen()
            self.aexpr()

    # 赋值表达式部分~~~~~~~~~~~~~~~~~~~~~~~~
    def qexpr(self):
        self.pos = self.pos - 1  # 单独调试赋值表达式要注释掉此行
        str = self.getnexttochen()
        if str == '700':
            str = self.getnexttochen()
            if str == '219':
                self.expr()
            else:
                print("报错，不是赋值表达式")
        else:
            print("报错，不是赋值表达式")

    # 表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def expr(self):
        str = self.getnexttochen()
        if str == '205':  # 处理 ！——处理布尔表达式
            str = self.getnexttochen()
            self.bexpr()
        else:
            self.aexpr()  # 处理算术表达式
            if self.pos == len(self.tochen) - 1:
                return
            self.exprfun()

    # 调用表达式部分
    def exprfun(self):
        str = self.getnexttochen()
        if str == '219':  # 处理 =(赋值运算符)
            self.pos = self.pos - 1
            self.qexpr()
        elif str in ['211', '212', '213', '214', '215', '216']:  # 处理关系运算符（关系表达式）
            self.pos = self.pos - 1
            self.bexpr()
        elif str in ['217', '218']:  # 处理 && || （布尔表达式     ！不需要要处理，不存在一个算术表达式标后面跟 ！ ）
            self.pos = self.pos - 1
            self.bexpr()
        else:
            print("报错，表达式报错")


def ll1():
    l = LL1()
    l.openfile()
    print(l.judge())


def fun():
    parser = Parser()
    parser.expr()
    if parser.pos == len(parser.tochen) - 1:
        print("正确表达式")
    else:
        print("错误表达式")


if __name__ == '__main__':
    fun()
