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


from core.ConfigHandler import myConfig
from core.Logging import myLogger
from core.System import mySystem
#from core.StreamlineHandler import myStreamlines


class VectorfieldHandler(object):
    def __init__(self):
        #: @type:list[int]
        self.vf_stack = []
        for object in self.vf_stack:
            assert(isinstance(object, list))
            object = "string"

        self.tgl = True

        self.mySystem = mySystem

    def set_system(self, system):
        self.mySystem = system

    def register_graph(self, parent, plot_pp):
        self.parent = parent # TODO: not needed, why keep it?
        self.plot_pp = plot_pp

    def update(self):
        """ This function updates the vectorfield in the phase plane.
        """
        self.remove_vectorfield()

        if self.tgl:
            # get axis limits
            xmin, xmax, ymin, ymax = self.plot_pp.axes.axis()
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
                DX1, DY1 = self.mySystem.rhs([X1, Y1])
                M = np.hypot(DX1, DY1)
                M[M == 0] = 1.
                DX1_mix, DY1_mix = DX1 / M, DY1 / M

                quiver = self.plot_pp.axes.quiver(X1, Y1, DX1_mix, DY1_mix,
                                                  angles='xy',
                                                  headwidth=vf_arrowHeadWidth,
                                                  headlength=vf_arrowHeadLength,
                                                  width=vf_arrowWidth,
                                                  pivot=vf_arrowPivot,
                                                  color=vf_color)

                self.vf_stack.append(quiver)
                myLogger.message("vector field created")
            except:
                myLogger.debug_message("Please enter system.")

        self.plot_pp.draw()

    def remove_vectorfield(self):
        """ This function removes the vector field if existent.
        """

        # IPS()
        if len(self.vf_stack) != 0:
            for i in xrange(0, len(self.vf_stack)):
                try:
                    self.vf_stack.pop().remove()
                    myLogger.message("Vector field removed")
                except Exception as error:
                    myLogger.debug_message("Couldn't delete vector field")
                    myLogger.debug_message(str(type(error)))
                    myLogger.debug_message(str(error))

        else:
            myLogger.debug_message("No vector field to delete")


myVectorfield = VectorfieldHandler()
