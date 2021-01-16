# -*- coding: utf-8 -*-

#    Copyright (C) 2013
#    by Klemens Fritzsche, pyplane@leckstrom.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Klemens Fritzsche'

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from matplotlib.backend_bases import NavigationToolbar2 as NavigationToolbar
from matplotlib.backends.backend_qt5 import cursord


class Toolbar(NavigationToolbar):
    """
        This class hides the functionality of NavigationToolbar, and only
        provides the necessary functions (only zooming at the moment)
    """
    def _init_toolbar(self):
        pass

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0

        w = abs(x1 - x0)
        h = abs(y1 - y0)

        rect = [int(val) for val in (min(x0, x1), min(y0, y1), w, h)]
        self.canvas.drawRectangle(rect)

    def set_cursor(self, cursor):
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(cursord[cursor]))

if __package__ is None:
    __package__ = "core.toolbar"
