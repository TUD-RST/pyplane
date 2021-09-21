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


from .ConfigHandler import myConfig
from .Logging import myLogger


class Vectorfield(object):
    def __init__(self, parent):
        self.myWidget = parent
        self.stack = []
        self.tgl = myConfig.get_boolean("Vectorfield", "vf_onByDefault")
        self.update()

    def toggle(self):
        self.tgl = not self.tgl
        self.update()
        
    def update(self):
        """ This function updates the vectorfield in the phase plane.
        """
        self.remove()

        if self.tgl:
            # get axis limits
            xmin, xmax, ymin, ymax = self.myWidget.Plot.canvas.axes.axis()

            N = int(myConfig.read("Vectorfield", "vf_gridPointsInX"))
            M = int(myConfig.read("Vectorfield", "vf_gridPointsInY"))
            vf_color = str(myConfig.read("Vectorfield", "vf_color"))
            vf_arrowHeadWidth = float(myConfig.read("Vectorfield", "vf_arrowHeadWidth"))
            vf_arrowHeadLength = float(myConfig.read("Vectorfield", "vf_arrowHeadLength"))
            vf_arrowWidth = float(myConfig.read("Vectorfield", "vf_arrowWidth"))
            vf_arrowPivot = str(myConfig.read("Vectorfield", "vf_arrowPivot"))

            a = np.linspace(xmin - xmin / N, xmax - xmax / N, N)
            b = np.linspace(ymin - ymin / M, ymax - ymax / M, M)
            X1, Y1 = np.meshgrid(a, b)

            try:
                DX1, DY1 = self.myWidget.mySystem.equation.rhs([X1, Y1])
                M = np.hypot(DX1, DY1)
                M[M == 0] = 1.
                DX1_mix, DY1_mix = DX1 / M, DY1 / M

                quiver = self.myWidget.Plot.canvas.axes.quiver(X1, Y1, DX1_mix, DY1_mix,
                                                  angles='xy',
                                                  headwidth=vf_arrowHeadWidth,
                                                  headlength=vf_arrowHeadLength,
                                                  width=vf_arrowWidth,
                                                  pivot=vf_arrowPivot,
                                                  color=vf_color)

                self.stack.append(quiver)
                myLogger.message("vector field created")
            except:
                myLogger.debug_message("Please enter system.")

        self.myWidget.Plot.update()

    def remove(self):
        """ This function removes the vector field if existent.
        """
        if len(self.stack) != 0:
            for i in range(0, len(self.stack)):
                try:
                    self.stack.pop().remove()
                    myLogger.message("Vector field removed")
                except Exception as error:
                    myLogger.debug_message("Couldn't delete vector field")
                    myLogger.debug_message(str(type(error)))
                    myLogger.debug_message(str(error))

        else:
            myLogger.debug_message("No vector field to delete")
