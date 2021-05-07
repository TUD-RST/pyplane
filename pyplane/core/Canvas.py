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

import pylab as pl
import matplotlib as mpl
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
from matplotlib import pyplot as plt
from .Toolbar import Toolbar
from .ConfigHandler import myConfig
from .Logging import myLogger


__author__ = 'Klemens Fritzsche'


class Canvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent, latex_installed, proj_3d=False):
        self.myWidget = parent

        plot_background = myConfig.read("Plotting", "plot_background")
        plot_CanvasBackground = str(myConfig.read("Plotting", "plot_CanvasBackground"))
        plot_fontSize = int(myConfig.read("Plotting", "plot_fontSize"))
        plot_topOfPlot = float(myConfig.read("Plotting", "plot_topOfPlot"))
        plot_leftOfPlot = 0.12#float(myConfig.read("Plotting", "plot_leftOfPlot"))
        plot_rightOfPlot = float(myConfig.read("Plotting", "plot_rightOfPlot"))
        plot_bottomOfPlot = 0.1#float(myConfig.read("Plotting", "plot_bottomOfPlot"))

        self.fig = pl.Figure(facecolor=plot_background)

        pl.matplotlib.rc('font', size=plot_fontSize)

        # Check if LaTeX and dvipng are installed on this system since this
        # is required by matplotlib for fine rendering. If it is not installed
        # only basic rendering will be done in the following
        rc('text', usetex=latex_installed)

        # ALIASING
        # TODO: read aliasing variables:
        # pl.matplotlib.rc('lines', antialiased=False)
        # pl.matplotlib.rc('text', antialiased=False)
        # pl.matplotlib.rc('patch', antialiased=False)

        self.axes = self.fig.add_subplot(111, projection="3d" if proj_3d else None)

        # Matplotlib 2.0 vs. 1.5 behavior...
        try:
            self.axes.set_facecolor(plot_CanvasBackground)  # Matplotlib >= 2
        except AttributeError:
            self.axes.set_axis_bgcolor(plot_CanvasBackground)   # Matplotlib < 2

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

        # TODO: rather as a real toolbar:
        # self.toolbar = NavigationToolbar(self, self.myWidget.mpl_layout, coordinates=True)
        # self.myWidget.mplvl.addWidget(self.toolbar)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # zoom mode on/off
        self.zoomMode = False

        myLogger.debug_message(str(self) + ": initialized")

    def toggle_zoom_mode(self):
        self.zoomMode = not self.zoomMode
        self.navigationToolbar.zoom()

        # update line edits
        xmin, xmax, ymin, ymax = self.axes.axis()
        self.myWidget.xminLineEdit.setText(str(round(xmin,2)))
        self.myWidget.xmaxLineEdit.setText(str(round(xmax,2)))
        self.myWidget.yminLineEdit.setText(str(round(ymin,2)))
        self.myWidget.ymaxLineEdit.setText(str(round(ymax,2)))


class ThreeDCanvas(Canvas):
    def __init__(self, parent, latex_installed):
        super(ThreeDCanvas, self).__init__(parent, latex_installed, proj_3d=True)
        self.myWidget = parent
        self.axes = self.fig.gca()

        self.axes.set_zlabel("t")
        self.axes.set_ylabel("y")
        self.axes.set_xlabel("x")
