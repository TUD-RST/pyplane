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

from __future__ import division

__author__ = 'Klemens Fritzsche'

from PyQt4 import QtGui

import sympy as sp
import pylab as pl
import numpy as np

from core.Logging import myLogger
from core.Equation import Equation
from core.ConfigHandler import myConfig
from gui.Widgets import SystemTabWidget, PhaseplaneWidget, ZoomWidgetSimple
from core.TrajectoryHandler import TrajectoryHandler
from core.FunctionHandler import FunctionHandler

counter = 0

class Container(object):
    """ For exporting and importing pyplane systems (.pps) files
    """
    def __init__(self):
        pass

class System(object):
    """ Class that bundles everything after submitting a new system
    """
    def __init__(self, parent, equation=None, name=None, linear=False):
        #~ assert isinstance(parent, PyplaneMainWindow)
        self.myPyplane = parent
        self.equation = Equation(equation)

        self.linear = linear
        self._tab_index = self.myPyplane.tabWidget.currentIndex()

        # TODO: possiblity to choose a name
        global counter
        counter = counter + 1
        if name == None:
            self.name = "System %s" % counter
        else:
            self.name = name

        # content of new systems tab:
        self._tab = SystemTabWidget(self)
        contents = QtGui.QWidget(self.myPyplane.tabWidget)
        self._tab.setupUi(contents)

        self.myPyplane.tabWidget.insertTab(0, contents, self.name)
        self.myPyplane.tabWidget.setCurrentIndex(0)

        self.Trajectories = TrajectoryHandler(self)
        self.Functions = FunctionHandler(self)

        self.Phaseplane = PhaseplaneWidget(self)
        self.Xt = ZoomWidgetSimple(self, "x")
        self.Yt = ZoomWidgetSimple(self, "y")

        # create tab content (phaseplane, x-t and y-t widgets)
        self._tab.ppLayout.addWidget(self.Phaseplane)
        self._tab.xLayout.addWidget(self.Xt)
        self._tab.yLayout.addWidget(self.Yt)

        # connect mouse events (left mouse button click) in phase plane
        self.Phaseplane.Plot.canvas.mpl_connect('button_press_event', self.Phaseplane.Plot.onclick)
        self.Phaseplane.Plot.canvas.mpl_connect('pick_event', self.Phaseplane.Plot.onpick)

        self.myPyplane.initialize_ui()

        if self.linear:
            self.plot_eigenvectors()

    #~ def pickle(self, path):
        #~ pcl.dump(self.data, file(str(path), 'w'))
        #~ return pps_file

    #~ def unpickle(self, pps_file):
        #~ self.data = pcl.load(pps_file)
        #~ assert isinstance(self.data, Container), myLogger.error_message("Could not open pps file!")

    def plot_eigenvectors(self):
        pass

    def update(self):
        self.Phaseplane.Plot.update()
        self.Xt.Plot.update()
        self.Yt.Plot.update()
