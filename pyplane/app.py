# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013
    by Klemens Fritzsche, pyplane@leckstrom.de

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from .core.ConfigHandler import myConfig
from .gui.App_PyPlane import PyplaneMainWindow
from .gui.Dlg_PyPlane_about import AboutDialog
from .core.Logging import myLogger

__author__ = 'Klemens Fritzsche, Jan Winkler'


# noinspection PyUnresolvedReferences
class MainApp(PyplaneMainWindow):
    """ This class contains toplevel application logic and takes care of:
        GUI changes (only overwriting xDotLabel and yDotLabel at the moment)
        connect buttons with functions,
        create a file menu,
        initializing,
        settings GUI logic (listview elements, variable description, etc)
    """

    __PYPLANE_VERSION = "2.0.2"
    __PYPLANE_DATE = "2022-05-25"

    def __init__(self):
        # superclass constructor
        PyplaneMainWindow.__init__(self)
        QtCore.pyqtRemoveInputHook()

        # Set Version-number
        self.setWindowTitle("PyPlane " + self.__PYPLANE_VERSION)

        # check config file if shown by default
        self.terminal_toggle = myConfig.get_boolean("Logging", "log_showTerminal")
        self.update_terminal()

        # # connect buttons ------------------------------------------------------
        # # connect buttons: system
        self.clearButton.clicked.connect(self.clear_trajectories)
        self.submitButton.clicked.connect(self.submit)

        # # connect buttons: additional function
        self.FctPlotButton.clicked.connect(self.add_function)
        self.FctClearButton.clicked.connect(self.remove_functions)

        # file menu ------------------------------------------------------
        # file
        self.file_menu = QtWidgets.QMenu('&System', self)

        self.load = QtWidgets.QMenu('&Open', self)
        self.file_menu.addMenu(self.load)
        self.load.addAction('&Recent', self.load_tmp_system)
        self.load.addAction('&From File', self.load_system_from_file,
                            QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&Save As...', self.save_file,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Export As...', self.export_as, QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.file_menu.addAction('&Close', self.close_current_tab, QtCore.Qt.CTRL + QtCore.Qt.Key_W)
        # self.file_menu.addAction('&Close All', self.close_all_tabs, QtCore.Qt.CTRL + QtCore.Qt.ShiftModifier + QtCore.Qt.Key_W)
        self.file_menu.addAction('&Quit', self.file_quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # show
        self.show_menu = QtWidgets.QMenu('&Show', self)
        self.menuBar().addMenu(self.show_menu)

        # terminal checkbox
        self.toggle_terminal_action = QtWidgets.QAction('Terminal', self.show_menu)
        self.toggle_terminal_action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_T)
        self.toggle_terminal_action.setCheckable(True)
        if myConfig.get_boolean("Logging", "log_showTerminal"):
            self.toggle_terminal_action.setChecked(True)
        self.toggle_terminal_action.triggered.connect(self.toggle_terminal)
        self.show_menu.addAction(self.toggle_terminal_action)

        # vector field checkbox
        self.toggle_vectorfield_action = QtWidgets.QAction('&Plot Vector Field', self.show_menu)
        self.toggle_vectorfield_action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_V)
        self.toggle_vectorfield_action.setCheckable(True)
        # if myConfig.get_boolean("Vectorfield", "vf_onByDefault"):
        #    self.toggle_vectorfield_action.setChecked(True)
        self.toggle_vectorfield_action.triggered.connect(self.vf_helper_function)
        self.show_menu.addAction(self.toggle_vectorfield_action)

        # streamlines checkbox
        self.toggle_streamlines_action = QtWidgets.QAction('&Plot Streamlines', self.show_menu)
        self.toggle_streamlines_action.setCheckable(True)
        # if myConfig.get_boolean("Streamlines", "stream_onByDefault"):
        #    self.toggle_streamlines_action.setChecked(True)
        self.toggle_streamlines_action.triggered.connect(self.sl_helper_function)
        self.show_menu.addAction(self.toggle_streamlines_action)

        # equilibrium checkbox
        self.toggle_equilibrium_action = QtWidgets.QAction('&Find an Equilibrium Point / Linearize', self.show_menu)
        self.toggle_equilibrium_action.setCheckable(True)
        # self.toggle_equilibrium_action.setChecked(False)
        self.toggle_equilibrium_action.triggered.connect(self.eq_helper_function)
        self.show_menu.addAction(self.toggle_equilibrium_action)
        # self.show_menu.addAction('&Find an Equilibrium Point', self.myGraph.toggleEP)

        # linearize checkbox
        # self.linearize_action = QtWidgets.QAction('&Linearize', self.show_menu)
        # self.linearize_action.triggered.connect(self.linearize_helper_function)
        # self.show_menu.addAction(self.linearize_action)

        # nullclines checkbox
        self.toggle_nullclines_action = QtWidgets.QAction('Nullclines', self.show_menu)
        self.toggle_nullclines_action.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        self.toggle_nullclines_action.setCheckable(True)
        # if system exists: read toggle-value
        # if not: read from config
        # TODO: new systems tab chosen -> check/uncheck toggle!
        # if self.systems == []:
        # read current systems tab:
        # if myConfig.get_boolean("Nullclines", "nc_onByDefault"):
        # self.toggle_nullclines_action.setChecked(True)
        self.toggle_nullclines_action.triggered.connect(self.toggle_nullclines)
        self.show_menu.addAction(self.toggle_nullclines_action)

        # self.show_menu.addAction('&Calculate Nullclines (symbolic)', myNullclines.print_symbolic_nullclines)

        # help
        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction('&About', self.about)

        # initializing with default values ------------------------------------------------------
        self.init()
        # self.build_settings_tab()

        # from now on, plot only log messages as defined in config file.
        # for that, call initialize function in myLogger
        myLogger.initialize()

    def clear_trajectories(self):
        system = self.get_current_system()
        if system != None:
            system.Trajectories.remove_all()

    def add_function(self):
        system = self.get_current_system()
        if system != None:
            system.Functions.add()

    def remove_functions(self):
        system = self.get_current_system()
        if system != None:
            system.Functions.remove_all()

    def vf_helper_function(self):
        system = self.get_current_system()
        if system != None:
            if system.Phaseplane.SL.tgl and not system.Phaseplane.VF.tgl:
                system.Phaseplane.SL.toggle()
            system.Phaseplane.VF.toggle()
            self.update_ui()

    def sl_helper_function(self):
        system = self.get_current_system()
        if system != None:
            if system.Phaseplane.VF.tgl and not system.Phaseplane.SL.tgl:
                system.Phaseplane.VF.toggle()
            system.Phaseplane.SL.toggle()
            self.update_ui()

    def eq_helper_function(self):
        system = self.get_current_system()
        if system != None:
            system.Phaseplane.Equilibria.toggle()
            self.update_ui()

    # def linearize_helper_function(self):
    # system = self.get_current_system()
    # if system != None:
    # system.Phaseplane.toggle_linearization_objects()

    def toggle_nullclines(self):
        system = self.get_current_system()
        if system != None:
            system.Phaseplane.Nullclines.toggle()
        self.update_ui()

    def get_current_system(self):
        index = self.tabWidget.currentIndex()
        if (len(self.systems) > 0) and (index != len(self.systems)):
            system = self.systems[index]
            return system
        else:
            myLogger.debug_message("No system chosen.")
            return None

    def toggle_terminal(self):
        self.terminal_toggle = not self.terminal_toggle
        self.update_terminal()

    def update_terminal(self):
        if not self.terminal_toggle:
            self.logField.setFixedHeight(0)
        else:
            self.logField.setFixedHeight(100)

    def file_quit(self):
        self.close()

    def about(self):
        AboutDialog(self.__PYPLANE_VERSION, self.__PYPLANE_DATE)


def run():
    app = QtWidgets.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
