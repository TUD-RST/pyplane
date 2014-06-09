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


class StreamlineHandler(object):
    def __init__(self):
        self.sl_stack = []
        self.tgl = False

        # TODO: logging
        #myLogger.debug_message("Streamlines class initialized")

    def register_graph(self, parent,plot_pp):
        self.plot_pp = plot_pp
        self.parent = parent

    def clear_stack(self):
        self.sl_stack = []

    def update(self):
        """ This function plots streamlines.
        """
        self.remove()

        if self.tgl:
            xmin, xmax, ymin, ymax = self.plot_pp.axes.axis()
            N = int(myConfig.read("Streamlines", "stream_gridPointsInX"))
            M = int(myConfig.read("Streamlines", "stream_gridPointsInY"))
            stream_linewidth = float(myConfig.read("Streamlines", "stream_linewidth"))
            stream_color = str(myConfig.read("Streamlines", "stream_color"))
            stream_density = float(myConfig.read("Streamlines", "stream_density"))

            a = np.linspace(xmin, xmax, N)
            b = np.linspace(ymin, ymax, M)
            X1, Y1 = np.meshgrid(a, b)

            try:
                DX1, DY1 = mySystem.rhs([X1, Y1])
                streamplot = self.plot_pp.axes.streamplot(X1, Y1, DX1, DY1,
                                                          density=stream_density,
                                                          linewidth=stream_linewidth,
                                                          color=stream_color)

                self.sl_stack.append(streamplot)

                myLogger.message("Streamplot created")
            except:
                myLogger.debug_message("No system yet")

        self.plot_pp.draw()

    def remove(self):
        """
            This function removes Streamlines if existent.
        """
        if len(self.sl_stack) != 0:
            for i in xrange(0, len(self.sl_stack)):
                sl = self.sl_stack.pop()

                try:
                    sl.lines.remove()
                except:
                    pass

                #sl_arrows.remove() doesn't work
                # doesn't work either: del sl.arrows
                # as long as no other patches are used:
                self.plot_pp.axes.patches = []

            myLogger.message("Streamlines removed")
        else:
            myLogger.debug_message("No streamlines to delete")

myStreamlines = StreamlineHandler()
