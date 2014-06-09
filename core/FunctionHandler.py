# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2013  Klemens Fritzsche, klim@leckstrom.de
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


class Function(object):
    """ this class defines the function """


    def __init__(self):
        self.x = sp.symbols('x')
        self.y = sp.symbols('y')


    def setRhs(self, string):
        """ this function will set the differential equations """

        self.function_expr = sp.sympify(string)

        self.function = sp.lambdify((self.x, self.y), self.function_expr, 'numpy')


    def whatIsMySystem(self):
        """ this function will return the current system """

        return self.function

    def rhs(self, z, t=0.):
        """ this function represents the system """
        self.x, self.y = z
        fct = self.function(self.x, self.y)

        return fct