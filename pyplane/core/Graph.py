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

import sympy as sp

from .Canvas import Canvas
from .Logging import myLogger
from .ConfigHandler import myConfig

from PyQt5.QtWidgets import QMessageBox

__author__ = 'Klemens Fritzsche'


class Plot(object):
    def __init__(self, parent, canvas):
        assert isinstance(canvas, Canvas)
        self.myWidget = parent
        self.canvas = canvas

        if not isinstance(self, PhasePlot):
            self._section = "%s-t-plot" % self.myWidget.param
            self._token = "%s_" % self.myWidget.param
        else:
            self._section = "Phaseplane"
            self._token = "pp_"

        self.clear()
        self.set_window_range()

    def clear(self):
        self.canvas.axes.clear()

        if myConfig.get_boolean(self._section, self._token + "showGrid"):
            self.canvas.axes.grid()

        if myConfig.get_boolean(self._section, self._token + "showMinorTicks"):
            self.canvas.axes.minorticks_on()
        else:
            self.canvas.axes.minorticks_off()

        if not myConfig.get_boolean(self._section, self._token + "showXTicks"):
            self.canvas.axes.xaxis.set_ticks([])

        if not myConfig.get_boolean(self._section, self._token + "showYTicks"):
            self.canvas.axes.yaxis.set_ticks([])

        if myConfig.get_boolean(self._section, self._token + "showXLabel"):
            pp_label_fontsize = myConfig.read(self._section, self._token + "labelFontSize")
            xlabel = "$%s$" % self.myWidget.xlabel_str
            self.canvas.axes.set_xlabel(xlabel, fontsize=pp_label_fontsize)

        if myConfig.get_boolean(self._section, self._token + "showTitle"):
            title_x_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[0])
            title_y_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[1])
            self.canvas.axes.set_title("$\\dot{x} = " + title_x_dot + "$\n$\\dot{y} = " + title_y_dot + "$")
        else:
            self.canvas.fig.subplots_adjust(top=0.99)

        if myConfig.get_boolean(self._section, self._token + "showYLabel"):
            pp_label_fontsize = myConfig.read(self._section, self._token + "labelFontSize")
            ylabel = "$%s$" % self.myWidget.ylabel_str
            self.canvas.axes.set_ylabel(ylabel, fontsize=pp_label_fontsize)

        # TODO (jcw): Check if this can be removed (together with Graph class)
        # if not myConfig.get_boolean(self._section, self._token + "showSpines"):
        #     for spine in Graph.axes.spines.values():
        #         spine.set_visible(False)

        self.update()
        myLogger.debug_message("Graph cleared")
        
    def add_eigenvectors_to_title(self, vec0, vec1):
        if myConfig.get_boolean(self._section, self._token + "showTitle"):
            title_x_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[0])
            title_y_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[1])
            dec_place = 2  # TODO: read from config
            self.canvas.axes.set_title("$\\dot{x} = " + title_x_dot + "$\n$\\dot{y} = " + title_y_dot +
                                       "$\n$\mathbf{v}_1=("+str(round(vec0[0],dec_place)) + "," +
                                       str(round(vec0[1],dec_place)) + ")^T\qquad\mathbf{v}_2=(" +
                                       str(round(vec1[0],dec_place)) + "," + str(round(vec1[1],dec_place)) + ")^T$")

    def update(self):
        try:
            self.canvas.draw()
        except Exception as e:
            if 'latex' in str(e).lower():
                QMessageBox.critical(None, 'Error',
                                     'LaTeX not properly installed! Please check the following message:\n\n' + str(e))
            else:
                QMessageBox.critical(None, 'Error',
                                     'Something seems to be wrong with matplotlib. Please check the following message:'
                                     '\n\n' + str(e))
            exit()        

    def set_window_range(self):
        _min = float(self.myWidget.xminLineEdit.text())
        _max = float(self.myWidget.xmaxLineEdit.text())
        _tmin = float(self.myWidget.yminLineEdit.text())
        _tmax = float(self.myWidget.ymaxLineEdit.text())

        if _min < _max and _tmin < _tmax:
            self.canvas.axes.set_xlim(_min, _max)
            self.canvas.axes.set_ylim(_tmin, _tmax)
        else:
            myLogger.error_message("Please check window size input!")

        self.update()

    def get_limits(self):
        """ This function returns the limits of a graph. """
        return self.canvas.axes.axis()


class ThreeDPlot(object):
    def __init__(self, parent, canvas):
        assert isinstance(canvas, Canvas)
        self.myWidget = parent
        self.canvas = canvas

        self._section = "3d-plot"
        self._token = "3d_"

        self.clear()
        self.set_window_range()

    def clear(self):
        self.canvas.axes.clear()

        if myConfig.get_boolean(self._section, self._token + "showGrid"):
            self.canvas.axes.grid()

        if myConfig.get_boolean(self._section, self._token + "showMinorTicks"):
            self.canvas.axes.minorticks_on()
        else:
            self.canvas.axes.minorticks_off()

        if not myConfig.get_boolean(self._section, self._token + "showTTicks"):
            self.canvas.axes.zaxis.set_ticks([])

        if not myConfig.get_boolean(self._section, self._token + "showXTicks"):
            self.canvas.axes.xaxis.set_ticks([])

        if not myConfig.get_boolean(self._section, self._token + "showYTicks"):
            self.canvas.axes.yaxis.set_ticks([])

        if myConfig.get_boolean(self._section, self._token + "showTitle"):
            title_x_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[0])
            title_y_dot = sp.latex(self.myWidget.mySystem.equation.what_is_my_system()[1])
            self.canvas.axes.set_title("$\\dot{x} = " + title_x_dot + "$\n$\\dot{y} = " + title_y_dot + "$")
        else:
            self.canvas.fig.subplots_adjust(top=0.99)

        if myConfig.get_boolean(self._section, self._token + "showXLabel"):
            xlabel = "$x$"
            label_fontsize = myConfig.read(self._section, self._token + "labelFontSize")
            self.canvas.axes.set_xlabel(xlabel, fontsize=label_fontsize)

        if myConfig.get_boolean(self._section, self._token + "showYLabel"):
            label_fontsize = myConfig.read(self._section, self._token + "labelFontSize")
            ylabel = "$y$"
            self.canvas.axes.set_ylabel(ylabel, fontsize=label_fontsize)

        if myConfig.get_boolean(self._section, self._token + "showTLabel"):
            label_fontsize = myConfig.read(self._section, self._token + "labelFontSize")
            tlabel = "$t$"
            self.canvas.axes.set_zlabel(tlabel, fontsize=label_fontsize)

        if not myConfig.get_boolean(self._section, self._token + "showSpines"):
            for spine in self.canvas.axes.spines.values():
                spine.set_visible(False)

        self.update()
        myLogger.debug_message("3d graph cleared")

    def update(self):
        # try:
        self.canvas.draw()
        # except Exception as e:
        #     if 'latex' in e.message.lower():
        #         QMessageBox.critical(None, 'Error', 'LaTeX not properly installed! Please check the following message:\n\n' + e.message)
        #     else:
        #         QMessageBox.critical(None, 'Error', 'Something seems to be wrong with matplotlib. Please check the following message:\n\n' + e.message)
        #     exit()

    def set_window_range(self):        
        _tmin = float(self.myWidget.tminLineEdit.text())
        _tmax = float(self.myWidget.tmaxLineEdit.text())
        _xmin = float(self.myWidget.xminLineEdit.text())
        _xmax = float(self.myWidget.xmaxLineEdit.text())
        _ymin = float(self.myWidget.yminLineEdit.text())
        _ymax = float(self.myWidget.ymaxLineEdit.text())

        if _xmin < _xmax and _ymin < _ymax and _tmin < _tmax:
            #~ self.canvas.axes.set_xlim3d(_xmin, _xmax)
            #~ self.canvas.axes.set_ylim3d(_ymin, _ymax)
            #~ self.canvas.axes.set_zlim3d(_tmin, _tmax)
            self.canvas.axes.set_xlim(_xmin, _xmax)
            self.canvas.axes.set_ylim(_ymin, _ymax)
            self.canvas.axes.set_zlim(_tmin, _tmax)
        else:
            myLogger.error_message("Please check window size input!")

        self.update()

    def get_limits(self):
        """ This function returns the limits of a graph. """
        return self.canvas.axes.axis()


class PhasePlot(Plot):
    def __init__(self, parent, canvas):
        self.myWidget = parent
        Plot.__init__(self, self.myWidget, canvas)

        # read initial values: vector field, streamlines, nullclines
        self.vf_toggle = myConfig.get_boolean("Vectorfield", "vf_onByDefault")
        self.nc_toggle = myConfig.get_boolean("Nullclines", "nc_onByDefault")
        self.sl_toggle = myConfig.get_boolean("Streamlines", "stream_onByDefault")

    def get_limits(self):
        """ This function returns the limits of a graph. """
        return self.canvas.axes.axis()

    def refresh(self):
        self.myWidget.VF.update()
        self.myWidget.SL.update()
        self.myWidget.Nullclines.update()

    def onclick(self, event):
        """
            This function is in charge of the mouse-click behaviour.
            A left mouse button click is recognized, the mouse location serves
            as an initial condition for trajectories.
        """

        # TODO: check if try/except is the best thing to do here!
        if not self.canvas.zoomMode:
            event1 = event.xdata is not None
            event2 = event.ydata is not None
            button = event.button == 1

            if not self.myWidget.Equilibria.tgl:
                # event.xdata and event.ydata are initial conditions for integration
                # mouse click will also be recognized if clicked outside of the graph area, so filter that:
                if event1 and event2 and button:
                    forward, backward = self.myWidget.trajectory_direction()
                    if self.myWidget.mySystem.Trajectories.plot_trajectory([event.xdata, event.ydata],
                                                                           forward, backward):
                        myLogger.message("New initial condition: " + str(event.xdata) + ", " + str(event.ydata))
                else:
                    pass
            else:
                # equilibrium point
                if event1 and event2 and button:
                    equilibrium_point = self.myWidget.Equilibria.find_equilibrium([event.xdata, event.ydata])
                    if equilibrium_point is not None:
                        # is this supposed to be here?
                        pass
                        # jacobian = self.myWidget.Equilibria.approx_ep_jacobian(equilibrium_point)
                        # self.myWidget.mySystem.myPyplane.new_linearized_system(self.myWidget.mySystem, jacobian, equilibrium_point)
        else:
            myLogger.debug_message("in zoom mode")

    def onpick(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        # ind = event.ind

        myLogger.message("Equilibrium Point chosen: "+str(xdata)+", "+str(ydata))


# TODO (jcw): Check if it was really ok to remove the Graph class which followed here

if __package__ is None:
    __package__ = "core.graph"
