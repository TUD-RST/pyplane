# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2013  Klemens Fritzsche, pyplane@leckstrom.de
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
##############################################################################

import sympy as sp
import numpy as np
from .ConfigHandler import myConfig
from .Logging import myLogger

class FunctionHandler(object):
    """ this class defines the function """
    def __init__(self, parent):
        self.mySystem = parent

        self.fct_stack = []
        self.x = sp.symbols('x')
        self.y = sp.symbols('y')

    def add(self):
        try:
            fct_string = str(self.mySystem.myPyplane.yLineEdit.text())
        except UnicodeEncodeError as exc:
            myLogger.error_message("input error!")
            myLogger.debug_message(str(exc))

        fct_string = str(self.mySystem.myPyplane.yLineEdit.text())

        if fct_string != "":
            try:
                self.fct_expr = sp.sympify(fct_string)
                self.fct = sp.lambdify((self.x, self.y), self.fct_expr, 'numpy')
                xmin, xmax, ymin, ymax = self.mySystem.Phaseplane.Plot.canvas.axes.axis()

                # plot the function for an x-interval twice as big as the current window
                deltax = (xmax - xmin) / 2
                deltay = (ymax - ymin) / 2
                plot_xmin = xmin - deltax
                plot_xmax = xmax + deltax
                plot_ymin = ymin - deltay
                plot_ymax = ymax + deltay

                pts_in_x = int(myConfig.read("Functions", "fct_gridPointsInX"))
                pts_in_y = int(myConfig.read("Functions", "fct_gridPointsInY"))

                fct_color = myConfig.read("Functions", "fct_color")
                fct_linewidth = float(myConfig.read("Functions", "fct_linewidth"))

                x = np.arange(plot_xmin, plot_xmax, (xmax - xmin) / pts_in_x)
                y = np.arange(plot_ymin, plot_ymax, (ymax - ymin) / pts_in_y)

                X, Y = np.meshgrid(x, y)

                myfunc = self.fct(X, Y)
                # TODO: plots like y=1/x have a connection between -inf and +inf that is not actually there!

                # plot function and put on function-stack
                new_fct = self.mySystem.Phaseplane.Plot.canvas.axes.contour(X, Y, myfunc, [0],
                                                            zorder=100,
                                                            linewidths=fct_linewidth,
                                                            colors=fct_color)
                # new_fct = self.myGraph.plot_pp.axes.plot(xvalue, yvalue, label="fct", color="green")
                self.fct_stack.append(new_fct)

                self.mySystem.Phaseplane.Plot.update()
                myLogger.message("function plot: 0 = " + fct_string)

            except Exception as error:
                # TODO: use handle_exception for this
                myLogger.error_message(str(error))
        else:
            myLogger.error_message("Please enter function.")

    def remove_all(self):
        if len(self.fct_stack) != 0:
            for i in range(0, len(self.fct_stack)):
                fct = self.fct_stack.pop().collections
                for j in range(0, len(fct)):
                    try:
                        fct[j].remove()
                    except Exception as error:
                        myLogger.debug_message("couldn't delete function")
                        myLogger.debug_message(str(type(error)))
                        myLogger.debug_message(str(error))
            myLogger.message("functions removed")
        else:
            myLogger.debug_message("no function to delete")

        self.mySystem.Phaseplane.Plot.update()
