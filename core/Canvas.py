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

import pylab as pl

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import rc
from matplotlib import pyplot as plt
from core.Toolbar import Toolbar
from core.ConfigHandler import myConfig
from core.Logging import myLogger


class Canvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        plot_background = myConfig.read("Plotting", "plot_background")
        plot_CanvasBackground = str(myConfig.read("Plotting", "plot_CanvasBackground"))
        plot_fontSize = int(myConfig.read("Plotting", "plot_fontSize"))
        plot_topOfPlot = float(myConfig.read("Plotting", "plot_topOfPlot"))
        plot_leftOfPlot = float(myConfig.read("Plotting", "plot_leftOfPlot"))
        plot_rightOfPlot = float(myConfig.read("Plotting", "plot_rightOfPlot"))
        plot_bottomOfPlot = float(myConfig.read("Plotting", "plot_bottomOfPlot"))

        self.fig = pl.Figure(facecolor=plot_background)

        pl.matplotlib.rc('font', size=plot_fontSize)

        # use latex
        rc('text', usetex=True)

        # ALIASING
        # TODO: read aliasing variables:
        # pl.matplotlib.rc('lines', antialiased=False)
        # pl.matplotlib.rc('text', antialiased=False)
        # pl.matplotlib.rc('patch', antialiased=False)

        self.axes = self.fig.add_subplot(111)

        self.axes.set_axis_bgcolor(plot_CanvasBackground)

        # matplotlib background transparent (issues on old versions?)
        if myConfig.get_boolean("Plotting", "plot_backgroundTransparent"):
            self.fig.frameon = False

        self.adjust = self.fig.subplots_adjust(top=plot_topOfPlot,
                                               left=plot_leftOfPlot,
                                               right=plot_rightOfPlot,
                                               bottom=plot_bottomOfPlot)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.navigationToolbar = Toolbar(self)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # zoom mode on/off
        self.zoomMode = False

        myLogger.debug_message(str(self) + ": initialized")

    def toggle_zoom_mode(self):
        self.zoomMode = not self.zoomMode
        self.navigationToolbar.zoom()