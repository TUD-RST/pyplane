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


class StreamlineHandler(object):
    def __init__(self, parent):
        self.myWidget = parent
        self.sl_stack = []
        self.tgl = False

    def clear_stack(self):
        self.sl_stack = []

    def toggle(self):
        self.tgl = not self.tgl
        self.update()

    def update(self):
        """ This function plots streamlines.
        """
        self.remove()

        if self.tgl:
            xmin, xmax, ymin, ymax = self.myWidget.Plot.canvas.axes.axis()

            N = int(myConfig.read("Streamlines", "stream_gridPointsInX"))
            M = int(myConfig.read("Streamlines", "stream_gridPointsInY"))
            stream_linewidth = float(myConfig.read("Streamlines", "stream_linewidth"))
            stream_color = str(myConfig.read("Streamlines", "stream_color"))
            stream_density = float(myConfig.read("Streamlines", "stream_density"))

            a = np.linspace(xmin, xmax, N)
            b = np.linspace(ymin, ymax, M)
            X1, Y1 = np.meshgrid(a, b)

            try:
                DX1, DY1 = self.myWidget.mySystem.equation.rhs([X1, Y1])
                streamplot = self.myWidget.Plot.canvas.axes.streamplot(X1, Y1, DX1, DY1,
                                                          density=stream_density,
                                                          linewidth=stream_linewidth,
                                                          color=stream_color)

                self.sl_stack.append(streamplot)

                myLogger.message("Streamplot created")
            except:
                myLogger.debug_message("No system yet")

        self.myWidget.Plot.canvas.draw()

    def remove(self):
        """
            This function removes Streamlines if existent.
        """
        if len(self.sl_stack) != 0:
            for i in range(0, len(self.sl_stack)):
                sl = self.sl_stack.pop()

                try:
                    sl.lines.remove()
                except:
                    pass

                self.myWidget.Plot.canvas.axes.patches.clear()

            myLogger.message("Streamlines removed")
        else:
            myLogger.debug_message("No streamlines to delete")
