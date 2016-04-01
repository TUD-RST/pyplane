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

import sys
import ast

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtGui
from PyQt4 import QtCore

from core.ConfigHandler import myConfig
from gui.App_PyPlane import PyplaneMainWindow
from gui.Dlg_PyPlane_about import AboutDialog
from core.Logging import myLogger
from core.EquilibriumHandler import myEquilibria
from core.NullclineHandler import myNullclines
from core.TrajectoryHandler import myTrajectories
from core.StreamlineHandler import myStreamlines
from core.VectorfieldHandler import myVectorfield

# This import is required by PyInstaller in order to produce a
# correctly working executable
import FileDialog


# noinspection PyUnresolvedReferences
class MainApp(PyplaneMainWindow):
    """ This class contains toplevel application logic and takes care of:
        GUI changes (only overwriting xDotLabel and yDotLabel at the moment)
        connect buttons with functions,
        create a file menu,
        initializing,
        settings GUI logic (listview elements, variable description, etc)
    """
    
    __PYPLANE_VERSION = "1.0"
    __PYPLANE_DATE = "31.07.2015"

    def __init__(self):
        # superclass constructor
        PyplaneMainWindow.__init__(self)
        QtCore.pyqtRemoveInputHook()

        # check config file if shown by default
        self.terminal_toggle = myConfig.get_boolean("Logging", "showTerminal")
        self.update_terminal()
        
        #~ # connect buttons ------------------------------------------------------
        #~ # connect buttons: system
        #~ self.clearButton.clicked.connect(myTrajectories.remove_all)
        self.submitButton.clicked.connect(self.submit)

        #~ # connect buttons: phase plane
        #~ self.PP_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_pp))
        #~ self.PP_ZoomButton.clicked.connect(self.myGraph.plot_pp.toggle_zoom_mode)
        #~ self.PP_ZoomButton.setCheckable(True)
        #~ self.PP_RefreshButton.clicked.connect(self.myGraph.refresh)
        #~ self.PP_CreateTrajectoryButton.clicked.connect(myTrajectories.create_trajectory)

        #~ # connect buttons: x(t)
        #~ self.X_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_x))
        #~ self.X_ZoomButton.clicked.connect(self.myGraph.plot_x.toggle_zoom_mode)
        #~ self.X_ZoomButton.setCheckable(True)
        #~ # self.X_ZoomButton.clicked.connect(self.plotCanvas2.zoomMode)

        #~ # connect buttons: y(t)
        #~ self.Y_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_y))
        #~ self.Y_ZoomButton.clicked.connect(self.myGraph.plot_y.toggle_zoom_mode)
        #~ self.Y_ZoomButton.setCheckable(True)

        #~ # connect buttons: additional function
        #~ self.FctPlotButton.clicked.connect(self.add_function_to_plot)
        #~ self.FctClearButton.clicked.connect(self.remove_function_from_plot)

        #~ # connect mouse events (left mouse button click) in phase plane
        #~ self.myGraph.plot_pp.mpl_connect('button_press_event', self.myGraph.onclick)
        #~ self.myGraph.plot_pp.mpl_connect('pick_event', self.myGraph.onpick)

        # file menu ------------------------------------------------------
        # file
        self.file_menu = QtGui.QMenu('&System', self)

        self.load = QtGui.QMenu('&Open', self)
        self.file_menu.addMenu(self.load)
        self.load.addAction('&Recent', self.load_tmp_system)
        self.load.addAction('&From File', self.load_system_from_file,
                            QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&Save As...', self.save_file,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Export As...', self.export_as, QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.file_menu.addAction('&Close', self.close_current_tab, QtCore.Qt.CTRL + QtCore.Qt.Key_W)
        #~ self.file_menu.addAction('&Close All', self.close_all_tabs, QtCore.Qt.CTRL + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_W)
        self.file_menu.addAction('&Quit', self.file_quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # show
        self.show_menu = QtGui.QMenu('&Show', self)
        self.menuBar().addMenu(self.show_menu)

        # terminal checkbox
        self.toggle_terminal_action = QtGui.QAction('Terminal', self.show_menu)
        #~ from PyQt4 import QtCore
        #~ from IPython import embed
        #~ QtCore.pyqtRemoveInputHook()
        #~ embed()
        self.toggle_terminal_action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_T)
        self.toggle_terminal_action.setCheckable(True)
        #self.toggle_nullclines_action.setShortcuts(
        if myConfig.get_boolean("Logging", "showTerminal"):
            self.toggle_terminal_action.setChecked(True)
        # noinspection PyUnresolvedReferences
        self.toggle_terminal_action.triggered.connect(self.toggle_terminal)
        self.show_menu.addAction(self.toggle_terminal_action)

        # vector field checkbox
        self.toggle_vectorfield_action = QtGui.QAction('&Plot Vector Field', self.show_menu)
        self.toggle_vectorfield_action.setCheckable(True)
        if myConfig.get_boolean("Vectorfield", "vf_onByDefault"):
            self.toggle_vectorfield_action.setChecked(True)
        # noinspection PyUnresolvedReferences
        self.toggle_vectorfield_action.triggered.connect(self.vf_helper_function)
        self.show_menu.addAction(self.toggle_vectorfield_action)

        # streamlines checkbox
        self.toggle_streamlines_action = QtGui.QAction('&Plot Streamlines', self.show_menu)
        self.toggle_streamlines_action.setCheckable(True)
        if myConfig.get_boolean("Streamlines", "stream_onByDefault"):
            self.toggle_streamlines_action.setChecked(True)
        self.toggle_streamlines_action.triggered.connect(self.sl_helper_function)
        self.show_menu.addAction(self.toggle_streamlines_action)

        # equilibrium checkbox
        self.toggle_equilibrium_action = QtGui.QAction('&Find an Equilibrium Point / Linearize', self.show_menu)
        self.toggle_equilibrium_action.setCheckable(True)
        self.toggle_equilibrium_action.setChecked(False)
        self.toggle_equilibrium_action.triggered.connect(myEquilibria.toggle)
        self.show_menu.addAction(self.toggle_equilibrium_action)
        #self.show_menu.addAction('&Find an Equilibrium Point', self.myGraph.toggleEP)

        # nullclines checkbox
        self.toggle_nullclines_action = QtGui.QAction('Nullclines', self.show_menu)
        self.toggle_nullclines_action.setCheckable(True)
        if myConfig.get_boolean("Nullclines", "nc_onByDefault"):
            self.toggle_nullclines_action.setChecked(True)
        self.toggle_nullclines_action.triggered.connect(myNullclines.toggle)
        self.show_menu.addAction(self.toggle_nullclines_action)

        self.show_menu.addAction('&Calculate Nullclines (symbolic)', myNullclines.print_symbolic_nullclines)

        # help
        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)

        # initializing with default values ------------------------------------------------------
        self.init()
        #~ self.build_settings_tab()

        # from now on, plot only log messages as defined in config file.
        # for that, call initialize function in myLogger
        myLogger.initialize()

    # this helper function untoggles the vector field checkbox
    def vf_helper_function(self):
        self.myGraph.toggle_vectorfield()
        self.helper_function()

        # this helper function untoggles the streamline checkbox

    def sl_helper_function(self):
        self.myGraph.toggle_streamlines()
        self.helper_function()

    def helper_function(self):
        self.toggle_vectorfield_action.setChecked(myVectorfield.tgl)
        self.toggle_streamlines_action.setChecked(myStreamlines.tgl)

    def toggle_terminal(self):
        self.terminal_toggle = not self.terminal_toggle
        self.update_terminal()

    def update_terminal(self):
        if not self.terminal_toggle:
            self.logField.setFixedHeight(0)
        else:
            self.logField.setFixedHeight(100)

    def file_quit(self):
        # quit pyplane
        self.close()

    def about(self):
        AboutDialog(self.__PYPLANE_VERSION, self.__PYPLANE_DATE)
        
#        QtGui.QMessageBox.about(self, "About", (
#                                "\n"
#                                "    PyPlane 0.1.7\n"
#                                "\n"
#                                "    Copyright (C) 2013-2014\n"
#                                "    by Klemens Fritzsche, Carsten Knoll\n"
#                                "\n"
#                                "    Dresden University of Technology\n"
#                                "    Institute of Control Theory\n"
#                                "\n"
#                                "    This code is free software, licensed under the terms of the\n"
#                                "    GNU General Public License, version 3\n"
#                                "    <http://www.gnu.org/license/>.\n"
#                                "\n")
#        )

app = QtGui.QApplication(sys.argv)
main = MainApp()
main.show()
sys.exit(app.exec_())
