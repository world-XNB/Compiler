# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dfaGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DFA(object):
    def setupUi(self, DFA):
        DFA.setObjectName("DFA")
        DFA.resize(1000, 800)
        self.layoutWidget = QtWidgets.QWidget(DFA)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 16, 981, 781))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_3.addWidget(self.graphicsView)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.layoutWidget)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout_4.addWidget(self.graphicsView_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.layoutWidget)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.horizontalLayout_5.addWidget(self.graphicsView_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DFA)
        self.pushButton.clicked.connect(DFA.check) # type: ignore
        self.pushButton_2.clicked.connect(DFA.nfa) # type: ignore
        self.pushButton_3.clicked.connect(DFA.dfa) # type: ignore
        self.pushButton_4.clicked.connect(DFA.mfa) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DFA)

    def retranslateUi(self, DFA):
        _translate = QtCore.QCoreApplication.translate
        DFA.setWindowTitle(_translate("DFA", "DFA"))
        self.label.setText(_translate("DFA", "正则表达式"))
        self.pushButton.setText(_translate("DFA", "验证"))
        self.pushButton_2.setText(_translate("DFA", "NFA"))
        self.pushButton_3.setText(_translate("DFA", "DFA"))
        self.pushButton_4.setText(_translate("DFA", "MFA"))