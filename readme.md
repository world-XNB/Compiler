# 西南北编译器

## 文件介绍

1. .ui 文件都是由Qtdesigner生成，然后通过pyUIC自动生成相应的.py文件
2. 该系统的启动文件：main.py
3. mainGUI.py：主界面文件
4. aboutGUI.py：关于界面文件
5. helpGUI：帮助界面文件
6. dfaGUI：DFA界面文件
7. lex.py：词法分析器的实现文件
8. Paser.py：语法分析器的实现文件

## 文件夹介绍

file文件夹里面为编译器编译过程中的中间图片或者资料图片

1. 种别码.jpg 是sample语言的种别码（注：本编译系统针对的是sample语言，然后在此基础上有所增加一些结构，所以此处的种别码和lex.py文件中的self.sample不太一样）  
2. 词法分析状态转换图.jpg 是词法分析的状态转换图，lex.py中self.lexfun()就是据此实现
3. 布尔表达式文法.jpg 表达式和赋值表达式文法.jpg 是识别其表达式的文法


## 关于

1. 系统编码格式:utf-8
2. IDE：Pycharm
3. 启动文件：main.py
4. 作者：西南北

## 注：取余操作