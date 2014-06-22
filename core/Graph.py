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

# sys.path.append("/home/klim/software/python/iphelp_ips")#location of iphelp
# from ipHelp import IPS

#import pylab as pl
#import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from core.Canvas import Canvas
#from scipy import integrate
from core.Logging import myLogger
from core.ConfigHandler import myConfig
from core.System import mySystem
from core.EquilibriumHandler import myEquilibria
from core.NullclineHandler import myNullclines
from core.TrajectoryHandler import myTrajectories
from core.StreamlineHandler import myStreamlines
from core.VectorfieldHandler import myVectorfield


class Graph(object):
    """
        This class is in charge of plotting the vectorfield, streamlines,
        nullclines and trajectories.

    """

    def __init__(self, parent, plot_pp, plot_x, plot_y):
        assert isinstance(plot_pp, Canvas)
        assert isinstance(plot_x, Canvas)
        assert isinstance(plot_y, Canvas)

        # for deleting lineedits/etc. from parent class
        self.parent = parent
        self.plot_pp = plot_pp
        self.plot_x = plot_x
        self.plot_y = plot_y

        # register_graph plot_pp
        myEquilibria.register_graph(self.plot_pp)
        myNullclines.register_graph(self.plot_pp)
        myTrajectories.register_graph(self, self.plot_pp, self.plot_x, self.plot_y)
        myStreamlines.register_graph(self, self.plot_pp)
        myVectorfield.register_graph(self, self.plot_pp)

        # read initial values: vector field, streamlines, nullclines
        self.vf_toggle = myConfig.get_boolean("Vectorfield", "vf_onByDefault")
        self.nc_toggle = myConfig.get_boolean("Nullclines", "nc_onByDefault")
        self.sl_toggle = myConfig.get_boolean("Streamlines", "stream_onByDefault")

        myLogger.debug_message("Graph class initialized")

    def clear_graph(self, Graph):
        """ This function resets a graph.
            Depending on the default values in the config file, the following is shown:
            - grid
            - minor ticks in x and y direction
            - labels on x and y axes
            - title
        """
        Graph.axes.clear()

        if Graph == self.plot_pp:
            section = "Phaseplane"
            token = "pp_"
        elif Graph == self.plot_x:
            section = "x-t-plot"
            token = "x_"
        else:
            section = "y-t-plot"
            token = "y_"

        if myConfig.get_boolean(section, token + "showGrid"):
            Graph.axes.grid()

        if myConfig.get_boolean(section, token + "showMinorTicks"):
            Graph.axes.minorticks_on()
        else:
            Graph.axes.minorticks_off()

        if not myConfig.get_boolean(section, token + "showXTicks"):
            Graph.axes.xaxis.set_ticks([])

        if not myConfig.get_boolean(section, token + "showYTicks"):
            Graph.axes.yaxis.set_ticks([])

        if myConfig.get_boolean(section, token + "showXLabel"):
            pp_label_fontsize = myConfig.read(section, token + "labelFontSize")
            if Graph == self.plot_pp:
                xlabel = "$x$"
            else:
                xlabel = "$t$"
            Graph.axes.set_xlabel(xlabel, fontsize=pp_label_fontsize)

        if myConfig.get_boolean(section, token + "showTitle"):
            title_x_dot = sp.latex(mySystem.what_is_my_system()[0])
            title_y_dot = sp.latex(mySystem.what_is_my_system()[1])
            Graph.axes.set_title("$\\dot{x} = " + title_x_dot + "$\n$\\dot{y} = " + title_y_dot + "$")
        else:
            Graph.fig.subplots_adjust(top=0.99)

        if myConfig.get_boolean(section, token + "showYLabel"):
            pp_label_fontsize = myConfig.read(section, token + "labelFontSize")
            if Graph == self.plot_pp:
                ylabel = "$\\dot{x}$"
            elif Graph == self.plot_x:
                ylabel = "$x$"
            else:
                ylabel = "$y$"
            Graph.axes.set_ylabel(ylabel, fontsize=pp_label_fontsize)

        if not myConfig.get_boolean(section, token + "showSpines"):
            for spine in Graph.axes.spines.itervalues():
                spine.set_visible(False)

        self.update_graph(Graph)
        myLogger.debug_message("Graph cleared")

    def clear(self):
        """ This function clears every graph.
        """
        # reset plots
        for graph in [self.plot_pp, self.plot_x, self.plot_y]:
            self.clear_graph(graph)

        # empty stacks
        self.vf_stack = []
        myStreamlines.clear_stack()
        myTrajectories.clear_stack()
        myEquilibria.clear_stack()
        myNullclines.clear_stack()

        myLogger.debug_message("graphs cleared!\n")

    def update_graph(self, Graph):
        """ This function updates a graph.
        """
        Graph.draw()

    def update_all(self):
        """ This function updates every graph.
        """
        for graph in [self.plot_pp, self.plot_x, self.plot_y]:
            self.update_graph(graph)

    def set_window_range(self, Graph):
        """ This function changes the window range of Graph.
        """

        # TODO: check if there is a better way to do this? --> put lineedit stuff in PyplaneMainWindow or MainApp!
        try:
            # phase plane flag
            pp_flag = False

            if Graph == self.plot_pp:
                xmin = float(self.parent.PP_xminLineEdit.text())
                xmax = float(self.parent.PP_xmaxLineEdit.text())
                ymin = float(self.parent.PP_yminLineEdit.text())
                ymax = float(self.parent.PP_ymaxLineEdit.text())

                # set flag
                pp_flag = True

            elif Graph == self.plot_x:
                xmin = float(self.parent.X_tminLineEdit.text())
                xmax = float(self.parent.X_tmaxLineEdit.text())
                ymin = float(self.parent.X_xminLineEdit.text())
                ymax = float(self.parent.X_xmaxLineEdit.text())

            # elif Graph == self.plot_y:
            else:
                xmin = float(self.parent.Y_tminLineEdit.text())
                xmax = float(self.parent.Y_tmaxLineEdit.text())
                ymin = float(self.parent.Y_yminLineEdit.text())
                ymax = float(self.parent.Y_ymaxLineEdit.text())

            if xmin < xmax and ymin < ymax:
                Graph.axes.set_xlim(xmin, xmax)
                Graph.axes.set_ylim(ymin, ymax)

                if pp_flag:
                    # self.update_graph(Graph)
                    myVectorfield.update()
                    myStreamlines.update()

                    #self.update_vectorfield()
                    #self.update_streamlines()
                    myNullclines.update()

            else:
                myLogger.error_message("Please check window size input!")

        except Exception as error:
            myLogger.error_message("Error!")
            myLogger.debug_message(str(type(error)))
            myLogger.debug_message(str(error))

        # update_all graph
        self.update_graph(Graph)

    def get_limits(self, Graph):
        """ This function returns the limits of a graph.
        """
        return Graph.axes.axis()

    def read_init(self):
        """ reads initial condition from line edits
        """
        x_init = float(self.parent.PP_x_initLineEdit.text())
        y_init = float(self.parent.PP_y_initLineEdit.text())

        return [x_init, y_init]


    def refresh(self):
        myVectorfield.update()
        myStreamlines.update()
        myNullclines.update()

        # change window range values in gui
        self.parent.update_window_range_lineedits()

    def toggle_vectorfield(self):
        """
            This function behaves like a toggle for turning the vectorfield on
            and off.
        """
        myVectorfield.tgl = not myVectorfield.tgl

        # turn off streamlines if vf and sl are True in config
        if myVectorfield.tgl and myStreamlines.tgl:
            self.toggle_streamlines()

        myVectorfield.update()
        #self.update()

    def toggle_streamlines(self):
        """
            This function behaves like a toggle and turns streamlines on and off
        """
        myStreamlines.tgl = not myStreamlines.tgl

        if (myVectorfield.tgl and myStreamlines.tgl):
            self.toggle_vectorfield()

        myStreamlines.update()

        #self.update()

    def trajectory_direction(self):
        forward = self.parent.forwardCheckbox.isChecked()
        backward = self.parent.backwardCheckbox.isChecked()

        return [forward, backward]

    def plot_vector(self, Graph, vector):
        # TODO: is this supposed to be here?
        # basically this is working, but vectors need to be shown on canvas!

        # x, y, dx, dy = vector
        # arr = plt.Arrow(x, y, dx, dy)
        # plt.gca().add_patch(arr)
        # plt.show()
        pass

    def onclick(self, event):
        """
            This function is in charge of the mouse-click behaviour.
            A left mouse button click is recognized, the mouse location serves
            as an initial condition for trajectories.
        """

        #TODO: check if try/except is the best thing to do here!

        if not self.plot_pp.zoomMode:
            try:
                mySystem
            except:
                # only capture mouse click if system exists
                myLogger.error_message("Please enter system.")
            else:
                cond1 = mySystem.x_dot is not None
                cond2 = mySystem.x_dot is not None
                cond3 = str(self.parent.xDotLineEdit.text()) != ""
                cond4 = str(self.parent.yDotLineEdit.text()) != ""

                if cond1 and cond2 and cond3 and cond4:
                    event1 = event.xdata is not None
                    event2 = event.ydata is not None
                    button = event.button == 1

                    if not myEquilibria.eqp_toggle:
                        # event.xdata and event.ydata are initial conditions for integration
                        # mouse click will also be recognized if clicked outside of the graph area, so filter that:

                        if event1 and event2 and button:
                            forward, backward = self.trajectory_direction()
                            if myTrajectories.plot_trajectory([event.xdata, event.ydata], forward, backward):
                                myLogger.message("New initial condition: " + str(event.xdata) + ", " + str(event.ydata))
                        else:
                            pass

                    else:
                        # equilibrium point
                        if event1 and event2 and button:
                            myEquilibria.find_equilibrium([event.xdata, event.ydata])
                else:
                    # only capture mouse click if system exists
                    myLogger.error_message("Please enter system.")

        else:
            myLogger.debug_message("in zoom mode")

    def onpick(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind

        myLogger.message("Equilibrium Point chosen: "+str(xdata)+", "+str(ydata))

        equilibrium = [map(float,xdata)[0], map(float,ydata)[0]]

        self.parent.add_linearization_tab(equilibrium)
        #xdata[ind], ydata[ind])
        #print
        #'onpick points:', zip(xdata[ind], ydata[ind])

if __package__ is None:
    __package__ = "core.graph"
