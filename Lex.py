# -*- coding:utf-8 -*-
# @Time : 2022/3/16 16:32
# @Author : 西~南~北
# @File : Test.py
# @Software: PyCharm


class Lex:
    def __init__(self):
        # 'integer': 整数, 'character': 字符, 'charstr': 字符串, 'identifier': 标识符', 'realnum': 实数（float） sample语言单词的种别码
        self.sample = {'char': 101, 'int': 102, 'float': 103, 'break': 104, 'const': 105, 'return': 106, 'void': 107,
                       'continue': 108, 'do': 109, 'while': 110, 'if': 111, 'else': 112, 'for': 113, 'string': 114,
                       '{': 301, '}': 302, ';': 303, ',': 304, 'integer': 400, 'character': 500, 'charstr': 600,
                       'identifier': 700, 'realnum': 800, '(': 201, ')': 202, '[': 203, ']': 204, '!': 205, '*': 206,
                       '/': 207, '%': 208, '+': 209, '-': 210, '<': 211, '<=': 212, '>': 213, '>=': 214, '==': 215,
                       '!=': 216, '&&': 217, '||': 218, '=': 219, '.': 220, '++': 221, '+=': 222, '--': 223, '-=': 224}
        self.tochen = []  # 最终输出的tochen串
        self.data = []
        self.flag = 0  # 多行注释标志
        self.error = 0  # 错误标志
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
                        self.flagword = 1
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

                    elif line[i] >= '0' and line[i] <= '7':
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
                    self.error = 1
                    self.a = i
                    i = i + 1
                    while line[i] != '\n':
                        while line[i] != '\'':
                            i = i + 1
                            self.error = 0
                            self.flagword = 1
                        break
                    i = i + 1
                    self.b = i
                    self.cut(line, 500)

                # 判断字符串常数
                elif line[i] in ['\"']:
                    self.error = 1
                    self.a = i
                    i = i + 1
                    while line[i] != '\n':
                        while line[i] != '\"':
                            i = i + 1
                            self.error = 0
                            self.flagword = 1
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
                    # 界符
                    elif line[i] in ['{', '}', ';', ',']:
                        self.tochen.append('(' + str(self.sample[line[i]]) + ',' + line[i] + ')')
                        i = i + 1
                    # 其他
                    else:
                        self.tochen.append('第' + str(self.data.index(line) + 1) + '行有不合法的单词')
                        while line[i] not in [' ', '\n', '\t']:
                            i = i + 1
