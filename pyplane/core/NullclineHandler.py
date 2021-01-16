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

import numpy as np
import sympy as sp
from sympy.solvers import solve
import matplotlib.pyplot as pyplot

from .Logging import myLogger
from .ConfigHandler import myConfig
from .Canvas import Canvas


class NullclineHandler(object):
    def __init__(self, parent):
        self.myWidget = parent
        self.nc_stack = []
        self.tgl = False

    def toggle(self):
        """ This function behaves like a toggle and turns nullclines on and off.
        """
        self.tgl = not self.tgl
        self.update()

    def clear_stack(self):
        self.nc_stack = []

    def update(self):
        """ this function will show nullclines
        """

        self.remove()

        if self.tgl:
            # get axis limits
            xmin, xmax, ymin, ymax = self.myWidget.Plot.canvas.axes.axis()

            pts_in_x = int(myConfig.read("Nullclines", "nc_gridPointsInX"))
            pts_in_y = int(myConfig.read("Nullclines", "nc_gridPointsInY"))
            nc_color_xdot = myConfig.read("Nullclines", "nc_color_xdot")
            nc_color_ydot = myConfig.read("Nullclines", "nc_color_ydot")
            nc_linewidth = float(myConfig.read("Nullclines", "nc_linewidth"))

            a = np.arange(xmin, xmax, (xmax - xmin) / pts_in_x)
            b = np.arange(ymin, ymax, (xmax - xmin) / pts_in_y)
            X1, Y1 = np.meshgrid(a, b)

            try:
                DX1, DY1 = self.myWidget.mySystem.equation.rhs([X1, Y1])

                nullclines_xdot = self.myWidget.Plot.canvas.axes.contour(X1, Y1, DX1,
                                                            levels=[0],
                                                            linewidths=nc_linewidth,
                                                            colors=nc_color_xdot)
                nullclines_ydot = self.myWidget.Plot.canvas.axes.contour(X1, Y1, DY1,
                                                            levels=[0],
                                                            linewidths=nc_linewidth,
                                                            colors=nc_color_ydot)

                # proxy artist for legend
                proxy_x_nc = pyplot.Rectangle((0, 0), 1, 1, fc=nc_color_xdot)
                proxy_y_nc = pyplot.Rectangle((0, 0), 1, 1, fc=nc_color_ydot)
                self.myWidget.Plot.canvas.axes.legend([proxy_x_nc, proxy_y_nc],
                                         ["x-Nullclines", "y-Nullclines"],
                                         bbox_to_anchor=(0., 1.02, 1., .102),
                                         loc=2,
                                         prop={'size': 8},
                                         frameon=False)

                self.nc_stack.append(nullclines_xdot)
                self.nc_stack.append(nullclines_ydot)
            except:
                myLogger.debug_message("Please submit system.")
        # refresh graph
        self.myWidget.Plot.canvas.draw()

    def remove(self):
        if len(self.nc_stack) != 0:
            for i in range(0, len(self.nc_stack)):
                nc = self.nc_stack.pop().collections
                for j in range(0, len(nc)):
                    try:
                        nc[j].remove()
                    except Exception as error:
                        myLogger.debug_message("Could not delete nullcline.")
                        myLogger.debug_message(str(type(error)))
                        myLogger.debug_message(str(error))
            # remove nullclines legend
            self.myWidget.Plot.canvas.axes.legend_ = None

            myLogger.message("Nullclines removed.")
        else:
            myLogger.debug_message("No nullclines to delete.")

    def print_symbolic_nullclines(self):
        """ This function will try to find the symbolic nullclines.
        """
        try:
            isoclines_x, isoclines_y = self.find_symbolic_nullclines()

            myLogger.message("Computed nullclines:")

            for i in range(len(isoclines_x)):
                myLogger.message("x = " + str(isoclines_x[i]).strip('[]'))

            for i in range(len(isoclines_y)):
                myLogger.message("y = " + str(isoclines_y[i]).strip('[]'))
        except:
            myLogger.message("Couldn't solve nullclines. There seems to be no algorithm implemented")

    def find_symbolic_nullclines(self):
        """ this function will try to find the symbolic roots for x prime and y prime (nullclines /
            isoclines with zero growth)

            please be aware that this only works in case sympy can find the root for the expression.
            for example, there are no algorithms implemented to solve the equation "x+sin(x)=0"
        """
        y = sp.Symbol('y')
        x = sp.Symbol('x')

        self.isoclines_x = []  # solution with x=...
        self.isoclines_y = []  # solution with y=...

        # TODO: solve gets called often - optimization possible?

        # 1:    isoclines parallel to x
        # 1.1:  check if y_dot is function of y (sloppy, should work though)
        if str(self.myWidget.mySystem.equation.y_dot_expr).count('y') != 0:
            # if yes: solve(self.y_dot_expr,y)
            self.isoclines_y.append(solve(self.myWidget.mySystem.equation.y_dot_expr, y))
            # print "isoclines parallel to x: y="+str(solve(self.y_dot_expr,y))

            # add "x=.." solutions that do not depend on y
            y_dot_solved_x = solve(self.myWidget.mySystem.equation.y_dot_expr, x)
            for i in range(len(y_dot_solved_x)):
                if str(y_dot_solved_x[i]).count('y') == 0:
                    self.isoclines_x.append(y_dot_solved_x[i])

        # if not: check if y_dot is function of x
        elif str(self.myWidget.mySystem.equation.y_dot_expr).count('x') != 0:
            # if yes: solve(self.y_dot_expr,x)
            self.isoclines_x.append(solve(self.myWidget.mySystem.equation.y_dot_expr, x))
            # print "and also: x="+str(solve(self.y_dot_expr,x))
        else:
            #               if not: skip (expression must be scalar)
            pass

        # 2:    isoclines parallel to y
        # 2.1:  check if x_dot is function of y:
        if str(self.myWidget.mySystem.equation.x_dot_expr).count('y') != 0:
            # if yes: solve(self.x_dot_expr,y)
            self.isoclines_y.append(solve(self.myWidget.mySystem.equation.x_dot_expr, y))
            # print "isoclines parallel to y: y="+str(solve(self.x_dot_expr,y))

            # add "x=.." solutions that do not depend on y
            x_dot_solved_x = solve(self.myWidget.mySystem.equation.x_dot_expr, x)
            for i in range(len(x_dot_solved_x)):
                if str(x_dot_solved_x[i]).count('y') == 0:
                    self.isoclines_x.append(x_dot_solved_x[i])

        #           if not: check if x_dot is function of x
        elif str(self.myWidget.mySystem.equation.x_dot_expr).count('x') != 0:
            #               if yes: solve(self.x_dot_expr,x)
            self.isoclines_x.append(solve(self.myWidget.mySystem.equation.x_dot_expr, x))
        #            print "and also: x="+str(solve(self.x_dot_expr,x))
        else:
            #               if not: skip (expression must be scalar)
            pass

        # return list of solutions
        return [self.isoclines_x, self.isoclines_y]
