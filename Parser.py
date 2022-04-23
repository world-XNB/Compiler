# -*- coding:utf-8 -*-
# @Time : 2022/4/3 14:28
# @Author : 西~南~北
# @File : Parser.py
# @Software: PyCharm

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
        # self.tochen = ['(700,"a")', '(219,"=")', '(201,"(")', '(700,"e")', '(210,"-")', '(700,"f")', '(206,"*")',
        #                '(700,"a")', '(202,")")', '(209,"+")', '(700,"b")', '(209,"+")', '(700,"c")', '(206,"*")',
        #                '(700,"d")']  # 测试赋值表达式

        # self.tochen = ['(105,"const")', '(102,"int")', '(700,"a")', '(219,"=")', '(400,"10")', '(304,",")', '(700,"c")',
        #                '(219,"=")', '(400,"20")', '(303,";")']  # 测试值声明语句
        # self.tochen = ['(102,"int")', '(700,"fun")', '(201,"(")', '(102,"int")', '(700,"a")', '(202,")")',
        #                '(303,";")']  # 测试值声明语句

        # self.tochen = ['(700,"a")', '(219,"=")', '(700,"b")', '(303,";")']  # 测试赋值语句
        # self.tochen = ['(700,"a")', '(219,"=")', '(201,"(")', '(700,"e")', '(210,"-")', '(700,"f")', '(206,"*")',
        #                '(700,"a")', '(202,")")', '(209,"+")', '(700,"b")', '(209,"+")', '(700,"c")', '(206,"*")',
        #                '(700,"d")', '(303,";")']  # 测试赋值语句

        # self.tochen = ['(111,"if")', '(201,()', '(700,"a")', '(213,>)', '(700,"b")', '(202,))', '(700,"a")', '(219,=)',
        #                '(700,"a")', '(209,+)', '(700,"b")', '(303,;)']  # 测量控制语句 if

        # self.tochen = ['(111,"if")', '(201,()', '(700,"a")', '(213,>)', '(700,"b")', '(202,))', '(301,{)', '(700,"a")',
        #                '(219,=)', '(700,"a")', '(209,+)', '(700,"b")', '(303,;)', '(700,"a")', '(219,=)', '(700,"a")',
        #                '(210,-)', '(700,"b")', '(303,;)', '(302,})']  # 测量控制语句 if

        # self.tochen = ['(113,"for")', '(201,()', '(700,"a")', '(303,;)', '(700,"a")', '(303,;)', '(700,"a")', '(202,))',
        #                '(102,"int")', '(700,"a")', '(303,;)']  # 测量控制语句 for
        # self.tochen = ['(110,"while")', '(201,()', '(102,"1")', '(202,))', '(301,{)', '(700,"a")', '(219,=)',
        #                '(700,"a")', '(209,+)', '(700,"b")', '(303,;)', '(302,})']  # 测量控制语句 while
        # self.tochen = ['(109,"do")', '(301,{)', '(111,"if")', '(201,()', '(700,"a")', '(213,>)', '(700,"b")', '(202,))',
        #                '(700,"a")', '(219,=)', '(700,"a")', '(209,+)', '(700,"b")', '(303,;)', '(700,"a")', '(219,=)',
        #                '(700,"a")', '(210,-)', '(700,"b")', '(303,;)', '(302,})', '(110,"while")', '(201,()',
        #                '(700,"a")', '(202,))', '(303,;)']       # 测量控制语句 do while
        self.tochen = ['(102,"int")', '(700,"comp")', '(201,()', '(102,"int")', '(304,,)', '(102,"int")', '(202,))',
                       '(303,;)', '(119,"main")', '(201,()', '(202,))', '(301,{)', '(102,"int")', '(700,"m")',
                       '(304,,)', '(700,"k")', '(304,,)', '(700,"result")', '(303,;)', '(700,"m")', '(219,=)',
                       '(700,"read")', '(201,()', '(202,))', '(303,;)', '(700,"k")', '(219,=)', '(700,"read")',
                       '(201,()', '(202,))', '(303,;)', '(700,"result")', '(219,=)', '(700,"comp")', '(201,()',
                       '(700,"m")', '(304,,)', '(700,"k")', '(202,))', '(303,;)', '(700,"write")', '(201,()',
                       '(700,"result")', '(202,))', '(303,;)', '(302,})', '(102,"int")', '(700,"comp")', '(201,()',
                       '(102,"int")', '(700,"n")', '(304,,)', '(102,"int")', '(700,"i")', '(202,))', '(301,{)',
                       '(102,"int")', '(700,"a")', '(304,,)', '(700,"b")', '(303,;)', '(111,"if")', '(201,()',
                       '(700,"n")', '(215,"==")', '(700,"i")', '(218,"||")', '(700,"i")', '(215,"==")', '(102,"0")',
                       '(202,))', '(301,{)', '(106,"return")', '(102,"1")', '(303,;)', '(302,})', '(700,"a")',
                       '(219,=)', '(700,"comp")', '(201,()', '(700,"n")', '(210,-)', '(102,"1")', '(304,,)',
                       '(700,"i")', '(202,))', '(303,;)', '(700,"b")', '(219,=)', '(700,"comp")', '(201,()',
                       '(700,"n")', '(210,-)', '(102,"1")', '(304,,)', '(700,"i")', '(210,-)', '(102,"1")', '(202,))',
                       '(303,;)', '(106,"return")', '(700,"a")', '(209,+)', '(700,"b")', '(303,;)']

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

    # 算术表达式~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++表达式部分++++++++++++++++++++++++++++++++
    def aexpr(self):
        self.term()  # 处理乘除，取负和括号部分
        while True:
            str = self.getnexttochen()
            if str in ['209', '210']:  # //处理 +,-
                # str = self.getnexttochen()
                self.term()  # 处理 + - 之后的部分
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 处理乘除，取负和括号部分
    def term(self):
        self.factor()  # 处理因子
        while True:
            str = self.getnexttochen()
            if str in ['206', '207', '208']:  # 处理 * / %
                # str = self.getnexttochen()
                self.factor()  # 递归调用，* / 之后跟随的另一个项
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 处理单个因子: 括号和单目取负、单个常量、变量
    def factor(self):
        str = self.getnexttochen()
        if str == '201':  # 处理括号
            # self.getnexttochen()
            self.aexpr()  # 调用表达式的分析
            str = self.getnexttochen()
            if str != '202':
                print("ERROR，缺少 ） ")
        elif str == '-':  # 处理弹幕取负
            self.aexpr()
        elif str not in ['101', '102', '103', '400', '500', '600', '700', '800']:  # 单个常量、变量
            self.pos = self.pos - 1
        elif str == '700':
            if self.getnexttochen() == '201':  # 处理 ( ——函数调用
                self.pos = self.pos - 2
                self.funcall()  # 函数调用
            else:
                self.pos = self.pos - 1

    # 布尔表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def bexpr(self):
        self.boolt()  # 与的优先级大于或的优先级
        if self.pos == len(self.tochen) - 1:
            return
        self.orfun()

    # 或运算
    def orfun(self):
        if self.getnexttochen() == '218':
            self.boolt()  # 布尔项
            self.orfun()
        else:
            self.pos = self.pos - 1

    # 布尔项
    def boolt(self):
        self.boolf()  # 布尔因子
        if self.pos == len(self.tochen) - 1:
            return
        self.andfun()

    # 与运算
    def andfun(self):
        if self.getnexttochen() == '217':
            self.boolf()  # 布尔项
            self.andfun()
        else:
            self.pos = self.pos - 1

    # 处理布尔因子
    def boolf(self):
        str = self.getnexttochen()
        if str == '205':  # 处理非运算
            self.bexpr()  # 处理 ! 之后的布尔表达式
        else:
            self.pos = self.pos - 1
            midpos = self.pos
            self.aexpr()  # 处理算术表达式
            if self.pos == len(self.tochen) - 1:
                return
            str = self.getnexttochen()
            if str in ['211', '212', '213', '214', '215', '216']:  # 关系表达式
                self.pos = midpos
                self.regufun()
            else:
                self.pos = self.pos - 1

    # 调用关系表达式部分
    def regufun(self):
        self.aexpr()
        str = self.getnexttochen()  # 匹配关系运算符
        if str in ['211', '212', '213', '214', '215', '216']:
            self.aexpr()

    # 赋值表达式部分~~~~~~~~~~~~~~~~~~~~~~~~
    def qexpr(self):
        str = self.getnexttochen()
        if str == '700':  # 处理标识符
            str = self.getnexttochen()
            if str == '219':  # 处理 =
                self.expr()
            else:
                self.pos = self.pos - 1
                print("报错，不是赋值表达式")
        else:
            self.pos = self.pos - 1
            print("报错，不是赋值表达式")

    # 表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def expr(self):
        str = self.getnexttochen()
        if str == '205':  # 处理 ！——处理布尔表达式
            self.pos = self.pos - 1
            self.getnexttochen()  # 匹配#
            self.bexpr()
        else:
            self.pos = self.pos - 1
            self.aexpr()  # 处理算术表达式
            if self.pos == len(self.tochen) - 1:
                return
            self.exprfun()

    # 调用表达式部分
    def exprfun(self):
        str = self.getnexttochen()
        if str == '219':  # 处理 =(赋值运算符)
            self.pos = self.pos - 2
            self.qexpr()
        elif str in ['211', '212', '213', '214', '215', '216']:  # 处理关系运算符（关系表达式）
            self.pos = self.pos - 2
            midpos = self.pos
            self.regufun()
            if self.getnexttochen() in ['217', '218']:  # 处理 && ||
                self.pos = midpos
                self.bexpr()
            else:
                self.pos = self.pos - 1
        elif str in ['217', '218']:  # 处理 && || （布尔表达式     ！不需要要处理，不存在一个算术表达式标后面跟 ！ ）
            self.pos = self.pos - 2
            self.bexpr()
        else:
            self.pos = self.pos - 1

    # 声明语句~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++语句部分++++++++++++++++++++++++++++++++
    def dstat(self):
        str = self.getnexttochen()
        if str == '105':  # const
            self.pos = self.pos - 1
            self.vdecl()  # 值声明
        elif str == '107':  # void
            self.pos = self.pos - 1
            self.fdecl()  # 函数声明
        else:
            if str in ['101', '102', '103']:  # int char float
                str = self.getnexttochen()
                if str == '700':  # 标识符/变量
                    str = self.getnexttochen()
                    if str == '201':  # (
                        self.pos = self.pos - 3
                        self.fdecl()  # 函数声明
                    elif str in ['219', '303', '304']:
                        self.pos = self.pos - 3
                        self.vdecl()  # 值声明
                    else:
                        self.pos = self.pos - 1
                        print("报错，声明语句报错")
                else:
                    self.pos = self.pos - 1
                    print("报错，声明语句报错")
            else:
                self.pos = self.pos - 1

    # 值声明
    def vdecl(self):
        str = self.getnexttochen()
        self.pos = self.pos - 1
        if str == '105':  # 处理 const
            self.cdecl()  # 常量声明
        else:
            self.vadecl()  # 变量声明

    # 常量声明
    def cdecl(self):
        str = self.getnexttochen()  # 匹配 const
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # 匹配常量类型
            self.cdtable()  # 常量声母表
        else:
            self.pos = self.pos - 1
            print("报错，常量声明错误")

    # 常量声母表
    def cdtable(self):
        str = self.getnexttochen()
        if str == '700':  # 标识符
            str = self.getnexttochen()
            if str == '219':  # =
                str = self.getnexttochen()
                if str in ['101', '102', '103', '400', '500', '600', '800']:  # 常量
                    str = self.getnexttochen()
                    if str == '303':  # ;
                        pass
                    elif str == '304':  # ，
                        self.cdtable()
                    else:
                        self.pos = self.pos - 1
                        print("报错，常量声明报错")
                else:
                    self.pos = self.pos - 1
                    print("报错，常量声明报错")
            else:
                self.pos = self.pos - 1
                print("报错，常量声明报错")
        else:
            self.pos = self.pos - 1
            print("报错，常量声明报错")

    # 变量声明
    def vadecl(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # 匹配变量类型
            self.vdtable()

    # 变量声明表
    def vdtable(self):
        self.udecl()  # 单变量声明
        if self.pos == len(self.tochen) - 1:
            return
        str = self.getnexttochen()
        if str == '303':  # ;
            pass
        elif str == '304':  # ,
            self.vdtable()  # 常量声明表

    # 单变量声明
    def udecl(self):
        str = self.getnexttochen()
        if str == '700':  # 匹配变量
            str = self.getnexttochen()
            if str == '219':
                self.expr()  # 表达式
            else:
                self.pos = self.pos - 1
        else:
            self.pos = self.pos - 1
            print("报错，变量声明报错")

    # 函数声明
    def fdecl(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103', '107']:  # int char float void
            str = self.getnexttochen()
            if str == '700':  # 标识符
                str = self.getnexttochen()
                if str == '201':  # （
                    self.fdplist()
                str = self.getnexttochen()  # 匹配 )
                if str == '202':
                    str = self.getnexttochen()  # 匹配 ;
                if str == '303':
                    pass
            else:
                self.pos = self.pos - 1

    # 函数声明形参列表
    def fdplist(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # int float char
            str = self.getnexttochen()
            if str == '304':
                self.fdplist()
        else:
            self.pos = self.pos - 1

    # 执行语句~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++
    def estat(self):
        str = self.getnexttochen()
        if str in ['111', '113', '110', '109', '106']:  # 控制语句
            self.pos = self.pos - 1
            self.contaolstat()  # 控制语句
        elif str == '301':
            self.pos = self.pos - 1
            self.compoundstat()  # 复合语句
        elif str == '700':  # 标识符
            if self.getnexttochen() in ['219', '201']:  # = （
                self.pos = self.pos - 2
                self.dpstat()  # 数据处理语句

    # 数据处理语句
    def dpstat(self):
        str = self.getnexttochen()
        str = self.getnexttochen()
        if str == '219':  # 赋值语句
            self.pos = self.pos - 2
            self.qexpr()  # 赋值表达式
            str = self.getnexttochen()  # 处理 ;
        elif str == '201':  # 函数调用语句
            self.pos = self.pos - 2
            self.funcall()  # 函数调用
            str = self.getnexttochen()  # 处理 ;

    # 函数调用语句
    def funcall(self):
        str = self.getnexttochen()
        if str == '700':  # 标识符
            str = self.getnexttochen()
            if str == '201':  # 处理 （
                self.funargu()  # 实参列表
                str = self.getnexttochen()
                if str != '202':  # 处理 ）
                    print("报错，缺少 )")
            else:
                print("报错，不是合法的函数调用")
        else:
            print("报错，不是合法的函数调用")

    # 函数调用形参
    def funargu(self):
        self.aexpr()  # 算术表达式
        str = self.getnexttochen()
        if str == '304':  # 处理多个形参
            self.funargu()
        else:
            self.pos = self.pos - 1

    # 控制语句
    def contaolstat(self):
        str = self.getnexttochen()
        self.pos = self.pos - 1
        if str == '111':  # if
            self.ifstat()
        elif str == '113':  # for
            self.forstat()
        elif str == '110':  # while
            self.whilestat()
        elif str == '106':  # return
            self.returnstat()
        elif str == '109':  # dowhile
            self.dowhilestat()
        else:
            print("报错，不合法的控制语句")

    # if 语句
    def ifstat(self):
        self.iffun()
        str = self.getnexttochen()
        if str == '112':  # 处理 else
            self.stat()
        else:
            self.pos = self.pos - 1

    # 调用if语句
    def iffun(self):
        str = self.getnexttochen()
        if str == '111':  # 处理 if
            str = self.getnexttochen()
            if str == '201':  # 处理 （
                self.expr()  # 表达式
                str = self.getnexttochen()
                if str == '202':  # 处理 ）
                    self.stat()  # 语句

    # for 语句
    def forstat(self):
        str = self.getnexttochen()
        if str == '113':  # 处理 for
            if self.getnexttochen() == '201':
                self.expr()
                if self.getnexttochen() == '303':
                    self.expr()
                    if self.getnexttochen() == '303':
                        self.expr()
                        if self.getnexttochen() == '202':  # 处理 ）
                            self.loop()  # 循环语句

    # while 语句
    def whilestat(self):
        if self.getnexttochen() == '110':  # 处理 while
            if self.getnexttochen() == '201':  # 处理（
                self.expr()
                if self.getnexttochen() == '202':  # 处理 ）
                    self.loop()  # 循环语句

    # dowhile 语句
    def dowhilestat(self):
        if self.getnexttochen() == '109':  # 处理 do
            self.loopcomstat()  # 循环用复合语句
            if self.getnexttochen() == '110':  # 处理 while
                if self.getnexttochen() == '201':  # 处理（
                    self.expr()
                    if self.getnexttochen() == '202':  # 处理 ）
                        if self.getnexttochen() == '303':  # 处理 ;
                            pass

    # 循环执行语句
    def loopestat(self):
        str = self.getnexttochen()
        self.pos = self.pos - 1
        if str == '111':  # if
            self.loopif()  # 循环用if语句
        elif str == '113':  # for
            self.forstat()
        elif str == '110':  # while
            self.whilestat()
        elif str == '106':  # return
            self.returnstat()
        elif str == '109':  # dowhile
            self.dowhilestat()
        elif str == '104':  # break
            str = self.getnexttochen()  # ;
        elif str == '108':  # contiue
            str = self.getnexttochen()  # ;

    # 循环用if语句
    def loopif(self):
        self.iffun()
        str = self.getnexttochen()
        if str == '112':  # 处理 else
            self.loop()  # 循环语句
        else:
            self.pos = self.pos - 1

    # 调用循环if语句
    def loopiffun(self):
        if self.getnexttochen() == '111':  # 处理 if
            if self.getnexttochen() == '201':  # 处理 （
                self.expr()  # 表达式
                str = self.getnexttochen()
                if str == '202':  # 处理 ）
                    self.loop()  # 循环语句

    # 循环语句
    def loop(self):
        str = self.getnexttochen()
        if str in ['105', '101', '102', '103', '107']:
            self.pos = self.pos - 1
            self.dstat()  # 声明语句
        elif str in ['111', '113', '110', '106', '109', '104', '108']:
            self.pos = self.pos - 1
            self.loopestat()  # 循环执行语句
        elif str == '301':  # 处理 {
            self.pos = self.pos - 1
            self.loopcomstat()  # 循环用复合语句
        elif str == '700':
            self.pos = self.pos - 1
            self.dpstat()
        else:
            self.pos = self.pos - 1

    # 循环用复合语句
    def loopcomstat(self):
        if self.getnexttochen() == '301':
            self.loopstattable()  # 循环语句表
            if self.getnexttochen() == '302':
                pass

    # 循环语句表
    def loopstattable(self):
        self.loop()  # 循环语句
        if self.getnexttochen() != '302':
            self.pos = self.pos - 1
            self.loopstattable()  # 循环语句表
        else:
            self.pos = self.pos - 1

    # return 语句
    def returnstat(self):
        str = self.getnexttochen()
        if str == '106':
            str = self.getnexttochen()
            if str != '303':
                self.pos = self.pos - 1
                self.expr()
                str = self.getnexttochen()

    # 复合语句
    def compoundstat(self):
        str = self.getnexttochen()
        if str == '301':  # 处理 {
            self.stable()  # 语句表
            str = self.getnexttochen()  # 匹配 }
            if str != '302':
                print("报错，不合法的复合语句，缺少 }")

    # 语句表
    def stable(self):
        self.stat()
        str = self.getnexttochen()
        if str in ['105', '101', '102', '103', '107', '111', '113', '110', '109', '106',
                   '301']:  # 声明语句、控制语句和符合语句
            self.pos = self.pos - 1
            self.stable()
        elif str == '700':  # 标识符
            if self.getnexttochen() in ['219', '201']:  # = （
                self.pos = self.pos - 2
                self.stable()
        elif str == '302':  # }
            self.pos = self.pos - 1

    # 语句
    def stat(self):
        str = self.getnexttochen()
        if str in ['105', '101', '102', '103', '107']:  # 声明语句
            self.pos = self.pos - 1
            self.dstat()
        elif str in ['111', '113', '110', '109', '106', '301']:  # 控制语句和复合语句
            self.pos = self.pos - 1
            self.estat()  # 执行语句
        elif str == '700':  # 标识符
            if self.getnexttochen() in ['219', '201']:  # = （
                self.pos = self.pos - 2
                self.estat()  # 执行语句

    # 函数定义~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++函数部分++++++++++++++++++++++++++++++++
    def fundef(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103', '107']:  # 函数类型
            if self.getnexttochen() == '700':  # 标识符
                if self.getnexttochen() == '201':  # 处理 (
                    if self.getnexttochen() in ['101', '102', '103']:  # 函数变量
                        self.pos = self.pos - 1
                        self.fundp()  # 函数定义形参
                if self.getnexttochen() == '202':  # 匹配 ）
                    self.compoundstat()  # 符合语句

    # 函数定义形参
    def fundp(self):
        if self.getnexttochen() in ['101', '102', '103']:  # 函数变量
            if self.getnexttochen() == '700':  # 标识符
                if self.getnexttochen() == '304':  # 匹配 ,
                    self.fundp()  # 函数定义形参
                else:
                    self.pos = self.pos - 1

    # 程序~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++程序部分++++++++++++++++++++++++++++++++
    def pro(self):
        self.dstat()  # 声明语句
        str = self.getnexttochen()
        if str == '119':  # 匹配 main
            if self.getnexttochen() == '201':  # 匹配 (
                if self.getnexttochen() == '202':  # 匹配 )
                    self.compoundstat()  # 复合语句
                    self.funblock()
        else:
            self.pos = self.pos - 1
            self.pro()

    # 函数快
    def funblock(self):
        if self.getnexttochen() in ['101', '102', '103', '107']:  # 函数类型
            self.pos = self.pos - 1
            self.fundef()  # 函数定义
            self.funblock()  # 函数块
        else:
            self.pos = self.pos - 1


def ll1():
    l = LL1()
    l.openfile()
    print(l.judge())


def fun():
    parser = Parser()
    parser.pro()
    if parser.pos == len(parser.tochen) - 1:
        print("正确程序")
    else:
        print("错误程序")


if __name__ == '__main__':
    fun()
