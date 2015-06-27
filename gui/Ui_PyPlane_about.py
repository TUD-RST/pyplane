# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/Ui_PyPlane_about.ui'
#
# Created: Wed Jun 24 11:46:39 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_DlgAbout(object):
    def setupUi(self, DlgAbout):
        DlgAbout.setObjectName(_fromUtf8("DlgAbout"))
        DlgAbout.resize(459, 393)
        self.buttonBox = QtGui.QDialogButtonBox(DlgAbout)
        self.buttonBox.setGeometry(QtCore.QRect(110, 360, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.grpInfo = QtGui.QGroupBox(DlgAbout)
        self.grpInfo.setGeometry(QtCore.QRect(0, 0, 451, 351))
        self.grpInfo.setObjectName(_fromUtf8("grpInfo"))
        self.verticalLayoutWidget = QtGui.QWidget(self.grpInfo)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 431, 321))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txtProgName = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtProgName.setFont(font)
        self.txtProgName.setObjectName(_fromUtf8("txtProgName"))
        self.horizontalLayout_2.addWidget(self.txtProgName)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(60, 60))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/pyplane_logo.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.txtCopyright = QtGui.QLabel(self.verticalLayoutWidget)
        self.txtCopyright.setWordWrap(True)
        self.txtCopyright.setObjectName(_fromUtf8("txtCopyright"))
        self.verticalLayout.addWidget(self.txtCopyright)
        self.txtGPL = QtGui.QLabel(self.verticalLayoutWidget)
        self.txtGPL.setObjectName(_fromUtf8("txtGPL"))
        self.verticalLayout.addWidget(self.txtGPL)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_python_version = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_python_version.setObjectName(_fromUtf8("label_python_version"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_python_version)
        self.python_version_info = QtGui.QLabel(self.verticalLayoutWidget)
        self.python_version_info.setObjectName(_fromUtf8("python_version_info"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.python_version_info)
        self.label_qt_version = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_qt_version.setObjectName(_fromUtf8("label_qt_version"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_qt_version)
        self.label_pyqt_version = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_pyqt_version.setObjectName(_fromUtf8("label_pyqt_version"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_pyqt_version)
        self.label_matplotlib_version = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_matplotlib_version.setObjectName(_fromUtf8("label_matplotlib_version"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_matplotlib_version)
        self.qt_version_info = QtGui.QLabel(self.verticalLayoutWidget)
        self.qt_version_info.setObjectName(_fromUtf8("qt_version_info"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.qt_version_info)
        self.pyqt_version_info = QtGui.QLabel(self.verticalLayoutWidget)
        self.pyqt_version_info.setObjectName(_fromUtf8("pyqt_version_info"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pyqt_version_info)
        self.matplotlib_version_info = QtGui.QLabel(self.verticalLayoutWidget)
        self.matplotlib_version_info.setObjectName(_fromUtf8("matplotlib_version_info"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.matplotlib_version_info)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(DlgAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DlgAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DlgAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgAbout)

    def retranslateUi(self, DlgAbout):
        DlgAbout.setWindowTitle(_translate("DlgAbout", "Dialog", None))
        self.grpInfo.setTitle(_translate("DlgAbout", "Information", None))
        self.txtProgName.setText(_translate("DlgAbout", "PyPlane Version 1.0 (23.06.2015)", None))
        self.txtCopyright.setText(_translate("DlgAbout", "Copyright (C) 2013-2015\n"
"by Klemens Fritzsche, Carsten Knoll, Jan Winkler\n"
"Technische Universität Dresden\n"
"Institut für Regelungs- und Steuerungstheorie", None))
        self.txtGPL.setText(_translate("DlgAbout", "This code is free software, licensed under the terms of the\n"
"GNU General Public License, version 3\n"
"<http://www.gnu.org/license/>.", None))
        self.label_2.setText(_translate("DlgAbout", "Please consult <https://github.com/TUD-RST/pyplane.git> for updated versions of this program!", None))
        self.label_python_version.setText(_translate("DlgAbout", "Python-Version:", None))
        self.python_version_info.setText(_translate("DlgAbout", "TextLabel", None))
        self.label_qt_version.setText(_translate("DlgAbout", "QT-Version:", None))
        self.label_pyqt_version.setText(_translate("DlgAbout", "PyQT-Version:", None))
        self.label_matplotlib_version.setText(_translate("DlgAbout", "Matplotlib-Version:", None))
        self.qt_version_info.setText(_translate("DlgAbout", "TextLabel", None))
        self.pyqt_version_info.setText(_translate("DlgAbout", "TextLabel", None))
        self.matplotlib_version_info.setText(_translate("DlgAbout", "TextLabel", None))

import icons_rc
