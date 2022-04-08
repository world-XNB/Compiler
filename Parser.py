# -*- coding:utf-8 -*-
# @Time : 2022/4/3 14:28
# @Author : 西~南~北
# @File : Parser.py
# @Software: PyCharm

import os

from PyQt5.QtWidgets import QFileDialog


# 语法分析器的实现类
class Parser:
    def __init__(self):
        # self.grammer = {}  # 用字典存储文法,键——开始符号  值——产生式（'$'——ε(发音：伊普西隆)）
        self.grammer = {'P': ['b', 'T', 'd'],
                        'T': ['S', 'F'],
                        'F': [[';', 'S', 'F'], ['$']],
                        'S': [['N'], ['C']],
                        'N': ['a'],
                        'C': ['I', 'D'],
                        'D': [['e', 'S'], ['$']],
                        'I': ['Z', 'N'],
                        'Z': ['i', 'c', 't']
                        }  # 用字典存储文法
        self.temp = []  # 用于消除在求非终结符A的后随符号集时的递归

    # 读取文法文件，初始化grammer
    def openfile(self):
        fname = QFileDialog.getOpenFileName("open file", '.')
        path = fname[0]  # 记录绝对路径，后面保存要用
        if fname[0]:
            f = open(path, 'r', encoding='utf-8')
            with f:
                data = f.readlines()
                strdata = ''
                for i in data:
                    strdata = strdata + str(data.index(i) + 1) + "\t" + i

    # 判断文法是否为LL(1)文法
    def judge(self):
        # 不含左递归
        for g in self.grammer.keys():
            for i in self.grammer[g]:
                if g == i[0]:
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
                                return False

        # 如果非终结符A的某个候选式的首终结符包含$，则First(A)交Follow(A)为空集
        for key in self.grammer.keys():
            for l in self.grammer[key]:
                if type(self.grammer[key][0]) == list:  # 多个候选式
                    if '$' in self.PFirst(key, l):
                        self.temp.clear()
                        if len(list(set(self.First(key)) & set(self.Follow(key)))) > 0:  # 判断是否有交集
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


if __name__ == '__main__':
    par = Parser()
    par.openfile()
    print(par.judge())
