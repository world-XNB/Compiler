# -*- coding:utf-8 -*-
# @Time : 2022/5/6 20:41
# @Author : 西~南~北
# @File : MCGeneration.py
# @Software: PyCharm

# 中间代码生成器的实现类（包含语义分析-符号表的建立、静态语义检查）-------L-属性文法的自上而下的翻译
class MCG:
    def __init__(self):
        self.tochen = ['(105,const)', '(102,int)', '(700,a_global)', '(219,=)', '(102,2)', '(303,;)', '(105,const)',
                       '(102,int)', '(700,b_global)', '(219,=)', '(102,3)', '(303,;)', '(102,int)', '(700,fun1)',
                       '(201,()', '(202,))', '(303,;)', '(102,int)', '(700,fun2)', '(201,()', '(102,int)', '(304,,)',
                       '(102,int)', '(202,))', '(303,;)', '(102,int)', '(700,fun3)', '(201,()', '(102,int)', '(304,,)',
                       '(103,float)', '(202,))', '(303,;)', '(102,int)', '(700,a)', '(219,=)', '(102,1)', '(303,;)',
                       '(119,main)', '(201,()', '(202,))', '(301,{)', '(102,int)', '(700,a)', '(219,=)', '(102,2)',
                       '(303,;)', '(102,int)', '(700,b)', '(219,=)', '(102,3)', '(303,;)', '(102,int)', '(700,a)',
                       '(219,=)', '(102,2)', '(303,;)', '(106,return)', '(102,1)', '(303,;)', '(302,})']

        self.pos = -1  # 记录访问tochen的位置
        self.constTbale = []  # 常量表
        self.varTable = []  # 变量表

        self.funTable = []  # 函数表
        self.scopePath = 0  # 作用域路径

    # 将常量插入常量表
    def InsertConst(self, id):
        dir = {}
        for con in self.constTbale:
            if con["name"] == id:
                print("语义错误，常量" + id + "的重复声明")
                return
            dir["entry"] = len(self.constTbale) + 1  # 记录入口
            dir["name"] = id
            self.constTbale.append(dir)

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
    def aexpr(self):
        self.term()  # 处理乘除，取负和括号部分
        while True:
            str = self.getnexttochen()
            if str in ['209', '210']:  # //处理 +,-
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
                self.factor()  # 递归调用，* / 之后跟随的另一个项
            else:
                self.pos = self.pos - 1  # 退回当前取出的token字
                break

    # 处理单个因子: 括号和单目取负、单个常量、变量
    def factor(self):
        str = self.getnexttochen()
        if str == '201':  # 处理括号
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
            self.getnexttochen()  # 匹配 !
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
        self.getnexttochen()  # 匹配 const
        str = self.getnexttochen()
        if str in ['101', '102', '103']:  # 匹配常量类型
            self.cdtable()  # 常量声明表
        else:
            self.pos = self.pos - 1

    # 常量声明表
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
            self.vdtable()  # 变量声明表

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

    # 函数声明
    def fdecl(self):
        str = self.getnexttochen()
        if str in ['101', '102', '103', '107']:  # int char float void
            str = self.getnexttochen()
            if str == '700':  # 标识符
                str = self.getnexttochen()
                if str == '201':  # （
                    fdp = []  # 存储形参
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
                self.fdplist()  # 函数声明形参列表
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
        self.getnexttochen()  # 判读数据处理语句类型
        str = self.getnexttochen()
        if str == '219':  # 赋值语句
            self.pos = self.pos - 2
            self.qexpr()  # 赋值表达式
            self.getnexttochen()  # 处理 ;
        elif str == '201':  # 函数调用语句
            self.pos = self.pos - 2
            self.funcall()  # 函数调用
            if self.getnexttochen() != 303:  # 处理 ;
                pass

    # 函数调用
    def funcall(self):
        str = self.getnexttochen()
        if str == '700':  # 标识符
            str = self.getnexttochen()
            if str == '201':  # 处理 （
                self.funargu()  # 实参列表
                self.getnexttochen()  # 处理 ）

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

    # if 语句
    def ifstat(self):
        self.iffun()
        str = self.getnexttochen()
        if str == '112':  # 处理 else
            self.stat()  # 语句
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
                self.expr()  # 表达式
                if self.getnexttochen() == '303':
                    self.expr()  # 表达式
                    if self.getnexttochen() == '303':
                        self.expr()  # 表达式
                        if self.getnexttochen() == '202':  # 处理 ）
                            self.loop()  # 循环语句

    # while 语句
    def whilestat(self):
        if self.getnexttochen() == '110':  # 处理 while
            if self.getnexttochen() == '201':  # 处理（
                self.expr()  # 表达式
                if self.getnexttochen() == '202':  # 处理 ）
                    self.loop()  # 循环语句

    # dowhile 语句
    def dowhilestat(self):
        if self.getnexttochen() == '109':  # 处理 do
            self.loopcomstat()  # 循环用复合语句
            if self.getnexttochen() == '110':  # 处理 while
                if self.getnexttochen() == '201':  # 处理（
                    self.expr()  # 表达式
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
                self.expr()
                self.getnexttochen()  # 处理 ;

    # 复合语句
    def compoundstat(self):
        self.scopePath = self.scopePath + 1
        str = self.getnexttochen()
        if str == '301':  # 处理 {
            self.stable()  # 语句表
            str = self.getnexttochen()  # 匹配 }
            if str != '302':
                print("报错，不合法的复合语句，缺少 }")
        self.scopePath = self.scopePath - 1

    # 语句表
    def stable(self):
        self.stat()
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
                    self.compoundstat()  # 复合语句

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


def fun():
    mcg = MCG()
    mcg.pro()
    print(mcg.constTbale)
    print(mcg.funTable)
    print(mcg.varTable)
    if mcg.pos == len(mcg.tochen) - 1:
        print("正确程序")
    else:
        print("错误程序")


if __name__ == '__main__':
    fun()
