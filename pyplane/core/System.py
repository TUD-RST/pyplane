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

import sympy as sp
import pylab as pl
import numpy as np

from .Logging import myLogger
from .Equation import Equation
from .ConfigHandler import myConfig
from ..gui.Widgets import SystemTabWidget, PhaseplaneWidget, ZoomWidgetSimple, ThreeDWidget
from .TrajectoryHandler import TrajectoryHandler
from .FunctionHandler import FunctionHandler

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
        self._tab_index = self.myPyplane.tabWidget.currentIndex() # what was this for again?

        # TODO: possiblity to choose a name
        global counter
        counter = counter + 1
        if name == None:
            self.name = "System %s" % counter
        else:
            self.name = name

        # content of new systems tab:
        self._tab = SystemTabWidget(self)
        contents = QtWidgets.QWidget(self.myPyplane.tabWidget)
        self._tab.setupUi(contents)

        self.myPyplane.tabWidget.insertTab(0, contents, self.name)
        self.myPyplane.tabWidget.setCurrentIndex(0)

        self.Trajectories = TrajectoryHandler(self)
        self.Functions = FunctionHandler(self)

        self.Phaseplane = PhaseplaneWidget(self)
        self.Xt = ZoomWidgetSimple(self, "x")
        self.Yt = ZoomWidgetSimple(self, "y")
        self.Txy = ThreeDWidget(self)

        # create tab content (phaseplane, x-t and y-t widgets)
        self._tab.ppLayout.addWidget(self.Phaseplane)
        self._tab.xLayout.addWidget(self.Xt)
        self._tab.yLayout.addWidget(self.Yt)
        self._tab.tLayout.addWidget(self.Txy)

        # connect mouse events (left mouse button click) in phase plane
        self.Phaseplane.Plot.canvas.mpl_connect('button_press_event', self.Phaseplane.Plot.onclick)
        self.Phaseplane.Plot.canvas.mpl_connect('pick_event', self.Phaseplane.Plot.onpick)

        self.myPyplane.initialize_ui()

        #~ if self.linear:
            #~ self.plot_eigenvectors()

    #~ def pickle(self, path):
        #~ pcl.dump(self.data, file(str(path), 'w'))
        #~ return pps_file

    #~ def unpickle(self, pps_file):
        #~ self.data = pcl.load(pps_file)
        #~ assert isinstance(self.data, Container), myLogger.error_message("Could not open pps file!")

    def plot_eigenvectors(self, equilibrium):
        if self.linear:
            # system is linear -> calculate jacobian
            x, y = sp.symbols("x, y")
            xdot = self.equation.x_dot_expr
            ydot = self.equation.y_dot_expr

            A11 = xdot.diff(x)
            A12 = xdot.diff(y)
            A21 = ydot.diff(x)
            A22 = ydot.diff(y)
            jac = np.array([[A11,A12],[A21,A22]], dtype=float)

            eigenvalues, eigenvectors = np.linalg.eig(jac)
            eigvec0 = eigenvectors[:,0]
            eigvec1 = eigenvectors[:,1]
            # calculating eigenvalues and eigenvectors:
            #~ eigenvalues, eigenvectors = self.Phaseplane.Equilibria.get_eigenval_eigenvec(equilibrium)
            myLogger.message("Eigenvectors: (" + str(eigvec0[0]) + ", " + str(eigvec0[1]) + ") and (" + str(eigvec1[0]) + ", " + str(eigvec1[1]) + ")")

            # scaling
            xmin, xmax, ymin, ymax = self.Phaseplane.Plot.get_limits()
            d1 = (xmax-xmin)/10
            d2 = (ymax-ymin)/10
            d_large = (xmax-xmin)*(ymax-ymin)

            EV0 = np.array([np.real(eigvec0[0]),np.real(eigvec0[1])])
            EV0_norm = np.sqrt(EV0[0]**2+EV0[1]**2)
            EV0_scaled = np.array([d1*(1/EV0_norm)*EV0[0],d1*(1/EV0_norm)*EV0[1]])

            EV1 = np.array([np.real(eigvec1[0]),np.real(eigvec1[1])])
            EV1_norm = np.sqrt(EV1[0]**2+EV1[1]**2)
            EV1_scaled = np.array([d1*(1/EV1_norm)*EV1[0],d1*(1/EV1_norm)*EV1[1]])

            # plot equilibrium:
            self.Phaseplane.Plot.canvas.axes.plot(equilibrium[0], equilibrium[1], 'ro', pickradius=2)

            # plot eigenvectors:
            color_eigenvec = myConfig.read("Linearization", "lin_eigenvector_color")
            color_eigenline = myConfig.read("Linearization", "lin_eigenvector_linecolor")

            if myConfig.get_boolean("Linearization","lin_show_eigenline"):
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], d_large*EV0_scaled[0], d_large*EV0_scaled[1], head_width=0, head_length=0, color=color_eigenline)
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], -d_large*EV0_scaled[0], -d_large*EV0_scaled[1], head_width=0, head_length=0, color=color_eigenline)
            if myConfig.get_boolean("Linearization","lin_show_eigenvector"):
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], EV0_scaled[0], EV0_scaled[1], head_width=0, head_length=0, color=color_eigenvec)

            if myConfig.get_boolean("Linearization","lin_show_eigenline"):
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], d_large*EV1_scaled[0], d_large*EV1_scaled[1], head_width=0, head_length=0, color=color_eigenline)
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], -d_large*EV1_scaled[0], -d_large*EV1_scaled[1], head_width=0, head_length=0, color=color_eigenline)
            if myConfig.get_boolean("Linearization","lin_show_eigenvector"):
                self.Phaseplane.Plot.canvas.axes.arrow(equilibrium[0], equilibrium[1], EV1_scaled[0], EV1_scaled[1], head_width=0, head_length=0, color=color_eigenvec)

            self.Phaseplane.Plot.add_eigenvectors_to_title(eigvec0, eigvec1)

            #~ return eigvec0, eigvec1

    def update(self):
        self.Phaseplane.Plot.update()
        self.Xt.Plot.update()
        self.Yt.Plot.update()
        self.Txy.Plot.update()
