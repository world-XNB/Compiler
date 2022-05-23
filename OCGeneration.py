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
                    {'number': 4, 'op': 'para', 'arg1': 3, 'arg2': ' ', 'result': ' '},
                    {'number': 5, 'op': 'para', 'arg1': 4, 'arg2': ' ', 'result': ' '},
                    {'number': 6, 'op': 'call', 'arg1': 'sum', 'arg2': ' ', 'result': 'T1'},
                    {'number': 7, 'op': 'para', 'arg1': 'T1', 'arg2': ' ', 'result': ' '},
                    {'number': 8, 'op': 'para', 'arg1': 'N', 'arg2': ' ', 'result': ' '},
                    {'number': 9, 'op': 'call', 'arg1': 'sum', 'arg2': ' ', 'result': 'T2'},
                    {'number': 10, 'op': '=', 'arg1': 'T2', 'arg2': ' ', 'result': 'a'},
                    {'number': 11, 'op': 'para', 'arg1': 'a', 'arg2': ' ', 'result': ' '},
                    {'number': 12, 'op': 'call', 'arg1': 'write', 'arg2': ' ', 'result': 'T3'},
                    {'number': 13, 'op': 'sys', 'arg1': ' ', 'arg2': ' ', 'result': ' '},
                    {'number': 14, 'op': 'sum', 'arg1': ' ', 'arg2': ' ', 'result': ' '},
                    {'number': 15, 'op': '+', 'arg1': 'sum_x', 'arg2': 'sum_y', 'result': 'T4'},
                    {'number': 16, 'op': '=', 'arg1': 'T4', 'arg2': ' ', 'result': 'result'},
                    {'number': 17, 'op': 'ret', 'arg1': ' ', 'arg2': ' ', 'result': 'result'},
                    {'number': 18, 'op': 'ret', 'arg1': ' ', 'arg2': ' ', 'result': ' '}]

        self.pos = 0  # 中间代码翻译的位置标志
        # 常量表
        self.constTbale = []
        # 变量表
        self.varTable = [{'SP': 0, 'type': 'int', 'fName': 'global', 'name': 'a'},
                         {'SP': 1, 'type': 'int', 'fName': 'main', 'name': 'N'},
                         {'SP': 0, 'type': 'int', 'name': 'sum_x', 'fName': 'sum'},
                         {'SP': 0, 'type': 'int', 'name': 'sum_y', 'fName': 'sum'},
                         {'SP': 1, 'type': 'int', 'fName': 'sum', 'name': 'result'}]

        # 函数表
        self.funTable = [{'type': 'int', 'name': 'sum', 'parameter': ['int', 'int']}]
        # 汇编代码
        self.ASM = ['assume cs:code,ds:data,ss:stack,es:extended',
                    'extended segment',
                    '\tdb 1024 dup (0)',
                    'extended ends',
                    'stack segment',
                    '\tdb 1024 dup (0)',
                    'stack ends',
                    'data segment',
                    '\t_buff_p db 256 dup (24h)',
                    '\t_buff_s db 256 dup (0)',
                    '\t_msg_p db 0ah,\'Output:\',0',
                    '_msg_s db 0ah,\'Input:\',0']

    # 初始化目标代码
    def ASMinint(self):
        for i in self.varTable:
            self.ASM.append("\t_" + i["name"] + " dw 0")
        for i in self.constTbale:
            self.ASM.append("\t_" + i["name"] + " dw 0")

        self.ASM.append('data ends')
        self.ASM.append('code segment')
        self.ASM.append('start:\tmov ax,extended')
        self.ASM.append('\tmov es,ax')
        self.ASM.append('\tmov ax,stack')
        self.ASM.append('\tmov ss,ax')
        self.ASM.append('\tmov sp,1024')
        self.ASM.append('\tmov bp,sp')
        self.ASM.append('\tmov ax,data')
        self.ASM.append('\tmov ds,ax')

    # 汇编代码最后部分（read,write）
    def ASMend(self):
        self.ASM.append('\n\n复制添加read,write的位置\n\n')
        self.ASM.append('code ends')
        self.ASM.append('end start')

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
                    self.funretA()
                else:
                    self.funret()
            elif mcg["op"] == 'sys':
                self.ASM.append('quit:\tmov ah,4ch')
                self.ASM.append('\tint 21h')
            else:
                for fun in self.funTable:  # 函数调用
                    if mcg["op"] == fun["name"]:
                        self.funfun()
            self.pos = self.pos + 1

    # 判断judge应该在内存哪一个区域
    def judgeVC(self, judge):
        if type(judge) == int:
            return str(judge)
        else:
            if judge[0] == 'T':
                return str("es:[" + str(int(judge.strip('T')) * 2) + "]")
            else:
                if judge in ['read', 'write']:
                    return str(judge)
                for i in self.varTable:
                    if i["name"] == judge:
                        return str("ds:[_" + str(judge) + "]")
                for i in self.constTbale:
                    if i["name"] == judge:
                        return str("ds:[_" + str(judge) + "]")
                for i in self.funTable:
                    if i["name"] == judge:
                        return str(judge)

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
        self.ASM.append("_" + str(self.pos) + ":\tjmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))

    # jz
    def funjz(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("jne _" + str(self.pos) + "_n")
        self.ASM.append("jmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tnop")

    # jnz
    def funjnz(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("cmp ax,0")
        self.ASM.append("je _" + str(self.pos) + "_n")
        self.ASM.append("jmp far ptr _" + self.judgeVC(self.MCG[self.pos]["result"]))
        self.ASM.append("_" + str(self.pos) + "_n" + ":\tnop")

    # para
    def funpara(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("push ax")

    # call
    def funcall(self):
        self.ASM.append("_" + str(self.pos) + ":\tcall _" + self.judgeVC(self.MCG[self.pos]["arg1"]))
        self.ASM.append("mov " + self.judgeVC(self.MCG[self.pos]["result"]) + ",ax")

    # ret---A
    def funretA(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov ax," + self.judgeVC(self.MCG[self.pos]["result"]))
        self.ASM.append("mov sp,bp")
        self.ASM.append("pop bp")
        self.ASM.append("ret")

    # ret
    def funret(self):
        self.ASM.append("_" + str(self.pos) + ":\tmov sp,bp")
        self.ASM.append("pop bp")
        self.ASM.append("ret")

    # fun
    def funfun(self):
        self.ASM.append("_" + str(self.MCG[self.pos]["op"]) + ":\tpush bp")
        self.ASM.append("mov bp,sp")
        self.ASM.append("sub sp,2")


if __name__ == '__main__':
    ocg = OCG()
    ocg.ASMinint()
    ocg.target()
    ocg.ASMend()
    for i in ocg.ASM:
        print(i)
