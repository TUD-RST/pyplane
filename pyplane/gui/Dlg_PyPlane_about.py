# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:07:50 2015

@author: winkler
"""

import sys
import platform
from PyQt5 import QtWidgets
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtCore import PYQT_VERSION_STR
import matplotlib as mp
import numpy as np
import sympy as sp
import scipy as scp

from .Ui_PyPlane_about import Ui_DlgAbout


class AboutDialog(QtWidgets.QDialog, Ui_DlgAbout):
    def __init__(self, version, date):
        self.status = None
        QtWidgets.QDialog.__init__(self)

        self.setupUi(self)

        platform_info = platform.uname()
        platform_info_str = '%s %s (%s) on %s' % (platform_info.system, platform_info.release, platform_info.version,
                                                  platform_info.machine)
        
        self.pyplane_version_info.setText(version)
        self.pyplane_date.setText(date)
        self.pyplane_platform.setText(platform_info_str)

        self.python_version_info.setText(sys.version)
        self.numpy_version_info.setText(np.version.version)
        self.scipy_version_info.setText(scp.__version__)
        self.sympy_version_info.setText(sp.__version__)
        self.matplotlib_version_info.setText(mp.__version__)
        self.qt_version_info.setText(QT_VERSION_STR)
        self.pyqt_version_info.setText(PYQT_VERSION_STR)

        self.show()
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.close)
        self.exec_()