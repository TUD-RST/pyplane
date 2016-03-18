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
__version__ = "1.0"

# this file contains the central class that inherits from the base gui class (VIEW) that
# was created using qt4-designer and pyuic4
# the class pyplaneMainWindow represents the CONTROLLER element of the mvc-structure

from PyQt4 import QtGui
from PyQt4 import QtCore
import traceback
import sys
import os

import sympy as sp
from IPython import embed
import numpy as np
import ast

from Ui_PyPlane import Ui_pyplane
from Ui_Pyplane_linearization import Ui_Form
from core.Logging import myLogger
from core.ConfigHandler import myConfig
from core.Graph import Graph
from core.Graph import Canvas
from core.System import mySystem, System
from core.NullclineHandler import myNullclines
from core.StreamlineHandler import myStreamlines
from core.VectorfieldHandler import myVectorfield, VectorfieldHandler
from core.EquilibriumHandler import myEquilibria
from core.TrajectoryHandler import myTrajectories
import core.PyPlaneHelpers as myHelpers


def handle_exception(error):

    myLogger.error_message("Error: An Python Exception occured.")
    myLogger.debug_message(str(type(error)))
    myLogger.debug_message(str(error))
    myLogger.message("See the log file config/logmessages.txt for full traceback ")

    exc_type, exc_value, exc_tb = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    tb_msg = "".join(lines)
    myLogger.append_to_file(tb_msg)


class PyplaneMainWindow(QtGui.QMainWindow, Ui_pyplane):
    def __init__(self, parent=None):
        super(PyplaneMainWindow, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('PyPlane %s' % __version__)

        myLogger.register_output(self.logField)

        # Check if LaTeX and dvipng is installed on the system. This
        # is required in order to ensure that advanced formatting in
        # matplotlib works correctly (\left, \begin{array} etc.)
        self.latex_installed = myHelpers.check_if_latex()

        self.myLayout1 = QtGui.QVBoxLayout(self.frame1)
        self.plotCanvas1 = Canvas(self.latex_installed, self.frame1)
        self.myLayout1.addWidget(self.plotCanvas1)

        self.myLayout2 = QtGui.QVBoxLayout(self.frame2)
        self.plotCanvas2 = Canvas(self.latex_installed, self.frame2)
        self.myLayout2.addWidget(self.plotCanvas2)

        self.myLayout3 = QtGui.QVBoxLayout(self.frame3)
        self.plotCanvas3 = Canvas(self.latex_installed, self.frame3)
        self.myLayout3.addWidget(self.plotCanvas3)

        self.myGraph = Graph(parent=self, plot_pp=self.plotCanvas1,
                             plot_x=self.plotCanvas2, plot_y=self.plotCanvas3)

        self.fct_stack = []
        self.linearization_stack = []

        self.xDotLabel.setText(u"\u1E8B(x,y) = ")
        self.yDotLabel.setText(u"\u1E8F(x,y) = ")

        try:
            test = myConfig.read("Test", "test_var")
        except:
            test = "Could not load config file. Please check existence"

        myLogger.debug_message("Loading config file: " + test)

    def init(self):
        """ This function gets called only after program start.
        """

        # load tmp file
        self.load_tmp_system()

        # set forward and backward integration true
        if myConfig.get_boolean("Trajectories", "traj_checkForwardByDefault"):
            self.forwardCheckbox.setChecked(True)
        if myConfig.get_boolean("Trajectories", "traj_checkBackwardByDefault"):
            self.backwardCheckbox.setChecked(True)
            
        self.initializing()

    def initializing(self):
        """ gets called after every submit call
        """

        self.PP_xminLineEdit.setText(str(myConfig.read("Phaseplane", "pp_xmin")))
        self.PP_xmaxLineEdit.setText(str(myConfig.read("Phaseplane", "pp_xmax")))
        self.PP_yminLineEdit.setText(str(myConfig.read("Phaseplane", "pp_ymin")))
        self.PP_ymaxLineEdit.setText(str(myConfig.read("Phaseplane", "pp_ymax")))
        self.myGraph.set_window_range(self.myGraph.plot_pp)

        self.X_tminLineEdit.setText(str(myConfig.read("x-t-plot", "x_tmin")))
        self.X_tmaxLineEdit.setText(str(myConfig.read("x-t-plot", "x_tmax")))
        self.X_xminLineEdit.setText(str(myConfig.read("x-t-plot", "x_xmin")))
        self.X_xmaxLineEdit.setText(str(myConfig.read("x-t-plot", "x_xmax")))
        self.myGraph.set_window_range(self.myGraph.plot_x)

        self.Y_tminLineEdit.setText(str(myConfig.read("y-t-plot", "y_tmin")))
        self.Y_tmaxLineEdit.setText(str(myConfig.read("y-t-plot", "y_tmax")))
        self.Y_yminLineEdit.setText(str(myConfig.read("y-t-plot", "y_ymin")))
        self.Y_ymaxLineEdit.setText(str(myConfig.read("y-t-plot", "y_ymax")))
        self.myGraph.set_window_range(self.myGraph.plot_y)

        #self.myGraph.update()
        myNullclines.update()
        myVectorfield.update()
        myStreamlines.update()

    def add_linearization_tab(self, equilibrium):
        # TODO: REFACTOR THIS FUNCTION!!!


        # if linearization has not been shown do so, otherwise ignore:
        if equilibrium not in self.linearization_stack:
            # TODO: This should actually be the same widget as
            #       phaseplane allowing the same behavior (click
            #       generates trajectories, etc.)
            # Set up the user interface from Designer.
            myWidget = Ui_Form()
            contents = QtGui.QWidget(self.tabWidget)
            myWidget.setupUi(contents)

            # add content to linearization tab!
            self.myLayout_Lin = QtGui.QVBoxLayout(myWidget.frame_lin)
            self.plotCanvas_Lin = Canvas(self.latex_installed, myWidget.frame_lin)
            self.myLayout_Lin.addWidget(self.plotCanvas_Lin)

            # window range should be equal to window range of phase plane
            #limits = self.myGraph.get_limits(self.myGraph.plot_pp)
            #print(limits)
            #self.myGraph.set_window_range(self.plotCanvas_Lin)

            # TODO make set_window_range-funtion reusable for this case
            xmin = float(self.PP_xminLineEdit.text())
            xmax = float(self.PP_xmaxLineEdit.text())
            ymin = float(self.PP_yminLineEdit.text())
            ymax = float(self.PP_ymaxLineEdit.text())

            self.plotCanvas_Lin.axes.set_xlim(xmin, xmax)
            self.plotCanvas_Lin.axes.set_ylim(ymin, ymax)

            # window range init
            section = "Phaseplane"
            token = "pp_"
            if myConfig.get_boolean(section, token + "showGrid"):
                self.plotCanvas_Lin.axes.grid()

            if myConfig.get_boolean(section, token + "showMinorTicks"):
                self.plotCanvas_Lin.axes.minorticks_on()
            else:
                self.plotCanvas_Lin.axes.minorticks_off()

            if not myConfig.get_boolean(section, token + "showXTicks"):
                self.plotCanvas_Lin.axes.xaxis.set_ticks([])

            if not myConfig.get_boolean(section, token + "showYTicks"):
                self.plotCanvas_Lin.axes.yaxis.set_ticks([])

            if myConfig.get_boolean(section, token + "showXLabel"):
                pp_label_fontsize = 9 #myConfig.read(section, token + "labelFontSize")
                xlabel = "$x$"
                self.plotCanvas_Lin.axes.set_xlabel(xlabel, fontsize=pp_label_fontsize)

            if myConfig.get_boolean(section, token + "showYLabel"):
                pp_label_fontsize = 9 #myConfig.read(section, token + "labelFontSize")
                ylabel = "$\\dot{x}$"
                self.plotCanvas_Lin.axes.set_ylabel(ylabel, fontsize=pp_label_fontsize)

            if not myConfig.get_boolean(section, token + "showSpines"):
                for spine in self.plotCanvas_Lin.axes.spines.itervalues():
                    spine.set_visible(False)

            #self.myGraph.plot_pp.mpl_connect('button_press_event', self.myGraph.onclick)

            # plot linearized vectorfield
            linearized_vectorfield = VectorfieldHandler()
            linearized_vectorfield.register_graph(None, self.plotCanvas_Lin)

            # create linearized system
            linearized_system = System()

            # set system properties
            jac = myEquilibria.approx_ep_jacobian(equilibrium)

            xe = equilibrium[0]
            ye = equilibrium[1]
            x_dot_string = str(jac[0,0]) + "*(x-(" + str(xe) + ")) + (" + str(jac[0,1]) + ")*(y-(" + str(ye) + "))"
            y_dot_string = str(jac[1,0]) + "*(x-(" + str(xe) + ")) + (" + str(jac[1,1]) + ")*(y-(" + str(ye) + "))"

            linearized_system.set_rhs(x_dot_string, y_dot_string)

            # set system for vectorfield
            linearized_vectorfield.set_system(linearized_system)

            #title_matrix = r"$A=\begin{Bmatrix}"+str(jac[0,0])+r" & "+str(jac[0,1])+r" \\"+str(jac[1,0])+r" & "+str(jac[1,1])+r"\end{Bmatrix}$"

            # set title
            lin_round = int(myConfig.read("Linearization", "lin_round_decimals")) # display rounded floats
            A00 = str(round(jac[0,0],lin_round))
            A01 = str(round(jac[0,1],lin_round))
            A11 = str(round(jac[1,1],lin_round))
            A10 = str(round(jac[1,0],lin_round))
            if self.latex_installed == True:
                title_matrix = r'$\underline{A}_{' + str(len(self.linearization_stack)) + r'} = \left( \begin{array}{ll} ' + A00 + r' & ' + A01 + r'\\ ' + A10 + r' & ' + A11 + r' \end{array} \right)$'
            else:
                title_matrix = r'$a_{11}(' + str(len(self.linearization_stack)) + r') =  ' + A00 + r', a_{12}(' + str(len(self.linearization_stack)) + r') = ' + A01 + '$\n $a_{21}( ' + str(len(self.linearization_stack)) + r') = ' + A10 +  r', a_{22}(' + str(len(self.linearization_stack)) + r') = ' + A11 + r'$'


            # calculating eigenvalues and eigenvectors:
            eigenvalues, eigenvectors = myEquilibria.get_eigenval_eigenvec(equilibrium)
            myLogger.message("Eigenvectors: (" + str(eigenvectors[0][0]) + ", " + str(eigenvectors[0][1]) + ") and (" + str(eigenvectors[1][0]) + ", " + str(eigenvectors[1][1]) + ")")

            # scaling
            d1 = (xmax-xmin)/10
            d2 = (ymax-ymin)/10
            d_large = (xmax-xmin)*(ymax-ymin)
            
            EV0 = np.array([np.real(eigenvectors[0][0]),np.real(eigenvectors[0][1])])
            EV0_norm = np.sqrt(EV0[0]**2+EV0[1]**2)
            EV0_scaled = np.array([d1*(1/EV0_norm)*EV0[0],d1*(1/EV0_norm)*EV0[1]])

            EV1 = np.array([np.real(eigenvectors[1][0]),np.real(eigenvectors[1][1])])
            EV1_norm = np.sqrt(EV1[0]**2+EV1[1]**2)
            EV1_scaled = np.array([d1*(1/EV1_norm)*EV1[0],d1*(1/EV1_norm)*EV1[1]])
            
            # plot eigenvectors:
            color_eigenvec = myConfig.read("Linearization", "lin_eigenvector_color")
            color_eigenline = myConfig.read("Linearization", "lin_eigenvector_linecolor")

            if myConfig.get_boolean("Linearization","lin_show_eigenline"):
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], d_large*EV0_scaled[0], d_large*EV0_scaled[1], head_width=0, head_length=0, color=color_eigenline)
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], -d_large*EV0_scaled[0], -d_large*EV0_scaled[1], head_width=0, head_length=0, color=color_eigenline)
            if myConfig.get_boolean("Linearization","lin_show_eigenvector"):
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], EV0_scaled[0], EV0_scaled[1], head_width=0, head_length=0, color=color_eigenvec)
            
            if myConfig.get_boolean("Linearization","lin_show_eigenline"):
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], d_large*EV1_scaled[0], d_large*EV1_scaled[1], head_width=0, head_length=0, color=color_eigenline)
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], -d_large*EV1_scaled[0], -d_large*EV1_scaled[1], head_width=0, head_length=0, color=color_eigenline)
            if myConfig.get_boolean("Linearization","lin_show_eigenvector"):
                self.plotCanvas_Lin.axes.arrow(equilibrium[0], equilibrium[1], EV1_scaled[0], EV1_scaled[1], head_width=0, head_length=0, color=color_eigenvec)


            # characterize EP:
            # stable focus:     SFOC
            # unstable focus:   UFOC
            # focus:            FOC
            # stable node:      SNOD
            # unstable node:    UNOD
            # saddle:           SAD

            determinant = jac[0,0]*jac[1,1] - jac[1,0]*jac[0,1]
            trace = jac[0,0] + jac[1,1]

            ep_character = ""

            if trace==0 and determinant==0:
                ep_character = "Unclassified"

            elif determinant < 0:
                ep_character = "Saddle"

            elif (determinant > 0) and (determinant < ((trace**2)/4)):
                if trace < 0:
                    ep_character = "Nodal Sink"
                elif trace > 0:
                    ep_character = "Nodal Source"

            elif determinant > ((trace**2)/4):
                if trace == 0:
                    ep_character = "Center"
                elif trace < 0:
                    ep_character = "Spiral Sink"
                elif trace > 0:
                    ep_character = "Spiral Source"
            elif determinant == ((trace**2)/4):
                if trace < 0:
                    ep_character = "Sink"
                elif trace > 0:
                    ep_character = "Source"

            if myConfig.get_boolean(section, token + "showTitle"):
                eq_x_rounded = str(round(equilibrium[0],lin_round))
                eq_y_rounded = str(round(equilibrium[1],lin_round))
                title1 = ep_character + r' at $(' + eq_x_rounded + r', ' + eq_y_rounded + r')$'
                #~ title1 = r'Equilibrium point ' + str(len(self.linearization_stack)) + r', ' + ep_character + r' at $(' + eq_x_rounded + r', ' + eq_y_rounded + r')$'
                #self.plotCanvas_Lin.axes.set_title(str(title1)+"$\n$\\dot{x} = " + x_dot_string + "$\n$\\dot{y} = " + y_dot_string + "$", loc='center')
                self.plotCanvas_Lin.axes.set_title(str(title1)+"\n"+title_matrix, fontsize=11)
            else:
                self.plotCanvas_Lin.fig.subplots_adjust(top=0.99)

            # mark EP in linearized tab
            self.plotCanvas_Lin.axes.plot(equilibrium[0], equilibrium[1],'ro')

            # add annotation in phaseplane
            label = str(ep_character)

            self.plotCanvas1.axes.text(equilibrium[0], equilibrium[1], label, fontsize=10)

            self.plotCanvas1.draw()

            # plot vectorfield
            linearized_vectorfield.update()

            self.plotCanvas_Lin.draw()

            title = str(ep_character)
            self.index = self.tabWidget.addTab(contents, title)

            self.linearization_stack.append(equilibrium)

            #QtCore.pyqtRemoveInputHook()
            #embed()


    def testfunction(self, equilibrium):
        print("equilibrium: "+str(equilibrium))

    def validate_expression(self, expression):
        # TODO: validation test expression
        pass

    def submit(self):
        """ This function gets called after clicking on the submit button
        """
        try:
            xtxt = str(self.xDotLineEdit.text())
            ytxt = str(self.yDotLineEdit.text())

        except UnicodeEncodeError as exc:
            myLogger.warn_message("UnicodeEncodeError! Please check input.")
            myLogger.debug_message(str(exc))

        else:
            cond1 = str(self.xDotLineEdit.text()) != ""
            cond2 = str(self.yDotLineEdit.text()) != ""

            if cond1 and cond2:
                self.tabWidget.setCurrentIndex(0) 
                # set right hand side, print rhs to logfield, solve,
                # then plot vector field

                # initialize system
                mySystem.__init__()

                # set rhs
                x_string = str(self.xDotLineEdit.text())
                y_string = str(self.yDotLineEdit.text())
                mySystem.set_rhs(x_string, y_string)

                try:
                    # write to tmp file:
                    self.save_system('library/tmp.ppf')

                    # clear figure, if there is any
                    self.myGraph.clear()

                    # delete linearization tabs (index 3 to n)
                    if len(self.linearization_stack) > 0:
                        for i in xrange(0, len(self.linearization_stack)):
                            index = 3 + len(self.linearization_stack) - i
                            self.tabWidget.removeTab(index)
                        #reset stack
                        self.linearization_stack = []
                        myLogger.debug_message("All linearization tabs removed.")


                    self.initializing()

                    myLogger.message("------ new system created ------")
                    myLogger.message("    x' = " + str(mySystem.what_is_my_system()[0]))
                    myLogger.message("    y' = " + str(mySystem.what_is_my_system()[1]) + "\n", )

                except Exception as error:
                    handle_exception(error)
            else:
                myLogger.error_message("No system entered")

    def load_system(self, file_name):
        """ load previous system (from tmp file) """

        with open(file_name, 'r') as sysfile:
            self.xDotLineEdit.setText(sysfile.readline().strip())
            self.yDotLineEdit.setText(sysfile.readline().strip())
            myLogger.message(file_name + " loaded")

    def load_tmp_system(self):
        self.load_system('library/tmp.ppf')

    def load_system_from_file(self):
        """ this function will load a system from a file """

        file_name = QtGui.QFileDialog.getOpenFileName(self,
                                                      'Open PyPlane File', '',
                                                      'PyPlane File (*.ppf)')
        if len(file_name) > 0:
            self.load_system(file_name)

    def save_file(self):

        file_name, filter = QtGui.QFileDialog.getSaveFileNameAndFilter(self,
                                                                       'Save PyPlane File', '',
                                                                       'PyPlane File (*.ppf)')
        self.save_system(file_name)

    def save_system(self, file_name):

        x_dot_string = str(self.xDotLineEdit.text())
        y_dot_string = str(self.yDotLineEdit.text())

        f_ending = '.ppf'
        f_len = len(file_name)

        if file_name[f_len - 4:f_len] == f_ending:
            with open(file_name, 'w') as sysfile:
                sysfile.write(x_dot_string + "\n" + y_dot_string)
        else:
            with open(file_name + f_ending, 'w') as sysfile:
                sysfile.write(x_dot_string + "\n" + y_dot_string)

        myLogger.message("system saved as " + file_name)

    def export_as(self):
        """ export dialog for pyplane plot
        """

        q_files_types = QtCore.QString(".png;;.svg;;.pdf;;.eps")
        q_file_name, q_file_type = QtGui.QFileDialog.getSaveFileNameAndFilter(self,
                                                                       "Export PyPlane Plot as .png, .svg, .pdf, or .eps-file", "",
                                                                       q_files_types)
        # Ensure we are out of the QString world in the following                                                               
        file_name = str(q_file_name)
        file_type = str(q_file_type)
            
        if file_name:
            # Fix: Under some KDE's the file_type is returned empty because
            # of a "DBUS-error". Hence, in such cases, we try to take the 
            # file_type from the extension specified by the user . If no valid extension 
            # is set by the user file_type is set to png. This bugfix is addressed
            # in the first part of the "if not" structure.
            #
            # In the else part of the "if not" structure the case is handled
            # where the user wants to have dots in the basename of the file
            # (affects all operating systems)
            #
            file_name2, file_type2 = os.path.splitext(file_name)
            if not file_type:
                if file_type2 not in [".png", ".svg", ".pdf", ".eps"]:                    
                    file_type = ".png"
                else:
                    # Allow things like figure.case21.pdf
                    file_name = file_name2
                    file_type = file_type2
            else:
                # This part runs on non KDE-systems or KDE-systems without
                # the DBUS error:                
                # drop accidently added duplicate file extensions
                # (avoid figure.png.png but allow figure.case1.png)
                if file_type2 == file_type:
                    file_name = file_name2
            # ------

            if file_type == ".png":
                self.export_as_png(file_name)
            elif file_type == ".svg":
                self.export_as_svg(file_name)
            elif file_type == ".pdf":
                self.export_as_pdf(file_name)
            elif file_type == ".eps":
                self.export_as_eps(file_name)
            else:
                myLogger.error_message("Filetype-Error")

    def update_window_range_lineedits(self):
        """ this function will update_all every window size line edit
        """

        # phase plane
        xmin1, xmax1, ymin1, ymax1 = self.myGraph.get_limits(self.myGraph.plot_pp)
        self.PP_xminLineEdit.setText(str(round(xmin1, 2)))
        self.PP_xmaxLineEdit.setText(str(round(xmax1, 2)))
        self.PP_yminLineEdit.setText(str(round(ymin1, 2)))
        self.PP_ymaxLineEdit.setText(str(round(ymax1, 2)))

        # x(t)
        xmin2, xmax2, ymin2, ymax2 = self.myGraph.get_limits(self.myGraph.plot_x)
        self.X_tminLineEdit.setText(str(round(xmin2, 2)))
        self.X_tmaxLineEdit.setText(str(round(xmax2, 2)))
        self.X_xminLineEdit.setText(str(round(ymin2, 2)))
        self.X_xmaxLineEdit.setText(str(round(ymax2, 2)))

        # y(t)
        xmin3, xmax3, ymin3, ymax3 = self.myGraph.get_limits(self.myGraph.plot_y)
        self.Y_tminLineEdit.setText(str(round(xmin3, 2)))
        self.Y_tmaxLineEdit.setText(str(round(xmax3, 2)))
        self.Y_yminLineEdit.setText(str(round(ymin3, 2)))
        self.Y_ymaxLineEdit.setText(str(round(ymax3, 2)))

    def export_as_png(self, filename):

        filename_pp = str(filename) + "_pp.png"
        self.myGraph.plot_pp.fig.savefig(filename_pp,
                                         bbox_inches='tight')

        filename_x = str(filename) + "_x.png"
        self.myGraph.plot_x.fig.savefig(filename_x, bbox_inches='tight')

        filename_y = str(filename) + "_y.png"
        self.myGraph.plot_y.fig.savefig(filename_y, bbox_inches='tight')

        myLogger.message(
            "plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_svg(self, filename):
        filename_pp = str(filename) + "_pp.svg"
        self.myGraph.plot_pp.fig.savefig(filename_pp, bbox_inches='tight')

        filename_x = str(filename) + "_x.svg"
        self.myGraph.plot_x.fig.savefig(filename_x, bbox_inches='tight')

        filename_y = str(filename) + "_y.svg"
        self.myGraph.plot_y.fig.savefig(filename_y, bbox_inches='tight')

        myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_eps(self, filename):
        filename_pp = str(filename) + "_pp.eps"

        self.myGraph.plot_pp.fig.savefig(filename_pp, bbox_inches='tight')

        filename_x = str(filename) + "_x.eps"
        self.myGraph.plot_x.fig.savefig(filename_x, bbox_inches='tight')

        filename_y = str(filename) + "_y.eps"
        self.myGraph.plot_y.fig.savefig(filename_y, bbox_inches='tight')

        myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_pdf(self, filename):
        filename_pp = str(filename) + "_pp.pdf"
        self.myGraph.plot_pp.fig.savefig(filename_pp, bbox_inches='tight')

        filename_x = str(filename) + "_x.pdf"
        self.myGraph.plot_x.fig.savefig(filename_x, bbox_inches='tight')

        filename_y = str(filename) + "_y.pdf"
        self.myGraph.plot_y.fig.savefig(filename_y, bbox_inches='tight')

        myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def add_function_to_plot(self):
        """ will plot additional functions and put it on a stack
        """
        self.x = sp.symbols('x')
        self.y = sp.symbols('y')
        self.fct = None

        try:
            fct_txt = str(self.yLineEdit.text())
        except UnicodeEncodeError as exc:
            myLogger.error_message("input error!")
            myLogger.debug_message(str(exc))

        if fct_txt != "":
            try:
                self.fct_string = str(self.yLineEdit.text())

                self.fct_expr = sp.sympify(self.fct_string)
                # self.fct = sp.lambdify(self.x,self.fct_expr,'numpy')
                self.fct = sp.lambdify((self.x, self.y), self.fct_expr, 'numpy')
                xmin, xmax, ymin, ymax = self.myGraph.get_limits(self.myGraph.plot_pp)

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

                #yvalue = self.fct(xvalue)

                myfunc = self.fct(X, Y)
                # TODO: plots like y=1/x have a connection between -inf and +inf that is not actually there!

                # plot function and put on function-stack
                new_fct = self.myGraph.plot_pp.axes.contour(X, Y, myfunc, [0],
                                                            zorder=100,
                                                            linewidths=fct_linewidth,
                                                            colors=fct_color)
                # new_fct = self.myGraph.plot_pp.axes.plot(xvalue, yvalue, label="fct", color="green")
                self.fct_stack.append(new_fct)

                self.myGraph.update_graph(self.myGraph.plot_pp)
                myLogger.message("function plot: 0 = " + self.fct_string)

            except Exception as error:
                handle_exception(error)
        else:
            myLogger.error_message("Please enter function.")

    def remove_function_from_plot(self):
        if len(self.fct_stack) != 0:
            for i in xrange(0, len(self.fct_stack)):
                fct = self.fct_stack.pop().collections
                for j in xrange(0, len(fct)):
                    try:
                        fct[j].remove()
                    except Exception as error:
                        myLogger.debug_message("couldn't delete function")
                        myLogger.debug_message(str(type(error)))
                        myLogger.debug_message(str(error))
            myLogger.message("functions removed")
        else:
            myLogger.debug_message("no function to delete")

        self.myGraph.update_graph(self.myGraph.plot_pp)

#     def addFctClear(self):
#         """ will remove every additional function
#         """
#         if len(self.fct_stack)!=0:
#             for i in xrange(0,len(self.fct_stack)):
#                 try:
#                     self.fct_stack.pop()[0].remove()
#                 except Exception as error:
#                     myLogger.debug_message("couldn't delete function plot")
#                     myLogger.debug_message(str(type(error)))
#                     myLogger.debug_message(str(error))
#
#             myLogger.message("function plots removed")
#             self.myGraph.update_graph(self.myGraph.plot_pp)
#         else:
#             myLogger.warn_message("no additional function has been plotted")

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    window_object = PyplaneMainWindow()
    window_object.showFullScreen()
    window_object.show()
    app.exec_()
