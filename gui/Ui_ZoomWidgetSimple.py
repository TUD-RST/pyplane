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
        ZoomWidgetSimple.resize(662, 593)
        self.horizontalLayout = QtGui.QHBoxLayout(ZoomWidgetSimple)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_9 = QtGui.QLabel(ZoomWidgetSimple)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout.addWidget(self.label_9)
        self.tminLabel = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tminLabel.setFont(font)
        self.tminLabel.setObjectName(_fromUtf8("tminLabel"))
        self.verticalLayout.addWidget(self.tminLabel)
        self.xminLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xminLineEdit.sizePolicy().hasHeightForWidth())
        self.xminLineEdit.setSizePolicy(sizePolicy)
        self.xminLineEdit.setMinimumSize(QtCore.QSize(100, 22))
        self.xminLineEdit.setObjectName(_fromUtf8("xminLineEdit"))
        self.verticalLayout.addWidget(self.xminLineEdit)
        self.tmaxLabel = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.tmaxLabel.setFont(font)
        self.tmaxLabel.setObjectName(_fromUtf8("tmaxLabel"))
        self.verticalLayout.addWidget(self.tmaxLabel)
        self.xmaxLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xmaxLineEdit.sizePolicy().hasHeightForWidth())
        self.xmaxLineEdit.setSizePolicy(sizePolicy)
        self.xmaxLineEdit.setMinimumSize(QtCore.QSize(0, 22))
        self.xmaxLineEdit.setObjectName(_fromUtf8("xmaxLineEdit"))
        self.verticalLayout.addWidget(self.xmaxLineEdit)
        self.param_minLabel = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.param_minLabel.setFont(font)
        self.param_minLabel.setObjectName(_fromUtf8("param_minLabel"))
        self.verticalLayout.addWidget(self.param_minLabel)
        self.yminLineEdit = QtGui.QLineEdit(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yminLineEdit.sizePolicy().hasHeightForWidth())
        self.yminLineEdit.setSizePolicy(sizePolicy)
        self.yminLineEdit.setMinimumSize(QtCore.QSize(0, 22))
        self.yminLineEdit.setObjectName(_fromUtf8("yminLineEdit"))
        self.verticalLayout.addWidget(self.yminLineEdit)
        self.param_maxLabel = QtGui.QLabel(ZoomWidgetSimple)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.param_maxLabel.setFont(font)
        self.param_maxLabel.setObjectName(_fromUtf8("param_maxLabel"))
        self.verticalLayout.addWidget(self.param_maxLabel)
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
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.mpl_layout = QtGui.QVBoxLayout()
        self.mpl_layout.setObjectName(_fromUtf8("mpl_layout"))
        self.frame = QtGui.QWidget(ZoomWidgetSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(444, 0))
        self.frame.setObjectName(_fromUtf8("frame"))
        self.mpl_layout.addWidget(self.frame)
        self.horizontalLayout.addLayout(self.mpl_layout)

        self.retranslateUi(ZoomWidgetSimple)
        QtCore.QMetaObject.connectSlotsByName(ZoomWidgetSimple)

    def retranslateUi(self, ZoomWidgetSimple):
        ZoomWidgetSimple.setWindowTitle(_translate("ZoomWidgetSimple", "Form", None))
        self.label_9.setText(_translate("ZoomWidgetSimple", "Window Range", None))
        self.tminLabel.setText(_translate("ZoomWidgetSimple", "tmin", None))
        self.tmaxLabel.setText(_translate("ZoomWidgetSimple", "tmax", None))
        self.param_minLabel.setText(_translate("ZoomWidgetSimple", "xmin", None))
        self.param_maxLabel.setText(_translate("ZoomWidgetSimple", "xmax", None))
        self.SetButton.setText(_translate("ZoomWidgetSimple", "Set", None))
        self.ZoomButton.setText(_translate("ZoomWidgetSimple", "Zoom", None))

