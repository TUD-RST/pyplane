# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ZoomWidgetSimple.ui'
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

class Ui_ZoomWidgetSimple(object):
    def setupUi(self, ZoomWidgetSimple):
        ZoomWidgetSimple.setObjectName(_fromUtf8("ZoomWidgetSimple"))
        ZoomWidgetSimple.resize(620, 477)
        self.horizontalLayout = QtGui.QHBoxLayout(ZoomWidgetSimple)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(ZoomWidgetSimple)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.label = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.xminLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xminLineEdit.sizePolicy().hasHeightForWidth())
        self.xminLineEdit.setSizePolicy(sizePolicy)
        self.xminLineEdit.setMinimumSize(QtCore.QSize(100, 22))
        self.xminLineEdit.setObjectName(_fromUtf8("xminLineEdit"))
        self.verticalLayout.addWidget(self.xminLineEdit)
        self.label_2 = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.xmaxLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xmaxLineEdit.sizePolicy().hasHeightForWidth())
        self.xmaxLineEdit.setSizePolicy(sizePolicy)
        self.xmaxLineEdit.setMinimumSize(QtCore.QSize(0, 22))
        self.xmaxLineEdit.setObjectName(_fromUtf8("xmaxLineEdit"))
        self.verticalLayout.addWidget(self.xmaxLineEdit)
        self.label_3 = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.yminLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yminLineEdit.sizePolicy().hasHeightForWidth())
        self.yminLineEdit.setSizePolicy(sizePolicy)
        self.yminLineEdit.setMinimumSize(QtCore.QSize(0, 22))
        self.yminLineEdit.setObjectName(_fromUtf8("yminLineEdit"))
        self.verticalLayout.addWidget(self.yminLineEdit)
        self.label_4 = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.ymaxLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ymaxLineEdit.sizePolicy().hasHeightForWidth())
        self.ymaxLineEdit.setSizePolicy(sizePolicy)
        self.ymaxLineEdit.setMinimumSize(QtCore.QSize(100, 22))
        self.ymaxLineEdit.setObjectName(_fromUtf8("ymaxLineEdit"))
        self.verticalLayout.addWidget(self.ymaxLineEdit)
        self.SetButton = QtGui.QPushButton(ZoomWidgetSimple)
        self.SetButton.setObjectName(_fromUtf8("SetButton"))
        self.verticalLayout.addWidget(self.SetButton)
        self.ZoomButton = QtGui.QPushButton(ZoomWidgetSimple)
        self.ZoomButton.setObjectName(_fromUtf8("ZoomButton"))
        self.verticalLayout.addWidget(self.ZoomButton)
        self.RefreshButton = QtGui.QPushButton(ZoomWidgetSimple)
        self.RefreshButton.setObjectName(_fromUtf8("RefreshButton"))
        self.verticalLayout.addWidget(self.RefreshButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.frame = QtGui.QWidget(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(444, 0))
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(ZoomWidgetSimple)
        QtCore.QMetaObject.connectSlotsByName(ZoomWidgetSimple)

    def retranslateUi(self, ZoomWidgetSimple):
        ZoomWidgetSimple.setWindowTitle(_translate("ZoomWidgetSimple", "Form", None))
        self.label_9.setText(_translate("ZoomWidgetSimple", "Window Range", None))
        self.label.setText(_translate("ZoomWidgetSimple", "xmin", None))
        self.label_2.setText(_translate("ZoomWidgetSimple", "xmax", None))
        self.label_3.setText(_translate("ZoomWidgetSimple", "ymin", None))
        self.label_4.setText(_translate("ZoomWidgetSimple", "ymax", None))
        self.SetButton.setText(_translate("ZoomWidgetSimple", "Set", None))
        self.ZoomButton.setText(_translate("ZoomWidgetSimple", "Zoom", None))
        self.RefreshButton.setText(_translate("ZoomWidgetSimple", "Refresh", None))

