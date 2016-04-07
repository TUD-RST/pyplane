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

import ast
import numpy as np
from scipy import linalg as LA
from core.Logging import myLogger
from core.Canvas import Canvas


class EquilibriumHandler(object):
    def __init__(self, parent):
        self.myWidget = parent
        self.stack = {}
        self.tgl = False
        self.jacobians = {}

    def toggle(self):
        self.tgl = not self.tgl

    def update_equilibria(self):
        self.myWidget.Plot.canvas.draw()

    def clear_stack(self):
        self.stack = {}

    def list_equilibria(self):
        return self.stack.keys()

    def approx_ep_jacobian(self, equilibrium):
        """ this function returns the jacobian for an equilibrium with a slight numerical error.
            use this function instead of self.jacobian(equilibrium)!
        """
        if self.is_equilibrium(equilibrium):
            true_equilibrium = self.return_true_equilibrium(equilibrium)
            jac = self.jacobian(true_equilibrium)
            return jac
        else:
            return False

    def get_linearized_equation(self, equilibrium):
        pass

    def characterize_equilibrium(self, equilibrium):
        self.get_eigenval_eigenvec(equilibrium)

    def get_eigenval_eigenvec(self, equilibrium):
        # eigenvalues, eigenvectors
        jac = self.approx_ep_jacobian(equilibrium)
        eigenvalues, eigenvectors = LA.eig(jac)
        return eigenvalues, eigenvectors

    def plot_equilibrium(self, z_equilibrium, jacobian):
        """ this function plots an equilibrium point
        """
        self.eq_plot = self.myWidget.Plot.canvas.axes.plot(z_equilibrium[0],
                                              z_equilibrium[1],
                                              'ro',
                                              picker=5)

        self.stack[str(z_equilibrium)] = self.eq_plot
        # TODO: actually this function was implemented in graph class
        self.update_equilibria()

        myLogger.message("Equilibrium Point found at: " + str(z_equilibrium))
        myLogger.message("jacobian:\n" + str(jacobian))

    def jacobian(self, equilibrium):
        if equilibrium in self.jacobians.keys():
            return self.jacobians[equilibrium]
        else:
            return False

    def find_equilibrium(self, z_init):
        """ hopf2.ppf has problems with this algorithms -> TODO: debug!!!
        """
        # TODO: this try-loop is too long!
        try:
            if self.tgl:
                # newton's method to find equilibrium points
                iterlimit = 50
                iter = 0
                h = .000001

                z_next = z_init

                functionf = self.myWidget.mySystem.equation.rhs(z_init)

                # allow for large/small solutions
                errorlim = np.linalg.norm(functionf, np.inf) * 0.000001

                while ((np.linalg.norm(functionf, np.inf) > errorlim) & (iter < iterlimit)):
                    iter = iter + 1

                    # now we calculate the jacobian
                    jacobian = np.eye(2)

                    for i in range(0, 2):
                        sav = z_next[i]
                        z_next[i] = z_next[i] + h
                        functionfhj = self.myWidget.mySystem.equation.rhs(z_next)
                        jac = (functionfhj - functionf) / h

                        jacobian[0, i] = jac[0]
                        jacobian[1, i] = jac[1]

                        z_next[i] = sav
                    z_next = z_next - np.linalg.solve(jacobian, functionf)
                    functionf = self.myWidget.mySystem.equation.rhs(z_next)

                if iter > (iterlimit - 1):
                    fLag = [0, 0]
                else:
                    fLag = [1, 1]

                    # TODO: this for loop is used twice: why not put it in a function?
                    for i in range(0, 2):
                        sav = z_next[i]
                        z_next[i] = z_next[i] + h
                        functionfhj = self.myWidget.mySystem.equation.rhs(z_next)
                        jac = (functionfhj - functionf) / h

                        jacobian[0, i] = jac[0]
                        jacobian[1, i] = jac[1]

                        z_next[i] = sav

                #TODO: use list instead of array and safe casting
                z_next = list(z_next)

                # due to numerical errors, this is not sufficient and
                # there could be multiple equilibria plotted where
                # only one should be:
                # calculate the distance to all existing equilibrium points
                # if the distance is smaller than a certain value epsilon, it is
                # assumed that this equilibrium point is already calculated
                epsilon = 1e-4

                if len(self.stack.keys()) == 0:
                    self.plot_equilibrium(z_next, jacobian)
                    self.jacobians[str(z_next)] = jacobian
                    return z_next

                else:
                    # there are equilibria already
                    # if the distance to an existing equilibrium point is less
                    # than epsilon, do not plot

                    if not self.calculated_before(z_next):
                        myLogger.debug_message("Equilibrium Point already there!")
                    else:
                        self.plot_equilibrium(z_next, jacobian)
                        # add to jacobians
                        self.jacobians[str(z_next)] = jacobian
                        return z_next

                        # d_norm = []  # list with distance to equ. pts
                        #
                        # for ep in self.eqp_stack.keys():
                        #     ep = ast.literal_eval(ep)
                        #     x_val = z_next[0] - ep[0]
                        #     y_val = z_next[1] - ep[1]
                        #
                        #     d_norm.append(np.sqrt(x_val ** 2 + y_val ** 2))
                        #
                        # if any(d < epsilon for d in d_norm):
                        #     myLogger.debug_message("Equilibrium Point already there!")
                        #
                        # else:
                        #     self.plot_equilibrium(z_next, jacobian)
                        #     # add to jacobians
                        #     self.jacobians[str(z_next)] = jacobian

        except:
            myLogger.error_message("Something strange happened while calculating the equilibrium")

    def is_equilibrium(self, equilibrium):
        """ this function returns True if delivered point was calculated as an equilibrium point before
            and False if it wasn't calculated. due to numerical errors two equilibrium points are
            understood as identical if the distance between these points is less than epsilon
        """
        d_norm = []  # list with distance to equ. pts
        epsilon = 1e-4

        # for ep in true_eq_values:
        for ep in self.stack.keys():
            ep = ast.literal_eval(ep)
            x_val = equilibrium[0] - ep[0]
            y_val = equilibrium[1] - ep[1]

            distance = np.sqrt(x_val ** 2 + y_val ** 2)

            d_norm.append(distance)

        if any(d < epsilon for d in d_norm):
            return True
        else:
            return False

    def return_true_equilibrium(self, equilibrium):
        """ due to numerical errors a point might be very close to the calculated and stacked equilibrium.
            instead of recalculating within an epsilon area around a calculated equilibrium point, this
            function returns the already calculated equilibrium. that is especially helpful when asking
            for its jacobian.
        """
        # check every single key if its distance is less than epsilon, if yes return true value
        epsilon = 1e-4

        for ep in self.stack.keys():
            ep_num = ast.literal_eval(ep)
            x_val = equilibrium[0] - ep_num[0]
            y_val = equilibrium[1] - ep_num[1]

            distance = np.sqrt(x_val ** 2 + y_val ** 2)

            if distance < epsilon:
                true_equilibrium = ep
                return true_equilibrium

        return False

    def calculated_before(self, equilibrium):
        """ this function essentially does the same as self.is_equilibrium. instead, it is used to check
            if an equilibrium was calculated before. the function returns True if it has been calculated before
            and False if a new equilibrium point was found.
        """
        if self.is_equilibrium(equilibrium):
            return False
        else:
            return True
