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

from __future__ import division

__author__ = 'Klemens Fritzsche'

import sympy as sp
import pylab as pl
import numpy as np

from core.Logging import myLogger
from core.ConfigHandler import myConfig
#from IPython import embed


class System(object):
    """ this class defines the differential equation system and contains methods to use it """

    def __init__(self):
        # naming variables
        self.x = sp.symbols('x')
        self.y = sp.symbols('y')

        self.x_dot = None
        self.y_dot = None

        self.x_dot_expr = None
        self.y_dot_expr = None

        try:
            self.max_norm = float(myConfig.read("System", "max_norm"))
        except:
            pass
        else:
            self.max_norm = 1e5

    def set_rhs(self, x_dot_string, y_dot_string):
        """ this function sets the differential equations
        """
        self.x_dot_expr = sp.sympify(x_dot_string)
        self.y_dot_expr = sp.sympify(y_dot_string)

        self.x_dot = sp.lambdify((self.x, self.y), self.x_dot_expr, 'numpy')
        self.y_dot = sp.lambdify((self.x, self.y), self.y_dot_expr, 'numpy')

    def what_is_my_system(self):
        """ this function returns the current system
        """
        return [self.x_dot_expr, self.y_dot_expr]

    def rhs(self, z, t=0.):
        """ this function represents the system
        """

        # falls endliche fluchtzeit:
        # abfrage ob norm(x)>10**5

        norm_z = pl.norm(z)

        if norm_z > self.max_norm:
            myLogger.debug_message("norm(z) exceeds " + str(self.max_norm) + ": norm(z) = " + str(norm_z))
            z2 = (z / norm_z) * self.max_norm
            self.x, self.y = z2
        else:
            self.x, self.y = z

        xx_dot = self.x_dot(self.x, self.y)
        yy_dot = self.y_dot(self.x, self.y)

        zDot = xx_dot, yy_dot

        #         norm_zDot = norm(zDot)
        #
        #         if norm_zDot>self.max_norm*1e3:
        #             myLogger.debug_message("norm(z dot) exceeds 1e10: norm(z')="+str(norm_zDot))

        return np.array([xx_dot, yy_dot])

    def n_rhs(self, z, t=0):
        """ this function is used for backward integration
        """
        solution = self.rhs(z, t)
        n_solution = [x * (-1) for x in solution]

        return n_solution

#     def jacobian(self, X, t=0):
#         """ return the jacobian matrix evaluated in X. """
#
#         Jfun = ndt.Jacobian(self.rhs)
#         return Jfun


#     def solve(self, initialCondition, time):
#         """ solves the system of differential equations """
#
#         self.solution = integrate.odeint(self.rhs, initialCondition, time, full_output=True, mxstep=20000)
#         self.x_t = self.solution[:,0] # extract the x vector
#         self.y_t = self.solution[:,1] # extract the dx/dt vector
#         return [self.x_t, self.y_t]


#if __package__ is None:
#    __package__ = "core.system"

# prepare system for importing
mySystem = System()