# -*- coding:utf-8 -*-
# @Time : 2022/3/8 16:51
# @Author : 西~南~北
# @File : Lex.py 本文件为此法分析部分
# @Software: PyCharm


class Lex:
    def __init__(self):
        self.word = ''
        # 'integer': 整数, 'character': 字符, 'charstr': 字符串, 'identifier': 标识符', 'realnum': 实数（float） sample语言单词的种别码
        self.sample = {'char': 101, 'int': 102, 'float': 103, 'break': 104, 'const': 105, 'return': 106, 'void': 107,
                       'continue': 108, 'do': 109, 'while': 110, 'if': 111, 'else': 112, 'for': 113, '{': 301, '}': 302,
                       ';': 303, ',': 304, 'integer': 400, 'character': 500, 'charstr': 600, 'identifier': 700,
                       'realnum': 800, '(': 201, ')': 202, '[': 203, ']': 204, '!': 205, '*': 206, '/': 207, '%': 208,
                       '+': 209, '-': 210, '<': 211, '<=': 212, '>': 213, '>=': 214, '==': 215, '!=': 216, '&&': 217,
                       '||': 218, '=': 219, '.': 220}
        self.tochen = []

    # 识别整数
    def Idenint(self, words):
        self.word = words
        flag = 0
        # 判断十进制整数
        if self.word[0].isdigit() and self.word[0] != '0':
            if self.word.isdigit():
                self.specileCode('integer', self.word)
                return '这个单词是十进制整数'
            else:
                return '这不是一个正确单词'
        elif self.word[0] == '0':
            # 判断八进制整数
            if self.word[1] in ['0', '1', '2', '3', '4', '5', '6', '7']:
                for i in range(len(self.word) - 2):
                    if self.word[i + 2] not in ['0', '1', '2', '3', '4', '5', '6', '7']:
                        flag = 1
                if flag == 1:
                    flag = 0
                    self.specileCode('integer', self.word)
                    return '这是八进制整数'
                else:
                    return '这不是一个正确单词'
            elif self.word[1] in ['X', 'x']:
                for i in range(len(self.word) - 2):
                    if self.word[i + 2] not in ['0', '1', '2', '3', '4', '5', '6', '7', 'a', 'b', 'c', 'd', 'e', 'f',
                                                'A', 'B', 'C', 'D', 'E', 'F']:
                        flag = 1
                if flag == 1:
                    self.specileCode('integer', self.word)
                    return '这不是十六进制整数'
                else:
                    return '这不是一个正确单词'

    # 识别标识符
    def Ideniden(self, words):
        self.word = words
        flag = 0
        print(self.word)
        if self.word[0].isalpha() or self.word[0] in ['_']:
            for i in range(len(self.word) - 2):
                if self.word[i + 2].isalpha() or self.word[i + 2].isdigit():
                    flag = 0
                else:
                    flag = 1
            if flag == 1:
                return '这不是一个正确单词'
            else:
                self.specileCode('identifier', self.word)
                return '这不是一个正确单词'

    # 功能函数：判别标识符/整数
    def fun(self, words):
        self.word = words
        if self.word[0].isdigit():
            return self.Idenint(self.word)
        else:
            return self.Ideniden(self.word)

    # 识别种别码 t:类别    w:单词
    def specileCode(self, t, w):
        # 转换为二元形式
        s = '(' + str(self.sample[t]) + ', "' + w + '" )'
        self.tochen.append(s)
        return self.tochen


if __name__ == '__main__':
    lex = Lex()
    # 测试整数
    # lex.Idenint('0x1')
    # lex.Idenint('0x1g')
    # lex.Idenint('02')
    # lex.Idenint('02a')
    # lex.Idenint('21ad')
    # 测试标识符
    # lex.Ideniden('_world1')
    # lex.Ideniden('world_1')
    # lex.Ideniden('1_wworld')
    # lex.Ideniden('a_ww@rld')

    # 输出二元式

    lex.fun('ab')
    print(lex.tochen)
