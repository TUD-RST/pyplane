# -*- coding: utf-8 -*-
"""
This stuff is needed for building the stand-alone executable. It is called by
the pyinstaller script (via the --runtime-hook flag) and ensures that the
proper API version for PyQT4 is loaded. PyPlane uses the API version 2, but
by default PyInstaller enables API version 1 resulting in non functional
setting dialogs where the datatype QVariant plays an important role.

Created on Wed Jun 14 15:49:26 2017

@author: winkler
"""

import sip

sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)