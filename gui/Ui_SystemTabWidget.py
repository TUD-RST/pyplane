# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/Ui_SystemTabWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SystemTabWidget(object):
    def setupUi(self, SystemTabWidget):
        SystemTabWidget.setObjectName(_fromUtf8("SystemTabWidget"))
        SystemTabWidget.resize(639, 541)
        self.horizontalLayout = QtGui.QHBoxLayout(SystemTabWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(SystemTabWidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.ppTab = QtGui.QWidget()
        self.ppTab.setObjectName(_fromUtf8("ppTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.ppTab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ppLayout = QtGui.QVBoxLayout()
        self.ppLayout.setObjectName(_fromUtf8("ppLayout"))
        self.ppPlaceholder = QtGui.QWidget(self.ppTab)
        self.ppPlaceholder.setObjectName(_fromUtf8("ppPlaceholder"))
        self.ppLayout.addWidget(self.ppPlaceholder)
        self.verticalLayout.addLayout(self.ppLayout)
        self.tabWidget.addTab(self.ppTab, _fromUtf8(""))
        self.xTab = QtGui.QWidget()
        self.xTab.setObjectName(_fromUtf8("xTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.xTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.xLayout = QtGui.QVBoxLayout()
        self.xLayout.setObjectName(_fromUtf8("xLayout"))
        self.xPlaceholder = QtGui.QWidget(self.xTab)
        self.xPlaceholder.setObjectName(_fromUtf8("xPlaceholder"))
        self.xLayout.addWidget(self.xPlaceholder)
        self.verticalLayout_2.addLayout(self.xLayout)
        self.tabWidget.addTab(self.xTab, _fromUtf8(""))
        self.yTab = QtGui.QWidget()
        self.yTab.setObjectName(_fromUtf8("yTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.yTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.yLayout = QtGui.QVBoxLayout()
        self.yLayout.setObjectName(_fromUtf8("yLayout"))
        self.yPlaceholder = QtGui.QWidget(self.yTab)
        self.yPlaceholder.setObjectName(_fromUtf8("yPlaceholder"))
        self.yLayout.addWidget(self.yPlaceholder)
        self.verticalLayout_3.addLayout(self.yLayout)
        self.tabWidget.addTab(self.yTab, _fromUtf8(""))
        self.tTab = QtGui.QWidget()
        self.tTab.setObjectName(_fromUtf8("tTab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tTab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.tLayout = QtGui.QVBoxLayout()
        self.tLayout.setObjectName(_fromUtf8("tLayout"))
        self.tPlaceholder = QtGui.QWidget(self.tTab)
        self.tPlaceholder.setObjectName(_fromUtf8("tPlaceholder"))
        self.tLayout.addWidget(self.tPlaceholder)
        self.verticalLayout_5.addLayout(self.tLayout)
        self.tabWidget.addTab(self.tTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(SystemTabWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SystemTabWidget)

    def retranslateUi(self, SystemTabWidget):
        SystemTabWidget.setWindowTitle(_translate("SystemTabWidget", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ppTab), _translate("SystemTabWidget", "Phase Plane", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.xTab), _translate("SystemTabWidget", "x(t)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.yTab), _translate("SystemTabWidget", "y(t)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tTab), _translate("SystemTabWidget", "t(x,y)", None))

