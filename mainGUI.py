# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 991, 651))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit_3 = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_3.setObjectName("textEdit_3")
        self.horizontalLayout.addWidget(self.textEdit_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menuBar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menuBar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menuBar)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menuBar)
        self.menu_7.setObjectName("menu_7")
        self.menu_8 = QtWidgets.QMenu(self.menuBar)
        self.menu_8.setObjectName("menu_8")
        MainWindow.setMenuBar(self.menuBar)
        self.actionnew = QtWidgets.QAction(MainWindow)
        self.actionnew.setObjectName("actionnew")
        self.actionhelp = QtWidgets.QAction(MainWindow)
        self.actionhelp.setObjectName("actionhelp")
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.actionsaves = QtWidgets.QAction(MainWindow)
        self.actionsaves.setObjectName("actionsaves")
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        self.actionW = QtWidgets.QAction(MainWindow)
        self.actionW.setObjectName("actionW")
        self.actionP = QtWidgets.QAction(MainWindow)
        self.actionP.setObjectName("actionP")
        self.actionM = QtWidgets.QAction(MainWindow)
        self.actionM.setObjectName("actionM")
        self.actionO = QtWidgets.QAction(MainWindow)
        self.actionO.setObjectName("actionO")
        self.actionD = QtWidgets.QAction(MainWindow)
        self.actionD.setObjectName("actionD")
        self.actionDFA = QtWidgets.QAction(MainWindow)
        self.actionDFA.setObjectName("actionDFA")
        self.actionLL_1 = QtWidgets.QAction(MainWindow)
        self.actionLL_1.setObjectName("actionLL_1")
        self.menu.addAction(self.actionnew)
        self.menu.addAction(self.actionopen)
        self.menu.addAction(self.actionsave)
        self.menu.addAction(self.actionsaves)
        self.menu.addAction(self.actionquit)
        self.menu_3.addAction(self.actionW)
        self.menu_3.addAction(self.actionDFA)
        self.menu_4.addAction(self.actionP)
        self.menu_4.addAction(self.actionLL_1)
        self.menu_5.addAction(self.actionM)
        self.menu_6.addAction(self.actionO)
        self.menu_8.addAction(self.actionhelp)
        self.menu_8.addAction(self.actionabout)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())
        self.menuBar.addAction(self.menu_4.menuAction())
        self.menuBar.addAction(self.menu_5.menuAction())
        self.menuBar.addAction(self.menu_6.menuAction())
        self.menuBar.addAction(self.menu_7.menuAction())
        self.menuBar.addAction(self.menu_8.menuAction())

        self.retranslateUi(MainWindow)
        self.actionquit.triggered.connect(MainWindow.close)
        self.actionopen.triggered.connect(MainWindow.openFile)
        self.actionW.triggered.connect(MainWindow.W)
        self.actionM.triggered.connect(MainWindow.M)
        self.actionO.triggered.connect(MainWindow.O)
        self.actionP.triggered.connect(MainWindow.P)
        self.actionhelp.triggered.connect(MainWindow.H)
        self.actionabout.triggered.connect(MainWindow.A)
        self.actionsaves.triggered.connect(MainWindow.S)
        self.actionsave.triggered.connect(MainWindow.save)
        self.actionnew.triggered.connect(MainWindow.new)
        self.actionDFA.triggered.connect(MainWindow.DFA)
        self.actionLL_1.triggered.connect(MainWindow.LL1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "西南北编译器"))
        self.menu.setTitle(_translate("MainWindow", "文件(F)"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑(E)"))
        self.menu_3.setTitle(_translate("MainWindow", "词法分析(W)"))
        self.menu_4.setTitle(_translate("MainWindow", "语法分析(P)"))
        self.menu_5.setTitle(_translate("MainWindow", "中间代码(M)"))
        self.menu_6.setTitle(_translate("MainWindow", "目标代码(O)"))
        self.menu_7.setTitle(_translate("MainWindow", "查看(V)"))
        self.menu_8.setTitle(_translate("MainWindow", "帮助(H)"))
        self.actionnew.setText(_translate("MainWindow", "新建(N)"))
        self.actionnew.setToolTip(_translate("MainWindow", "新建"))
        self.actionhelp.setText(_translate("MainWindow", "帮助"))
        self.actionabout.setText(_translate("MainWindow", "关于Compiler"))
        self.actionopen.setText(_translate("MainWindow", "打开(O)"))
        self.actionsave.setText(_translate("MainWindow", "保存(S)"))
        self.actionsaves.setText(_translate("MainWindow", "另存为(A)"))
        self.actionquit.setText(_translate("MainWindow", "退出(Q)"))
        self.actionW.setText(_translate("MainWindow", "词法分析(W)"))
        self.actionP.setText(_translate("MainWindow", "语法分析(P)"))
        self.actionM.setText(_translate("MainWindow", "中间代码(M)"))
        self.actionO.setText(_translate("MainWindow", "目标代码(O)"))
        self.actionD.setText(_translate("MainWindow", "识别单词(D)"))
        self.actionDFA.setText(_translate("MainWindow", "有穷自动机(DFA)"))
        self.actionLL_1.setText(_translate("MainWindow", "LL(1)"))

