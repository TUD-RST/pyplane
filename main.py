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
from PyQt4 import QtGui
from PyQt4 import QtCore

from core.ConfigHandler import myConfig
from gui.App_PyPlane import PyplaneMainWindow
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

    def __init__(self):
        # superclass constructor
        PyplaneMainWindow.__init__(self)
        QtCore.pyqtRemoveInputHook()

        # check config file if shown by default
        self.terminal_toggle = myConfig.get_boolean("Logging", "showTerminal")
        self.update_terminal()

        # connect buttons ------------------------------------------------------
        # connect buttons: system
        self.clearButton.clicked.connect(myTrajectories.remove_all)
        self.submitButton.clicked.connect(self.submit)

        # connect buttons: phase plane
        self.PP_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_pp))
        self.PP_ZoomButton.clicked.connect(self.myGraph.plot_pp.toggle_zoom_mode)
        self.PP_ZoomButton.setCheckable(True)
        self.PP_RefreshButton.clicked.connect(self.myGraph.refresh)
        self.PP_CreateTrajectoryButton.clicked.connect(myTrajectories.create_trajectory)

        # connect buttons: x(t)
        self.X_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_x))
        self.X_ZoomButton.clicked.connect(self.myGraph.plot_x.toggle_zoom_mode)
        self.X_ZoomButton.setCheckable(True)
        # self.X_ZoomButton.clicked.connect(self.plotCanvas2.zoomMode)

        # connect buttons: y(t)
        self.Y_SetButton.clicked.connect(lambda: self.myGraph.set_window_range(self.myGraph.plot_y))
        self.Y_ZoomButton.clicked.connect(self.myGraph.plot_y.toggle_zoom_mode)
        self.Y_ZoomButton.setCheckable(True)

        # connect buttons: additional function
        self.FctPlotButton.clicked.connect(self.add_function_to_plot)
        self.FctClearButton.clicked.connect(self.remove_function_from_plot)

        # connect mouse events (left mouse button click) in phase plane
        self.myGraph.plot_pp.mpl_connect('button_press_event', self.myGraph.onclick)
        self.myGraph.plot_pp.mpl_connect('pick_event', self.myGraph.onpick)

        # file menu ------------------------------------------------------
        # file
        self.file_menu = QtGui.QMenu('&File', self)

        self.load = QtGui.QMenu('&Open', self)
        self.file_menu.addMenu(self.load)
        self.load.addAction('&Recent', self.load_tmp_system)
        self.load.addAction('&From File', self.load_system_from_file,
                            QtCore.Qt.CTRL + QtCore.Qt.Key_O)

        self.file_menu.addAction('&Save System As...', self.save_file,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Export As...', self.export_as, QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.file_menu.addAction('&Quit', self.file_quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # show
        self.show_menu = QtGui.QMenu('&Show', self)
        self.menuBar().addMenu(self.show_menu)

        # terminal checkbox
        self.toggle_terminal_action = QtGui.QAction('Terminal', self.show_menu)
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
        self.build_settings_tab()

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

    # settings ----------------------------------------------------------
    def build_settings_tab(self):

        self.SetupApplyButton.clicked.connect(self.apply_config_changes)

        # read config-descriptions from dictionary
        self.descr = {}
        with open('core/config_description.py', 'r') as dict:
            data = dict.read()
            self.descr = ast.literal_eval(data)

        # qlistview
        sectionlist = self.descr["sectionlist"]
        # sectionlist = myConfig.config.sections()

        # create model for the section
        self.model = QtGui.QStandardItemModel(self.SectionListView)

        for section in sectionlist:
            item = QtGui.QStandardItem(section)
            # add item to the model
            self.model.appendRow(item)

        # apply model to listview
        self.SectionListView.setModel(self.model)

        # add action
        self.SectionListView.clicked.connect(self.settings_item_clicked)

        self.stack_visible = []

    def settings_item_clicked(self, index):
        self.remove_visible_items()

        # set section title
        self.section = str(index.data().toString())

        # what was sec_elab supposed to mean?
        section_description = self.descr[self.section]

        self.SetupSectionTitle.setText(section_description)

        # iterate over items in section
        items = myConfig.config.items(self.section)

        self.remove_visible_items()

        for i in items:
            # add qlabel and a qlineedit to gui
            label = QtGui.QLabel()
            label.setObjectName(i[0])
            label.setFixedWidth(300)

            # this does not seem to work, but why?:
            label.setAlignment(QtCore.Qt.AlignRight)
            #QtCore.pyqtRemoveInputHook()
            #embed()

            item_description = str(self.descr[i[0]][0])

            label.setText(str(item_description) + ":")
            label.setAlignment(QtCore.Qt.AlignRight)

            #lineedit = QtGui.QLineEdit()
            #lineedit.setObjectName(i[0])
            #lineedit.setFixedWidth(100)
            #lineedit.setAlignment(QtCore.Qt.AlignRight)
            value = myConfig.read(self.section, i[0])
            #lineedit.setText(value)
            
            if (value.lower() == "true") | (value.lower() == "false"):
                input_widget = self.create_boolean_combo_box(i[0], value)
            elif "color" in item_description.lower():
                input_widget = self.create_color_chooser(i[0], value)
            else:
                input_widget = self.create_line_edit(i[0], value)
                
            
            # add to stack_visible:
            # what was the 0 for?
            self.stack_visible.append([label, 0])
            #self.stack_visible.append([lineedit, self.section, str(i[0])])
            #self.add_to_layout(label, lineedit)
            self.stack_visible.append([input_widget, self.section, str(i[0])])
            self.add_to_layout(label, input_widget)

            # detect if entered new value
            # google "python lambda loop parameter" or see
            # http://stackoverflow.com/questions/938429/
            #                                       scope-of-python-lambda-functions-and-their-parameters/938493#938493
            # noinspection PyUnresolvedReferences
            #lineedit.textEdited.connect(self.callback_factory(lineedit, self.section, i[0]))
            #lineedit.textEdited.connect(self.callback_factory(lineedit, self.section, i[0]))
            #lineedit.textEdited.connect(lambda lineedit=lineedit: self.new_value(lineedit,self.section,i[0]))

            #print(self.stack_visible)

    def create_boolean_combo_box(self, name, value):
        """ 
        Creates a combo-box with the two entries "true" and "false" and
        connects its signal "currentIndexChanged" with the method "new_value"
        via the "callback_factory"
        
        Parameter:
        name  -- the name of the parameter represented by the value of the box
        value -- the current value of the parmeter
        """
        cbox = QtGui.QComboBox(self)
        cbox.setObjectName(name)
        cbox.setFixedWidth(100)
        cbox.addItem("true", "true")
        cbox.addItem("false", "false")
        if value.lower() == "true":
            cbox.setCurrentIndex(0)
        else:
            cbox.setCurrentIndex(1)
        cbox.currentIndexChanged.connect(self.callback_factory(cbox, self.section, name))            
        return cbox
        
    def create_line_edit(self, name, value):
        """ 
        Creates a lineedit box and connects its signal "textEdited" 
        with the method "new_value" via the "callback_factory"
        
        Parameter:
        name  -- the name of the parameter represented by the value of the box
        value -- the current value of the parmeter
        """
        lineedit = QtGui.QLineEdit(self)
        lineedit.setObjectName(name)
        lineedit.setFixedWidth(100)
        lineedit.setAlignment(QtCore.Qt.AlignRight)           
        lineedit.setText(value)
        lineedit.textEdited.connect(self.callback_factory(lineedit, self.section, name))
        return lineedit
        
    def create_color_chooser(self, name, value):
        """ 
        Creates a combo-box with some basic colors and connects its signal 
        "currentIndexChanged" with the method "new_value" via the 
        "callback_factory". The colors are presented in human readable names,
        but are represented by RGB-hex-strings in the background
        
        Parameter:
        name  -- the name of the parameter represented by the value of the box
        value -- the current value of the parmeter
        """
        ccbox = QtGui.QComboBox(self)
        ccbox.setObjectName(name)
        ccbox.setFixedWidth(100)
        ccbox.addItem("red", "#ff0000")
        ccbox.addItem("blue", "#0000ff")
        ccbox.addItem("green", "#008000")
        ccbox.addItem("orange", "#ff6600")
        ccbox.addItem("cyan", "#00ffff")
        ccbox.addItem("magenta", "#ff00ff")
        ccbox.addItem("purple", "#800080")
        ccbox.addItem("black", "#000000")
        ccbox.addItem("dark grey", "#666666")
        ccbox.addItem("light grey", "#b3b3b3")
        ccbox.addItem("white", "#ffffff")
        ccbox.addItem("custom...", "#d1193b")
        ind = ccbox.findData(QtCore.QVariant(value.lower()))
        if ind == -1:
            ccbox.setCurrentIndex(ccbox.count()-1)
        else:
            ccbox.setCurrentIndex(ind)
        ccbox.currentIndexChanged.connect(self.callback_factory(ccbox, self.section, name))
        return ccbox

    def callback_factory(self, input_widget, section, value):
        return lambda: self.new_value(input_widget, section, value)

    def add_to_layout(self, Label, LineEdit):
        count = self.SectionLayout.rowCount()

        self.SectionLayout.setWidget(count, QtGui.QFormLayout.LabelRole, Label)
        self.SectionLayout.setWidget(count, QtGui.QFormLayout.FieldRole, LineEdit)

    def remove_visible_items(self):
        if len(self.stack_visible) != 0:
            for i in xrange(0, len(self.stack_visible)):
                # get element from stack which is a list
                # with [QLineEdit,section,variable]
                element = self.stack_visible.pop()
                try:
                    if len(element) != 0:
                        item = element[0]
                        item.deleteLater()
                except Exception as error:
                    print("Could not remove element")

    def new_value(self, input_widget, section, variable):
        """ 
        Ensures that a changed parameter in the ui is written into the
        configuration data. 
        
        Parameter:
        input_widget -- the widget the value of which has been changed by the
                        user
        section      -- the configuration section the variable refers to
        variable     -- the name of the parameter
        """
        
        # read lineedit
        #QtCore.pyqtRemoveInputHook()
        #embed()
    
        if input_widget.metaObject().className() == "QLineEdit":
            new_value = str(input_widget.text())
        elif input_widget.metaObject().className() == "QComboBox":
            new_value = input_widget.itemData(input_widget.currentIndex()).toString()
        else:
            myLogger.debug_message("Unsupported widget type passed!")
            return
            
        # write config file
        myConfig.write(section, variable, new_value)
        myLogger.debug_message("New value for " + str(variable) + ":" + new_value)

    def apply_config_changes(self):
        myConfig.apply_changes()
        myLogger.debug_message("Config changes stored.")
        myLogger.initialize()

        # init
        # self.init()

        # VALIDATE EXPRESSIONS HERE!

    #         if len(self.stack_changed.keys())!=0:
    #             for i in xrange(0,len(self.stack_changed.keys())):
    #
    #                 item = str(self.stack_changed.keys()[i])
    #                 print(item)
    #                 value = str(self.stack_changed[item].text())
    #                 print(value)
    #                 if type(item)==QtGui.QLineEdit:
    #                     myConfig.write(self.section,item,value)
    #                     #print(str(item.text()))

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
        QtGui.QMessageBox.about(self, "About", (
                                "\n"
                                "    PyPlane 0.1.7\n"
                                "\n"
                                "    Copyright (C) 2013-2014\n"
                                "    by Klemens Fritzsche, Carsten Knoll\n"
                                "\n"
                                "    Dresden University of Technology\n"
                                "    Institute of Control Theory\n"
                                "\n"
                                "    This code is free software, licensed under the terms of the\n"
                                "    GNU General Public License, version 3\n"
                                "    <http://www.gnu.org/license/>.\n"
                                "\n")
        )

app = QtGui.QApplication(sys.argv)
main = MainApp()
main.show()
sys.exit(app.exec_())
