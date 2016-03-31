# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SettingsWidget.ui'
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

class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        SettingsWidget.setObjectName(_fromUtf8("SettingsWidget"))
        SettingsWidget.resize(513, 413)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.SectionListView = QtGui.QListView(SettingsWidget)
        self.SectionListView.setMinimumSize(QtCore.QSize(100, 0))
        self.SectionListView.setMaximumSize(QtCore.QSize(100, 16777215))
        self.SectionListView.setObjectName(_fromUtf8("SectionListView"))
        self.horizontalLayout_2.addWidget(self.SectionListView)
        self.SectionLayout = QtGui.QFormLayout()
        self.SectionLayout.setObjectName(_fromUtf8("SectionLayout"))
        self.SetupSectionTitle = QtGui.QLabel(SettingsWidget)
        self.SetupSectionTitle.setMinimumSize(QtCore.QSize(200, 30))
        self.SetupSectionTitle.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.SetupSectionTitle.setFont(font)
        self.SetupSectionTitle.setText(_fromUtf8(""))
        self.SetupSectionTitle.setObjectName(_fromUtf8("SetupSectionTitle"))
        self.SectionLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.SetupSectionTitle)
        self.horizontalLayout_2.addLayout(self.SectionLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.SetupApplyButton = QtGui.QPushButton(SettingsWidget)
        self.SetupApplyButton.setMinimumSize(QtCore.QSize(100, 0))
        self.SetupApplyButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.SetupApplyButton.setObjectName(_fromUtf8("SetupApplyButton"))
        self.horizontalLayout.addWidget(self.SetupApplyButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SettingsWidget)
        QtCore.QMetaObject.connectSlotsByName(SettingsWidget)

    def retranslateUi(self, SettingsWidget):
        SettingsWidget.setWindowTitle(_translate("SettingsWidget", "Form", None))
        self.SetupApplyButton.setText(_translate("SettingsWidget", "Apply", None))

