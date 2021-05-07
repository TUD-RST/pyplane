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

# this file contains the central class that inherits from the base gui class (VIEW) that
# was created using qt5-designer and pyuic5
# the class pyplaneMainWindow represents the CONTROLLER element of the mvc-structure

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import traceback
import sys
import os
import sympy as sp
import numpy as np
from .Ui_PyPlane import Ui_pyplane
from ..core.Logging import myLogger
from ..core.ConfigHandler import myConfig
from ..core.System import System
from ..core import PyPlaneHelpers as myHelpers
from .Widgets import SettingsWidget

__author__ = 'Klemens Fritzsche'


basedir = os.path.dirname(os.path.dirname(sys.modules.get(__name__).__file__))
librarydir = os.path.join(basedir, 'library')
TMP_PATH = os.path.join(basedir, 'library', 'tmp.ppf')


def handle_exception(error):
    myLogger.error_message("Error: An Python Exception occured.")
    myLogger.debug_message(str(type(error)))
    myLogger.debug_message(str(error))
    myLogger.message("See the log file config/logmessages.txt for full traceback ")

    exc_type, exc_value, exc_tb = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    tb_msg = "".join(lines)
    myLogger.append_to_file(tb_msg)


class PyplaneMainWindow(QtWidgets.QMainWindow, Ui_pyplane):
    def __init__(self, parent=None):
        super(PyplaneMainWindow, self).__init__()
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('PyPlane')

        myLogger.register_output(self.logField)

        # Check if LaTeX and dvipng is installed on the system. This
        # is required in order to ensure that advanced formatting in
        # matplotlib works correctly (\left, \begin{array} etc.)
        self.latex_installed = myHelpers.check_if_latex()

        # Embed SettingsWidget:
        self.mySettings = SettingsWidget()
        self.SettingsLayout.addWidget(self.mySettings)

        self.fct_stack = []
        self.linearization_stack = []

        self.systems = []

        self.xDotLabel.setText("\u1E8B(x,y) = ")
        self.yDotLabel.setText("\u1E8F(x,y) = ")

        try:
            test = myConfig.read("Test", "test_var")
        except:
            test = "Could not load config file. Please check existence"

        myLogger.debug_message(f"Current working dir: {os.path.abspath(os.curdir)}")
        myLogger.debug_message("Loading config file: " + test)


    def init(self):
        """ This function gets called only after program start.
        """
        # load tmp file
        try:
            self.load_tmp_system()
            self.disable_menu_items()
        except:
            pass

    def disable_menu_items(self):
        # uncheck items
        self.toggle_vectorfield_action.setChecked(False)
        self.toggle_streamlines_action.setChecked(False)
        self.toggle_equilibrium_action.setChecked(False)
        self.toggle_nullclines_action.setChecked(False)
        # shade out items:
        self.toggle_vectorfield_action.setEnabled(False)
        self.toggle_streamlines_action.setEnabled(False)
        self.toggle_equilibrium_action.setEnabled(False)
        if hasattr(self, "linearize_action"):
            self.linearize_action.setEnabled(False)
        self.toggle_nullclines_action.setEnabled(False)

    def update_ui(self):
        # unshade items
        self.toggle_vectorfield_action.setEnabled(True)
        self.toggle_streamlines_action.setEnabled(True)
        self.toggle_equilibrium_action.setEnabled(True)
        self.toggle_nullclines_action.setEnabled(True)

        # check items
        system = self.get_current_system()
        if hasattr(system, "Phaseplane"):
            if hasattr(system.Phaseplane, "VF"):
                self.toggle_vectorfield_action.setChecked(system.Phaseplane.VF.tgl)
            if hasattr(system.Phaseplane, "SL"):
                self.toggle_streamlines_action.setChecked(system.Phaseplane.SL.tgl)
            if hasattr(system.Phaseplane, "Equilibria"):
                self.toggle_equilibrium_action.setChecked(system.Phaseplane.Equilibria.tgl)
            if hasattr(system.Phaseplane, "Nullclines"):
                self.toggle_nullclines_action.setChecked(system.Phaseplane.Nullclines.tgl)
            # equation:
            self.xDotLineEdit.setText(system.equation.x_dot_string)
            self.yDotLineEdit.setText(system.equation.y_dot_string)

    def initialize_ui(self):
        # gets called after submitting a system (updae_ui() cannot be
        # used since the new system tab is not visible yet
        # values are taken from config file

        self.toggle_vectorfield_action.setChecked(myConfig.get_boolean("Vectorfield", "vf_onByDefault"))
        self.toggle_streamlines_action.setChecked(myConfig.get_boolean("Streamlines", "stream_onByDefault"))
        self.toggle_equilibrium_action.setChecked(False)
        self.toggle_nullclines_action.setChecked(myConfig.get_boolean("Nullclines", "nc_onByDefault"))

    def new_linearized_system(self, equation, name, equilibrium):
        xe, ye = equilibrium
        system = System(self, equation, name=name, linear=True)
        self.systems.insert(0, system)
        system.plot_eigenvectors(equilibrium)

        myLogger.message("------ new linearized system created at xe = " + str(xe) + ", ye = " + str(ye) + " ------")
        myLogger.message("    x' = " + str(system.equation.what_is_my_system()[0]))
        myLogger.message("    y' = " + str(system.equation.what_is_my_system()[1]) + "\n", )

    def close_current_tab(self):
        index = self.tabWidget.currentIndex()
        if index != self.tabWidget.count() - 1:
            self.tabWidget.removeTab(index)
            self.systems.pop(index)
        self.update_ui()

    def close_all_tabs(self):
        for i in range(self.tabWidget.count() - 1):
            self.tabWidget.removeTab(i)
            # TODO: Delete Data
        self.update_ui()

    def new_system(self, equation):
        system = System(self, equation)
        self.systems.insert(0, system)

    def submit(self):
        """ This function gets called after clicking on the submit button
        """
        myLogger.message("New system submitted...")
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
                x_string = str(self.xDotLineEdit.text())
                y_string = str(self.yDotLineEdit.text())

                try:
                    # Non-modal (!) Box intended for calming down the user...
                    info_box = QtWidgets.QMessageBox(self)
                    info_box.setAttribute(Qt.WA_DeleteOnClose)
                    info_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    info_box.setIcon(QtWidgets.QMessageBox.Information)
                    info_box.setWindowTitle("New system submitted")
                    info_box.setText("The new system is being processed now, please wait! \n"
                                     "Especially when LaTeX is used for the labels this may take some time and the "
                                     "program might seem unresponsive!")
                    info_box.setModal(False)
                    info_box.show()
                    QtCore.QCoreApplication.processEvents()

                    # Processing equations
                    equation = (x_string, y_string)
                    system = System(self, equation)
                    self.systems.insert(0, system)
                    self.save_tmp_system()

                    myLogger.message("------ new system created ------")
                    myLogger.message("    x' = " + str(system.equation.what_is_my_system()[0]))
                    myLogger.message("    y' = " + str(system.equation.what_is_my_system()[1]) + "\n", )

                    try:
                        info_box.close()
                    except RuntimeError:  # if dialog has already been closed by the user
                        pass

                except BaseException as exc:
                    QtWidgets.QMessageBox.critical(self, "Error!", "An error occured while processing the system. "
                                                                   "Detailed error message: \n %s" % exc)
                    myLogger.error_message(str(exc))
            else:
                myLogger.error_message("Please check system!")

    def load_system(self, file_name):
        """ load previous system (from tmp file) """

        with open(file_name, 'r') as sysfile:
            # TODO: This does not work, but how would i find a way to store a system?
            # pps_file = pcl.loads(sysfile.read())
            # system = System(self)
            # system.unpickle(pps_file)
            # self.systems.insert(0, system)
            # self.xDotLineEdit.setText(sysfile.readline().strip())
            # self.yDotLineEdit.setText(sysfile.readline().strip())
            xdot_string = str(sysfile.readline())
            ydot_string = str(sysfile.readline())
            self.xDotLineEdit.setText(xdot_string.strip())
            self.yDotLineEdit.setText(ydot_string.strip())
            myLogger.message(file_name + " loaded")

    def load_tmp_system(self):
        self.load_system(TMP_PATH)

    def load_system_from_file(self):
        orig_dir = os.path.abspath(os.curdir)
        os.chdir(librarydir)
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open pyplane file', '', 'pyplane file (*.ppf)')
        os.chdir(orig_dir)

        # Function returns on some platforms a tuple: First element -> file name, second element -> filter
        # We do only need the filter
        if type(file_name) == tuple:
            file_name = file_name[0]

        if len(file_name) > 0:
            self.load_system(file_name)
            self.submit()
            self.update_ui()

    def save_tmp_system(self):
        if len(self.systems) > 0:
            index = self.tabWidget.currentIndex()
            system = self.systems[index]
            file_name = TMP_PATH
            self.save_system(file_name, system.equation.what_is_my_system())
        else:
            myLogger.error_message("There is no system to save!")

    def save_file(self):
        if len(self.systems) > 0:
            index = self.tabWidget.currentIndex()
            system = self.systems[index]
            file_name, file_type = QtWidgets.QFileDialog.getSaveFileName(self, "Save pyplane file", "",
                                                                               "pyplane file (*.ppf)")
            # sys_pickleds = system.pickle(file_name)
            # system.equation.what_is_my_system()
            self.save_system(file_name, system.equation.what_is_my_system())
        else:
            myLogger.error_message("There is no system to save!")

    def save_system(self, file_name, system):
        x_dot_string = str(system[0])
        y_dot_string = str(system[1])
        f_ending = '.ppf'
        f_len = len(file_name)

        if file_name[f_len - 4:f_len] == f_ending:
            with open(file_name, 'w') as sysfile:
                sysfile.write(x_dot_string + "\n" + y_dot_string)
        else:
            with open(file_name + f_ending, 'w') as sysfile:
                sysfile.write(x_dot_string + "\n" + y_dot_string)

        myLogger.message("System saved as " + file_name)

    def export_as(self):
        """ export dialog for pyplane plot
        """

        files_types = ".png;;.svg;;.pdf;;.eps"
        file_name, file_type = \
            QtWidgets.QFileDialog.getSaveFileName(self, "Export PyPlane Plot as .png, .svg, .pdf, or .eps-file", "",
                                                  files_types)

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
        system = self.get_current_system()
        if system != None:
            filename_pp = str(filename) + "_pp.png"
            system.Phaseplane.Plot.canvas.fig.savefig(filename_pp,
                                                      bbox_inches='tight')

            filename_x = str(filename) + "_x.png"
            system.Xt.Plot.canvas.fig.savefig(filename_x, bbox_inches='tight')

            filename_y = str(filename) + "_y.png"
            system.Yt.Plot.canvas.fig.savefig(filename_y, bbox_inches='tight')

            myLogger.message(
                "plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_svg(self, filename):
        system = self.get_current_system()
        if system != None:
            filename_pp = str(filename) + "_pp.svg"
            system.Phaseplane.Plot.canvas.fig.savefig(filename_pp, bbox_inches='tight')

            filename_x = str(filename) + "_x.svg"
            system.Xt.Plot.canvas.fig.savefig(filename_x, bbox_inches='tight')

            filename_y = str(filename) + "_y.svg"
            system.Yt.Plot.canvas.fig.savefig(filename_y, bbox_inches='tight')

            myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_eps(self, filename):
        system = self.get_current_system()
        if system != None:
            filename_pp = str(filename) + "_pp.eps"

            system.Phaseplane.Plot.canvas.fig.savefig(filename_pp, bbox_inches='tight')

            filename_x = str(filename) + "_x.eps"
            system.Xt.Plot.canvas.fig.savefig(filename_x, bbox_inches='tight')

            filename_y = str(filename) + "_y.eps"
            system.Yt.Plot.canvas.fig.savefig(filename_y, bbox_inches='tight')

            myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def export_as_pdf(self, filename):
        system = self.get_current_system()
        if system != None:
            filename_pp = str(filename) + "_pp.pdf"
            system.Phaseplane.Plot.canvas.fig.savefig(filename_pp, bbox_inches='tight')

            filename_x = str(filename) + "_x.pdf"
            system.Xt.Plot.canvas.fig.savefig(filename_x, bbox_inches='tight')

            filename_y = str(filename) + "_y.pdf"
            system.Yt.Plot.canvas.fig.savefig(filename_y, bbox_inches='tight')

            myLogger.message("plot exported as\n\t" + filename_pp + ",\n\t" + filename_x + ",\n\t" + filename_y)

    def add_function_to_plot(self):
        """ will plot additional functions and put it on a stack
        """
        self.x = sp.symbols('x')
        self.y = sp.symbols('y')
        self.fct = None

        fct_txt = ""
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

                # yvalue = self.fct(xvalue)

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

        self.myGraph.update_graph(self.myGraph.plot_pp)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window_object = PyplaneMainWindow()
    window_object.showFullScreen()
    window_object.show()
    app.exec_()
