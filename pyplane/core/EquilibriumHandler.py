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
from .Logging import myLogger
from .ConfigHandler import myConfig
from .Canvas import Canvas
from .Container import Container


class EquilibriumHandler(object):
    def __init__(self, parent):
        self.myWidget = parent
        self.tgl = False
        # this should be an attribute of the elements in self.stack
        self.jacobians = {}
        self.stack = []

        # counter for unique identifiers
        self.cnt_unclassified = 0
        self.cnt_saddle = 0
        self.cnt_nodalsink = 0
        self.cnt_nodalsource = 0
        self.cnt_center = 0
        self.cnt_spiralsink = 0
        self.cnt_spiralsource = 0
        self.cnt_sink = 0
        self.cnt_source = 0

    def toggle(self):
        self.tgl = not self.tgl

    def update_equilibria(self):
        self.myWidget.Plot.canvas.draw()

    def clear_stack(self):
        self.stack = []

    def list_equilibria(self):
        eq_list = []
        for i in range(len(self.stack)):
            eq_list.append(self.stack[i].coordinates)
        return eq_list

    def list_characterized_equilibria(self):
        character_list = []
        for i in range(len(self.stack)):
            character_list.append(self.stack[i].character)
        return character_list

    def get_equilibrium_by_character_identifier(self, character_identifier):
        for i in range(len(self.stack)):
            if self.stack[i].character == character_identifier:
                return self.stack[i]
        return None

    def approx_ep_jacobian(self, equilibrium):
        """ this function returns the jacobian for an equilibrium with a slight numerical error.
            use this function instead of self.jacobian(equilibrium)!
        """
        if self.is_equilibrium(equilibrium):
            true_equilibrium = self.return_true_equilibrium(equilibrium)
            jac = self.jacobian(true_equilibrium)
            return jac
        else:
            return None

    def get_linearized_equation(self, equilibrium):
        pass

    def characterize_equilibrium(self, jacobian):
        # NOTE: jacobian is evaluated at a specific equilibrium point
        determinant = jacobian[0,0]*jacobian[1,1] - jacobian[1,0]*jacobian[0,1]
        trace = jacobian[0,0] + jacobian[1,1]

        ep_character = ""

        if trace==0 and determinant==0:
            ep_character = "Unclassified " + str(self.cnt_unclassified) # should not happen
            self.cnt_unclassified = self.cnt_unclassified + 1

        elif determinant < 0:
            ep_character = "Saddle " + str(self.cnt_saddle) 
            self.cnt_saddle = self.cnt_saddle + 1

        elif (determinant > 0) and (determinant < ((trace**2)/4)):
            if trace < 0:
                ep_character = "Nodal Sink " + str(self.cnt_nodalsink) 
                self.cnt_nodalsink = self.cnt_nodalsink + 1
            elif trace > 0:
                ep_character = "Nodal Source " + str(self.cnt_nodalsource) 
                self.cnt_nodalsource = self.cnt_nodalsource + 1

        elif determinant > ((trace**2)/4):
            if trace == 0:
                ep_character = "Center " + str(self.cnt_center) 
                self.cnt_center = self.cnt_center + 1
            elif trace < 0:
                ep_character = "Spiral Sink " + str(self.cnt_spiralsink) 
                self.cnt_spiralsink = self.cnt_spiralsink + 1
            elif trace > 0:
                ep_character = "Spiral Source " + str(self.cnt_spiralsource) 
                self.cnt_spiralsource = self.cnt_spiralsource + 1
        elif determinant == ((trace**2)/4):
            if trace < 0:
                ep_character = "Sink " + str(self.cnt_sink) 
                self.cnt_sink = self.cnt_sink + 1
            elif trace > 0:
                ep_character = "Source " + str(self.cnt_source) 
                self.cnt_source = self.cnt_source + 1

        return ep_character

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
                                              pickradius=5)

        # equilibrium point in t(x,y):
        # TODO: let user specify this in config!
        # TODO: show equilibria in x(t) and y(t) as well!
        if self.myWidget.mySystem.Phaseplane.backwardCheckbox.isChecked():
            tmin = -float(myConfig.read("Trajectories", "traj_integrationtime"))
        else:
            tmin = 0

        if self.myWidget.mySystem.Phaseplane.forwardCheckbox.isChecked():
            tmax = float(myConfig.read("Trajectories", "traj_integrationtime"))
        else:
            tmax = 0

        # equilibrium line from tmin to tmax
        if not(tmin==0 and tmax==0):
            self.myWidget.mySystem.Txy.Plot.canvas.axes.plot([z_equilibrium[0],z_equilibrium[0]],
                                                            [z_equilibrium[1],z_equilibrium[1]],
                                                            [tmin, tmax], linestyle="dashed", color="r")
        # marker t=0:
        self.myWidget.mySystem.Txy.Plot.canvas.axes.plot([z_equilibrium[0]],
                                                            [z_equilibrium[1]],
                                                            [0],
                                                            'o',
                                                            color="r")
        self.myWidget.mySystem.Txy.Plot.update()

        #~ self.stack[str(z_equilibrium)] = self.eq_plot
        equilibrium_point = Container()
        equilibrium_point.coordinates = z_equilibrium
        equilibrium_point.plot = self.eq_plot
        equilibrium_point.character = self.characterize_equilibrium(jacobian)
        self.stack.append(equilibrium_point)

        # label equilibrium point
        self.myWidget.Plot.canvas.axes.text(z_equilibrium[0], z_equilibrium[1], equilibrium_point.character, fontsize=10)

        self.update_equilibria()

        # TODO: this call probably move somewhere else:
        if len(self.stack) > 0: self.myWidget.show_linearization_objects()

        myLogger.message("Equilibrium Point found at: " + str(z_equilibrium))
        myLogger.message("jacobian:\n" + str(jacobian))

    def jacobian(self, equilibrium):
        #~ from PyQt4 import QtCore
        #~ from IPython import embed
        #~ QtCore.pyqtRemoveInputHook()
        #~ embed()
        if str(equilibrium) in list(self.jacobians.keys()):
            return self.jacobians[str(equilibrium)]
        else:
            return None

    def find_equilibrium(self, z_init):
        """ hopf2.ppf has problems with this algorithm -> TODO: debug!!!
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

                if len(self.stack) == 0:
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
        except Exception as error:
            myLogger.error_message("Something strange happened while calculating the equilibrium")
            if myConfig.read("Logging", "log_showDbg"):
                myLogger.debug_message(error)

    def is_equilibrium(self, equilibrium):
        """ this function returns True if delivered point was calculated as an equilibrium point before
            and False if it wasn't calculated. due to numerical errors two equilibrium points are
            understood as identical if the distance between these points is less than epsilon
        """
        # equilibrium is of type list [xval, yval]
        d_norm = []  # list with distance to equ. pts
        epsilon = 1e-4

        # for ep in true_eq_values:
        for ep in self.list_equilibria():
            #~ ep = ast.literal_eval(ep)
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
        # equilibrium is of type list [xval, yval]
        # check every single key if its distance is less than epsilon, if yes return true value
        epsilon = 1e-4

        for ep in self.list_equilibria():
            ep_num = ep
            #~ ep_num = ast.literal_eval(ep)
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
