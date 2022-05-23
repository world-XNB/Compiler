# -*- coding:utf-8 -*-
# @Time : 2022/5/6 20:41
# @Author : 西~南~北
# @File : MCGeneration.py
# @Software: PyCharm


# 中间代码生成器的实现类（包含语义分析-符号表的建立、静态语义检查）-------L-属性文法的自上而下的翻译
class MCG:
    def __init__(self):
        self.tochen = ['(102,int)', '(700,a)', '(219,=)', '(102,1)', '(303,;)', '(102,int)', '(700,sum)', '(201,()',
                       '(102,int)', '(304,,)', '(102,int)', '(202,))', '(303,;)', '(102,int)', '(700,max)', '(201,()',
                       '(102,int)', '(304,,)', '(102,int)', '(202,))', '(303,;)', '(119,main)', '(201,()', '(202,))',
                       '(301,{)', '(102,int)', '(700,N)', '(219,=)', '(700,read)', '(201,()', '(202,))', '(303,;)',
                       '(102,int)', '(700,M)', '(219,=)', '(700,read)', '(201,()', '(202,))', '(303,;)', '(700,a)',
                       '(219,=)', '(700,sum)', '(201,()', '(700,max)', '(201,()', '(700,M)', '(304,,)', '(700,N)',
                       '(202,))', '(304,,)', '(102,100)', '(202,))', '(303,;)', '(700,write)', '(201,()', '(700,a)',
                       '(202,))', '(303,;)', '(302,})', '(102,int)', '(700,sum)', '(201,()', '(102,int)', '(700,sum_x)',
                       '(304,,)', '(102,int)', '(700,sum_y)', '(202,))', '(301,{)', '(102,int)', '(700,result)',
                       '(303,;)', '(700,result)', '(219,=)', '(700,sum_x)', '(209,+)', '(700,sum_y)', '(303,;)',
                       '(106,return)', '(700,result)', '(303,;)', '(302,})', '(102,int)', '(700,max)', '(201,()',
                       '(102,int)', '(700,m_x)', '(304,,)', '(102,int)', '(700,m_y)', '(202,))', '(301,{)', '(102,int)',
                       '(700,result)', '(303,;)', '(111,if)', '(201,()', '(700,m_x)', '(214,>=)', '(700,m_y)',
                       '(202,))', '(700,result)', '(219,=)', '(700,m_x)', '(303,;)', '(112,else)', '(700,result)',
                       '(219,=)', '(700,m_y)', '(303,;)', '(106,return)', '(700,result)', '(303,;)', '(302,})']

        self.pos = -1  # 记录访问tochen的位置
        self.constTbale = []  # 常量表
        self.varTable = []  # 变量表
        self.funTable = []  # 函数表
        self.scopePath = 0  # 作用域路径

        self.NXQ = 0  # 中间代码的编号——指针
        self.T = 0  # 用来辅助产生临时变量
        self.Tvar = locals()  # locals以字典的形式返回当前函数运行环境下的所有局部变量
        self.ICT = []  # 中间代码表

        self.flagvar = 1  # 标志量，辅助多个声明变量的翻译

        self.P = []  # 辅助if语句因为else的多种情况

    # 回填函数
    def backpatch(self, p, t):
        for i in p:
            i["result"] = t

    # 合并函数
    def merge(self, p, p1):
        p.append(p1)

    # 语义函数——产生临时变量
    def newtemp(self):
        self.Tvar[f"T{self.T}"] = self.T
        self.T = self.T + 1

    # 语义函数——产生一条四元式
    def gencode(self, op, arg1, arg2, result):
        dir = {}
        dir["number"] = self.NXQ
        dir["op"] = op
        dir["arg1"] = arg1
        dir["arg2"] = arg2
        dir["result"] = result
        self.ICT.append(dir)
        self.NXQ = self.NXQ + 1

    # # 符号表插入操作
    def insert(self, L, D):
        for l in L:
            if l["name"] == D["name"]:
                print("语义错误，重复的" + l["name"])
                return
        L.append(D)

    # 获取下一个tochen串的种别码
    def getnexttochen(self):
        if self.pos < len(self.tochen) - 1:
            self.pos = self.pos + 1
            s = self.tochen[self.pos].split(',')
            return s[0].strip('(')
        else:
            self.pos = self.pos + 1
            return self.tochen[len(self.tochen) - 1].split(',')[0].strip('(')  # 返回最后一个种别码

    # 获取下一个tochen串的单词
    def getnextword(self):
        self.pos = self.pos - 1
        if self.pos < len(self.tochen) - 1:
            self.pos = self.pos + 1
            s = self.tochen[self.pos].split(',')
            return s[1].strip(')')
        else:
            self.pos = self.pos + 1
            return self.tochen[len(self.tochen) - 1].split(',')[1].strip(')')  # 返回最后一个种别码

    # 算术表达式~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++表达式部分++++++++++++++++++++++++++++++++
    def aexpr(self, S="default"):
        term1 = self.term(S)  # 处理乘除，取负和括号部分
        while True:
            string = self.getnexttochen()
            if string in ['209', '210']:  # //处理 +,-
                term2 = self.term()  # 处理 + - 之后的部分
                self.newtemp()
                if string == '209':
                    self.gencode('+', term1, term2, "T" + str(self.T - 1))
                else:
                    self.gencode('-', term1, term2, "T" + str(self.T - 1))
                return "T" + str(self.T - 1)
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                return term1

    # 处理乘除，取负和括号部分
    def term(self, S='default'):
        fac1 = self.factor(S)  # 处理因子
        while True:
            string = self.getnexttochen()
            if string in ['206', '207', '208']:  # 处理 * / %
                fac2 = self.factor()  # 递归调用，* / 之后跟随的另一个项
                self.newtemp()
                if string == '206':
                    self.gencode('*', fac1, fac2, "T" + str(self.T - 1))
                elif string == '207':
                    self.gencode('/', fac1, fac2, "T" + str(self.T - 1))
                else:
                    self.gencode('%', fac1, fac2, "T" + str(self.T - 1))
                return "T" + str(self.T - 1)
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                return fac1

    # 处理单个因子: 括号和单目取负、单个常量、变量
    def factor(self, S='default'):
        Str = self.getnexttochen()
        if Str == '201':  # 处理括号
            aex = self.aexpr(Str)  # 调用表达式的分析
            Str = self.getnexttochen()
            if Str != '202':
                print("ERROR，缺少 ） ")
            return aex
        elif Str == '-':  # 处理弹幕取负
            aex = self.aexpr(Str)

            self.newtemp()
            self.gencode('-', aex, ' ', "T" + str(self.T - 1))
            return "T" + str(self.T - 1)
        elif Str not in ['101', '102', '103', '400', '500', '600', '700', '800']:  # 单个常量、变量
            self.pos = self.pos - 1
            Str = self.getnextword()
            return Str
        elif Str == '700':
            if self.getnexttochen() == '201':  # 处理 ( ——函数调用
                self.pos = self.pos - 2
                func = self.funcall(S)  # 函数调用
                return func
            else:
                self.pos = self.pos - 1
                return self.getnextword()
        elif Str == '102':
            Str = self.getnextword()
            if Str == '"0"':
                return 0
            else:
                return int(self.getnextword())  # 此处因为默认程序中的数值都是整数
        else:
            return self.getnextword()

    # 布尔表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def bexpr(self):
        bt = self.boolt()  # 与的优先级大于或的优先级
        if self.pos == len(self.tochen) - 1:
            return bt
        orf = self.orfun(bt)
        return orf

    # 或运算
    def orfun(self, bt):
        if self.getnexttochen() == '218':
            bt1 = self.boolt()  # 布尔项

            self.newtemp()
            self.gencode('||', bt, bt1, 'T' + str(self.T - 1))
            self.orfun('T' + str(self.T - 1))
        else:
            self.pos = self.pos - 1
            return bt

    # 布尔项
    def boolt(self):
        bf = self.boolf()  # 布尔因子
        if self.pos == len(self.tochen) - 1:
            return bf
        andf = self.andfun(bf)
        return andf

    # 与运算
    def andfun(self, bf):
        if self.getnexttochen() == '217':
            bf1 = self.boolf()  # 布尔项

            self.newtemp()
            self.gencode('&&', bf, bf1, 'T' + str(self.T - 1))
            self.andfun('T' + str(self.T - 1))
        else:
            self.pos = self.pos - 1
            return bf

    # 处理布尔因子
    def boolf(self):
        Str = self.getnexttochen()
        if Str == '205':  # 处理非运算
            bex = self.bexpr()  # 处理 ! 之后的布尔表达式

            self.newtemp()
            self.gencode('!', bex, ' ', 'T' + str(self.T - 1))
            return 'T' + str(self.T - 1)
        else:
            self.pos = self.pos - 1
            midpos = self.pos
            aex = self.aexpr()  # 处理算术表达式
            if self.pos == len(self.tochen) - 1:
                return aex
            Str = self.getnexttochen()
            if Str in ['211', '212', '213', '214', '215', '216']:  # 关系表达式
                self.pos = midpos
                reg = self.regufun(aex)
                return reg
            else:
                self.pos = self.pos - 1
                return aex

    # 调用关系表达式部分
    def regufun(self, aex):
        # aex1 = self.aexpr()
        Str = self.getnexttochen()  # 匹配关系运算符
        if Str in ['211', '212', '213', '214', '215', '216']:
            word = self.getnextword()

            aex2 = self.aexpr()
            self.newtemp()
            self.gencode(word, aex, aex2, 'T' + str(self.T - 1))
            return 'T' + str(self.T - 1)

    # 赋值表达式部分~~~~~~~~~~~~~~~~~~~~~~~~
    def qexpr(self):
        Str1 = self.getnexttochen()
        word = self.getnextword()
        if Str1 == '700':  # 处理标识符
            Str2 = self.getnexttochen()
            if Str2 == '219':  # 处理 =
                ex = self.expr()
                self.gencode('=', ex, ' ', word)
            else:
                self.pos = self.pos - 1
                print("报错，不是赋值表达式")
        else:
            self.pos = self.pos - 1
            print("报错，不是赋值表达式")

    # 表达式~~~~~~~~~~~~~~~~~~~~~~~~
    def expr(self, S='default'):
        Str = self.getnexttochen()
        if Str == '205':  # 处理 ！——处理布尔表达式
            self.pos = self.pos - 1
            self.getnexttochen()  # 匹配 !
            bex = self.bexpr()

            self.newtemp()
            self.gencode('!', bex, ' ', 'T' + str(self.T - 1))
            return 'T' + str(self.T - 1)
        else:
            self.pos = self.pos - 1
            aex = self.aexpr(S)  # 处理算术表达式
            if self.getnexttochen() == '303':
                self.pos = self.pos - 1
                return aex
            else:
                self.pos = self.pos - 1
            exp = self.exprfun(aex)
            return exp

    # 调用表达式部分
    def exprfun(self, aex):
        str = self.getnexttochen()
        if str == '219':  # 处理 =(赋值运算符)
            self.pos = self.pos - 2
            self.qexpr()
        elif str in ['211', '212', '213', '214', '215', '216']:  # 处理关系运算符（关系表达式）
            self.pos = self.pos - 1
            midpos = self.pos
            reg = self.regufun(aex)
            if self.getnexttochen() in ['217', '218']:  # 处理 && ||
                self.pos = midpos
                bex = self.bexpr()
                return bex
            else:
                self.pos = self.pos - 1
                return reg
        elif str in ['217', '218']:  # 处理 && || （布尔表达式     ！不需要要处理，不存在一个算术表达式标后面跟 ！ ）
            self.pos = self.pos - 2
            bex = self.bexpr()
            return bex
        else:
            self.pos = self.pos - 1
            return aex

    # 声明语句~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++语句部分++++++++++++++++++++++++++++++++
    def dstat(self, funName="name"):
        str = self.getnexttochen()
        if str == '105':  # const
            self.pos = self.pos - 1
            self.vdecl(funName)  # 值声明
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
                        self.vdecl(funName)  # 值声明
                    else:
                        self.pos = self.pos - 1
                        print("报错，声明语句报错")
                else:
                    self.pos = self.pos - 1
                    print("报错，声明语句报错")
            else:
                self.pos = self.pos - 1

    # 值声明
    def vdecl(self, sp="name"):
        str = self.getnexttochen()
        self.pos = self.pos - 1
        if str == '105':  # 处理 const
            self.cdecl(sp)  # 常量声明
        else:
            self.vadecl(sp)  # 变量声明

    # 常量声明
    def cdecl(self, sp="name"):
        self.getnexttochen()  # 匹配 const
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # 匹配常量类型

            constdir = {}
            constdir["type"] = self.getnextword()  # 记录常量类型
            constdir["fName"] = sp
            self.cdtable(constdir)  # 常量声明表
        else:
            self.pos = self.pos - 1

    # 常量声明表
    def cdtable(self, constdir):
        name = self.getnexttochen()
        if name == '700':  # 标识符

            str = self.getnextword()
            constdir["name"] = str  # 记录常量名字

            str = self.getnexttochen()
            if str == '219':  # =
                str = self.getnexttochen()
                if str in ['101', '102', '103', '400', '500', '600', '800']:  # 常量
                    str = self.getnextword()
                    constdir["value"] = str  # 记录常量值
                    self.gencode('=', str, ' ', name)
                    # self.constTbale.append(constdir)
                    self.insert(self.constTbale, constdir)

                    str = self.getnexttochen()
                    if str == '303':  # ;
                        pass
                    elif str == '304':  # ，
                        self.cdtable(constdir)

    # 变量声明
    def vadecl(self, sp="name"):
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # 匹配变量类型
            vardir = {}
            vardir["SP"] = self.scopePath
            vardir["type"] = self.getnextword()
            vardir["fName"] = sp
            self.vdtable(vardir)

    # 变量声明表
    def vdtable(self, vardir):
        self.udecl(vardir)  # 单变量声明
        if self.pos == len(self.tochen) - 1:
            return
        str = self.getnexttochen()
        if str == '303':  # ;
            pass
        elif str == '304':  # ,
            v = vardir.copy()
            self.vdtable(v)  # 变量声明表

    # 单变量声明
    def udecl(self, vardir):
        Str = self.getnexttochen()
        if Str == '700':  # 匹配变量
            Str = self.getnextword()
            vardir["name"] = self.getnextword()
            flag = 0
            for var in self.varTable:
                if var["SP"] == self.scopePath and var["name"] == vardir["name"]:
                    flag = 1
                    print("重复声明变量 " + vardir["name"])
            if flag == 0:
                self.varTable.append(vardir)

            s = self.getnexttochen()
            if s == '219':
                exp = self.expr(Str)  # 表达式
                if exp != 'default':
                    self.gencode('=', exp, ' ', vardir["name"])
            else:
                self.pos = self.pos - 1
        else:
            self.pos = self.pos - 1

    # 函数声明
    def fdecl(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103', '107']:  # int char float void

            fundir = {}
            funtype = self.getnextword()
            fundir["type"] = funtype

            str = self.getnexttochen()
            if str == '700':  # 标识符
                funname = self.getnextword()
                fundir["name"] = funname
                str = self.getnexttochen()

                if str == '201':  # （
                    fdp = []  # 存储形参
                    self.fdplist(fundir, fdp)
                str = self.getnexttochen()  # 匹配 )
                if str == '202':
                    str = self.getnexttochen()  # 匹配 ;
                if str == '303':
                    pass
            else:
                self.pos = self.pos - 1

    # 函数声明形参列表
    def fdplist(self, fundir, fdp):
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # int float char
            f = self.getnextword()
            fdp.append(f)
            str = self.getnexttochen()
            if str == '304':
                self.fdplist(fundir, fdp)  # 函数声明形参列表
            else:
                fundir["parameter"] = fdp
                # self.funTable.append(fundir)
                self.insert(self.funTable, fundir)
        else:
            self.pos = self.pos - 1
            fundir["parameter"] = fdp
            # self.funTable.append(fundir)
            self.insert(self.funTable, fundir)

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
        self.getnexttochen()  # 判读数据处理语句类型
        str = self.getnexttochen()
        if str == '219':  # 赋值语句
            self.pos = self.pos - 2
            self.qexpr()  # 赋值表达式
            self.getnexttochen()  # 处理 ;
        elif str == '201':  # 函数调用语句
            self.pos = self.pos - 2
            self.funcall(S='default')  # 函数调用
            if self.getnexttochen() != 303:  # 处理 ;
                pass

    # 函数调用
    def funcall(self, S='default'):
        s = self.getnexttochen()
        if s == '700':  # 标识符
            Str = self.getnextword()
            s = self.getnexttochen()
            if s == '201':  # 处理 （
                self.funargu()  # 实参列表
                self.getnexttochen()  # 处理 ）
                self.newtemp()
                self.gencode('call', Str, ' ', "T" + str(self.T - 1))
                if (S != 'default'):
                    self.gencode('=', "T" + str(self.T - 1), ' ', S)
                    return 'default'
                else:
                    return "T" + str(self.T - 1)

    # 函数调用形参
    def funargu(self):
        aex = self.aexpr()  # 算术表达式
        if aex != "(":
            self.gencode('para', aex, ' ', ' ')
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

    # if 语句
    def ifstat(self):
        exp = self.iffun()
        str = self.getnexttochen()
        if str == '112':  # 处理 else
            self.backpatch(self.P, self.NXQ + 1)
            self.P = []

            p1 = []
            self.gencode('j', ' ', ' ', self.NXQ + 1)
            self.merge(p1, self.ICT[self.NXQ - 1])

            self.stat()  # 语句
            self.backpatch(p1, self.NXQ)

        else:
            self.P = []
            self.pos = self.pos - 1

    # 调用if语句
    def iffun(self):
        Str = self.getnexttochen()
        if Str == '111':  # 处理 if
            Str = self.getnexttochen()
            if Str == '201':  # 处理 （
                exp = self.expr()  # 表达式
                Str = self.getnexttochen()
                if Str == '202':  # 处理 ）
                    # p1 = []
                    self.gencode('jz', exp, ' ', "else")
                    self.merge(self.P, self.ICT[self.NXQ - 1])

                    self.stat()  # 语句

                    self.backpatch(self.P, self.NXQ)
                return exp

    # for 语句
    def forstat(self):
        Str = self.getnexttochen()
        if Str == '113':  # 处理 for
            if self.getnexttochen() == '201':  # 处理 （
                self.expr()  # 表达式
                if self.getnexttochen() == '303':
                    TEST = self.NXQ  # 表达式的入口代码
                    exp = self.expr()  # 表达式

                    p1 = []  # 真出口回填链
                    p2 = []  # 假出口回填链就
                    self.gencode('jz', exp, ' ', "NXQ")
                    self.merge(p2, self.ICT[self.NXQ - 1])
                    self.gencode('jnz', exp, ' ', "AGAIN")  # 需要回填
                    self.merge(p1, self.ICT[self.NXQ - 1])

                    if self.getnexttochen() == '303':
                        INC = self.NXQ  # 表达式的入口代码
                        self.expr()  # 表达式
                        self.gencode('j', ' ', ' ', TEST)
                        if self.getnexttochen() == '202':  # 处理 ）

                            AGAIN = self.NXQ
                            self.backpatch(p1, AGAIN)

                            self.loop()  # 循环语句
                            self.gencode('j', ' ', ' ', INC)
                            self.backpatch(p2, self.NXQ)

    # while 语句
    def whilestat(self):
        if self.getnexttochen() == '110':  # 处理 while
            if self.getnexttochen() == '201':  # 处理（
                start = self.NXQ
                exp = self.expr()  # 表达式
                p1 = []
                p2 = []
                if exp == 1:
                    self.gencode('jnz', exp, ' ', "AGAIN")  # 需要回填
                    self.merge(p1, self.ICT[self.NXQ - 1])
                else:
                    self.gencode('jz', exp, ' ', "NXQ")
                    self.merge(p2, self.ICT[self.NXQ - 1])

                if self.getnexttochen() == '202':  # 处理 ）
                    AGAIN = self.NXQ
                    self.backpatch(p1, AGAIN)
                    self.loop()  # 循环语句
                    self.gencode('j', ' ', ' ', start)
                    self.backpatch(p2, self.NXQ)

    # dowhile 语句
    def dowhilestat(self):
        if self.getnexttochen() == '109':  # 处理 do
            head = self.NXQ  # 记住入口
            self.loopcomstat()  # 循环用复合语句
            if self.getnexttochen() == '110':  # 处理 while
                if self.getnexttochen() == '201':  # 处理（
                    exp = self.expr()  # 表达式
                    if exp == 1:
                        self.gencode('jnz', exp, ' ', head)  # 真出口
                    else:
                        self.gencode('jz', exp, ' ', self.NXQ)  # 假出口

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
            self.breakstat()
        elif str == '108':  # contiue
            self.contiuestat()

    # break语句
    def breakstat(self):
        if self.getnexttochen() == '108':  # 处理 break
            self.getnexttochen()  # 处理 ;

    # contiue语句
    def contiuestat(self):
        if self.getnexttochen() == '108':  # 处理 contiue
            self.getnexttochen()  # 处理 ;

    # 循环用if语句
    def loopif(self):
        self.iffun()  # 循环if语句
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
            self.dpstat()  # 数据处理语句
        else:
            self.pos = self.pos - 1

    # 循环用复合语句
    def loopcomstat(self):
        if self.getnexttochen() == '301':  # 处理 {
            self.loopstattable()  # 循环语句表
            if self.getnexttochen() == '302':  # 处理 }
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
            if str != '303':  # 处理 ;
                self.pos = self.pos - 1
                exp = self.expr()
                self.gencode('ret', ' ', ' ', exp)
                self.gencode('ret', ' ', ' ', ' ')
                self.getnexttochen()  # 处理 ;

    # 复合语句
    def compoundstat(self, sp="main"):
        self.scopePath = self.scopePath + 1
        str = self.getnexttochen()
        if str == '301':  # 处理 {
            self.stable(sp)  # 语句表
            str = self.getnexttochen()  # 匹配 }
            if str != '302':
                print("报错，不合法的复合语句，缺少 }")
        self.scopePath = self.scopePath - 1

    # 语句表
    def stable(self, sp="name"):
        self.stat(sp)
        str = self.getnexttochen()
        if str in ['105', '101', '102', '103', '107', '111', '113', '110', '109', '106',
                   '301']:  # 声明语句、控制语句和复合语句
            self.pos = self.pos - 1
            self.stable()
        elif str == '700':  # 标识符
            if self.getnexttochen() in ['219', '201']:  # = （
                self.pos = self.pos - 2
                self.stable()
        elif str == '302':  # }
            self.pos = self.pos - 1

    # 语句
    def stat(self, sp="name"):
        str = self.getnexttochen()
        if str in ['105', '101', '102', '103', '107']:  # 声明语句
            self.pos = self.pos - 1
            self.dstat(sp)
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
            Str = self.getnexttochen()
            if Str == '700':  # 标识符
                funName = self.getnextword()
                # self.pos = self.pos - 1
                Str = self.getnextword()
                self.gencode(Str, ' ', ' ', ' ')
                if self.getnexttochen() == '201':  # 处理 (
                    if self.getnexttochen() in ['101', '102', '103']:  # 函数变量
                        self.pos = self.pos - 1
                        self.fundp(funName)  # 函数定义形参
                if self.getnexttochen() == '202':  # 匹配 ）
                    self.compoundstat(Str)  # 复合语句

    # 函数定义形参
    def fundp(self, funName):
        self.scopePath = 0
        vardic = {}
        vardic['SP'] = self.scopePath
        if self.getnexttochen() in ['101', '102', '103']:  # 函数变量
            t = self.getnextword()
            vardic['type'] = t
            if self.getnexttochen() == '700':  # 标识符
                name = self.getnextword()
                vardic['name'] = name
                vardic['fName'] = funName
                self.varTable.append(vardic)
                if self.getnexttochen() == '304':  # 匹配 ,
                    self.fundp(funName)  # 函数定义形参
                else:
                    self.pos = self.pos - 1

    # 程序~~~~~~~~~~~~~~~~~~~~~~~~++++++++++++++++++++++++++++++++程序部分++++++++++++++++++++++++++++++++
    def pro(self):
        if self.flagvar == 1:
            self.gencode("main", ' ', ' ', ' ')
            self.flagvar = 0
        self.dstat("global")  # 声明语句
        Str = self.getnexttochen()
        if Str == '119':  # 匹配 main
            if self.getnexttochen() == '201':  # 匹配 (
                if self.getnexttochen() == '202':  # 匹配 )
                    self.compoundstat("main")  # 复合语句
                    self.gencode("sys", ' ', ' ', ' ')
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


def fun():
    mcg = MCG()
    mcg.pro()
    print("常量表：" + str(mcg.constTbale))
    print("函数表：" + str(mcg.funTable))
    print("变量表：" + str(mcg.varTable))
    print(mcg.ICT)
    # for i in mcg.ICT:
    #     print(i)
    if mcg.pos == len(mcg.tochen) - 1:
        print("正确程序")
    else:
        print("错误程序")


# 测试临时变量是否可以生成
def fun1():
    mcg = MCG()
    mcg.newtemp()
    mcg.newtemp()
    mcg.Tvar["T1"] = mcg.Tvar["T1"] + 1
    print(mcg.Tvar["T" + str(mcg.T - 1)])


if __name__ == '__main__':
    fun()
