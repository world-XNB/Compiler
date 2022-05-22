# -*- coding:utf-8 -*-
# @Time : 2022/5/20 21:17
# @Author : 西~南~北
# @File : OCGeneration.py
# @Software: PyCharm

class OCG:
    def __init__(self):
        # 中间代码生成器输出的中间代码表
        self.MCG = [{'number': 0, 'op': 'main', 'arg1': ' ', 'arg2': ' ', 'result': ' '},
                    {'number': 1, 'op': '=', 'arg1': 1, 'arg2': ' ', 'result': 'a'},
                    {'number': 2, 'op': 'call', 'arg1': 'read', 'arg2': ' ', 'result': 'T0'},
                    {'number': 3, 'op': '=', 'arg1': 'T0', 'arg2': ' ', 'result': 'N'},
                    {'number': 4, 'op': 'call', 'arg1': 'read', 'arg2': ' ', 'result': 'T1'},
                    {'number': 5, 'op': '=', 'arg1': 'T1', 'arg2': ' ', 'result': 'M'},
                    {'number': 6, 'op': '>=', 'arg1': 'M', 'arg2': 'N', 'result': 'T2'},
                    {'number': 7, 'op': 'jz', 'arg1': 'T2', 'arg2': ' ', 'result': 9},
                    {'number': 8, 'op': '=', 'arg1': 'M', 'arg2': ' ', 'result': 'result'},
                    {'number': 9, 'op': 'j', 'arg1': ' ', 'arg2': ' ', 'result': 11},
                    {'number': 10, 'op': '=', 'arg1': 'N', 'arg2': ' ', 'result': 'result'},
                    {'number': 11, 'op': '+', 'arg1': 'result', 'arg2': 100, 'result': 'T3'},
                    {'number': 12, 'op': '=', 'arg1': 'T3', 'arg2': ' ', 'result': 'a'},
                    {'number': 13, 'op': 'para', 'arg1': 'a', 'arg2': ' ', 'result': ' '},
                    {'number': 14, 'op': 'call', 'arg1': 'write', 'arg2': ' ', 'result': 'T4'},
                    {'number': 15, 'op': 'sys', 'arg1': ' ', 'arg2': ' ', 'result': ' '}]

        self.pos = 0  # 中间代码翻译的位置标志
        # 常量表
        self.constTbale = []
        # 变量表
        self.varTable = [{'SP': 0, 'type': 'int', 'fName': 'global', 'name': 'a'},
                         {'SP': 1, 'type': 'int', 'fName': 'main', 'name': 'result'},
                         {'SP': 1, 'type': 'int', 'fName': 'name', 'name': 'N'},
                         {'SP': 1, 'type': 'int', 'fName': 'name', 'name': 'M'}]

        # 函数表
        self.funTable = []
        # 汇编代码
        self.ASM = []

    # 目标代码生成函数
    def target(self):
        for mcg in self.MCG:
            if mcg["op"] == 'main':
                pass
            elif mcg["op"] == '=':
                self.funEqual()
            elif mcg["op"] == '+':
                self.funAdd()
            elif mcg["op"] == '-':
                self.funSub()
            elif mcg["op"] == '*':
                self.funMul()
            elif mcg["op"] == '/':
                self.funDiv()
            elif mcg["op"] == '%':
                self.funSur()
            elif mcg["op"] == '<':
                self.funLess()
            elif mcg["op"] == '>=':
                self.funGOE()
            elif mcg["op"] == '>':
                self.funGreater()
            elif mcg["op"] == '<=':
                self.funLOE()
            elif mcg["op"] == '==':
                self.funEE()
            elif mcg["op"] == '!=':
                self.funNE()
            elif mcg["op"] == '&&':
                self.funAnd()
            elif mcg["op"] == '||':
                self.funOr()
            elif mcg["op"] == '!':
                self.funNot()
            elif mcg["op"] == 'j':
                self.funj()
            elif mcg["op"] == 'jz':
                self.funjz()
            elif mcg["op"] == 'jnz':
                self.funjnz()
            elif mcg["op"] == 'para':
                self.funpara()
            elif mcg["op"] == 'call':
                self.funcall()
            elif mcg["op"] == 'ret':
                if mcg["result"] != ' ':
                    self.funret()
                else:
                    self.funretA()
            else:  # 函数调用
                self.funfun()
            self.pos = self.pos + 1

    # 判断judge应该在内存哪一个区域
    def judgeVC(self, judge):
        if type(judge) == int:
            return str(judge)
        else:
            if judge[0] == 'T':
                return str("es[" + str(judge.strip('T')) + "]")
            else:
                for i in self.varTable:
                    if i["name"] == judge:
                        return str("ds[_" + str(judge) + "]")
                for i in self.varTable:
                    if i["name"] == judge:
                        return str("ds[_" + str(judge) + "]")

    # =
    def funEqual(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # +
    def funAdd(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("add ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # -
    def funSub(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("sub ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # *
    def funMul(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov bx," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("mul bx")
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # /
    def funDiv(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov dx,0")
        self.ASM.append("mov bx," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("div bx")
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # %
    def funSur(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov dx,0")
        self.ASM.append("mov bx," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("div bx")
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",dx")

    # <
    def funLess(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("jb _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # >=
    def funGOE(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("jnb _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # >
    def funGreater(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("ja _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # <=
    def funLOE(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("jna _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # ==
    def funEE(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("je _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # !=
    def funNE(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("jne _" + str(self.pos) + "_n")
        self.ASM.append("mov dx,0")
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tmov " + self.judgeVC(
            self.MCG[self.pos]["result"]) + ",dx")

    # &&
    def funAnd(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,0")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _and")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _and")
        self.ASM.append("mov dx,1")
        self.ASM.append("_and" + ":\tmov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",dx")

    # ||
    def funOr(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("jne _or")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg2"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("jne _or")
        self.ASM.append("mov dx,0")
        self.ASM.append("_or" + ":\tmov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",dx")

    # !
    def funNot(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov dx,1")
        self.ASM.append("mov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _not")
        self.ASM.append("mov dx,0")
        self.ASM.append("_not" + ":\tmov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",dx")

    # j
    def funj(self):
        self.ASM.append("jmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))

    # jz
    def funjz(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _ne")
        self.ASM.append("jmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))
        self.ASM.append("_ne" + ":\tnop")

    # jnz
    def funjnz(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _ez")
        self.ASM.append("jmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))
        self.ASM.append("_ez" + ":\tnop")

    # para
    def funpara(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("push ax")

    # call
    def funcall(self):
        self.ASM.append("_" + str(self.pos) + ":\tcall " + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # ret---A
    def funretA(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov sp,bp")
        self.ASM.append("pop bp")
        self.ASM.append("ret")

    # ret
    def funret(self):
        self.ASM.append("mov sp,bp")
        self.ASM.append("pop bp")
        self.ASM.append("ret")

    # fun
    def funfun(self):
        self.ASM.append("push bp")
        self.ASM.append("move bp,sp")
        self.ASM.append("sub sp")


if __name__ == '__main__':
    ocg = OCG()
    ocg.target()
    print(ocg.ASM)
