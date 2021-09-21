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


import ast
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from .Ui_SettingsWidget import Ui_SettingsWidget
from .Ui_SystemTabWidget import Ui_SystemTabWidget
from .Ui_ZoomWidget import Ui_ZoomWidget
from .Ui_ZoomWidgetSimple import Ui_ZoomWidgetSimple
from .Ui_ThreeDWidget import Ui_ThreeDWidget
from ..core.Canvas import Canvas, ThreeDCanvas
from ..core.ConfigHandler import myConfig
from ..core.Graph import Plot, ThreeDPlot, PhasePlot
from ..core.NullclineHandler import NullclineHandler
from ..core.Vectorfield import Vectorfield
from ..core.StreamlineHandler import StreamlineHandler
from ..core.EquilibriumHandler import EquilibriumHandler
from ..core.Logging import myLogger, basedir


__author__ = 'Klemens Fritzsche'
__version__ = "1.0"


# TODO: It may be better to move these classes to separate files.
class SettingsWidget(QtWidgets.QWidget, Ui_SettingsWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.SetupApplyButton.clicked.connect(self.apply_config_changes)

        # read config-descriptions from dictionary
        self.descr = {}
        with open(os.path.join(basedir, 'core', 'config_description.py'), 'r') as descr:
            data = descr.read()
            self.descr = ast.literal_eval(data)

        # qlistview
        sectionlist = self.descr["sectionlist"]
        # sectionlist = myConfig.config.sections()

        # create model for the section
        self.model = QtGui.QStandardItemModel(self.SectionListView)

        for section in sectionlist:
            item = QtGui.QStandardItem(section[0])
            # add item to the model
            self.model.appendRow(item)

        # apply model to listview
        self.SectionListView.setModel(self.model)

        # add action
        self.SectionListView.clicked.connect(self.settings_item_clicked)

        self.stack_visible = []

        self.section = None

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

    def settings_item_clicked(self, index):
        # TODO: May be we should change this mechanism to a clear model-view
        #       process. Maybe a tree view is appropriate?
        self.remove_visible_items()

        # set section title
        self.section = str(index.data())

        # what was sec_elab supposed to mean?
        section_description = self.descr[self.section]

        self.SetupSectionTitle.setText(section_description)

        # iterate over items in section
        items = myConfig.config.items(self.section)

        self.remove_visible_items()

        for i in items:
            # add qlabel and a qlineedit to gui
            label = QtWidgets.QLabel()
            label.setObjectName(i[0])
            label.setFixedWidth(300)

            # this does not seem to work, but why?:
            label.setAlignment(QtCore.Qt.AlignRight)
            # QtCore.pyqtRemoveInputHook()
            # embed()

            try:
                item_description = str(self.descr[i[0]][0])
            except KeyError:
                myLogger.debug_message("Key %s not found in description list (key deprecated or invalid), ignoring...!"
                                       % (i[0]))

            label.setText(str(item_description) + ":")
            label.setAlignment(QtCore.Qt.AlignRight)

            value = myConfig.read(self.section, i[0])

            if (value.lower() == "true") | (value.lower() == "false"):
                input_widget = self.create_boolean_combo_box(i[0], value)
            elif "color" in item_description.lower():
                input_widget = self.create_color_chooser(i[0], value)
            else:
                input_widget = self.create_line_edit(i[0], value)

            # add to stack_visible:
            # what was the 0 for?
            self.stack_visible.append([label, 0])
            # self.stack_visible.append([lineedit, self.section, str(i[0])])
            # self.add_to_layout(label, lineedit)
            self.stack_visible.append([input_widget, self.section, str(i[0])])
            self.add_to_layout(label, input_widget)

            # detect if entered new value
            # google "python lambda loop parameter" or see
            # http://stackoverflow.com/questions/938429/
            #                                       scope-of-python-lambda-functions-and-their-parameters/938493#938493
            # noinspection PyUnresolvedReferences
            # lineedit.textEdited.connect(self.callback_factory(lineedit, self.section, i[0]))
            # lineedit.textEdited.connect(self.callback_factory(lineedit, self.section, i[0]))
            # lineedit.textEdited.connect(lambda lineedit=lineedit: self.new_value(lineedit,self.section,i[0]))

            # print(self.stack_visible)

    def create_boolean_combo_box(self, name, value):
        """
        Creates a combo-box with the two entries "true" and "false" and
        connects its signal "currentIndexChanged" with the method "new_value"
        via the "callback_factory"

        Parameter:
        name  -- the name of the parameter represented by the value of the box
        value -- the current value of the parmeter
        """
        cbox = QtWidgets.QComboBox(self)
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
        lineedit = QtWidgets.QLineEdit(self)
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
        # TODO (jcw): Implement color picker for custom color
        ccbox = QtWidgets.QComboBox(self)
        ccbox.setObjectName(name)
        ccbox.setFixedWidth(100)
        ccbox.addItem("red", "#ff0000")
        ccbox.addItem("blue", "#0000ff")
        ccbox.addItem("green", "#008000")
        ccbox.addItem("orange", "#ff6600")
        ccbox.addItem("cyan", "#00ffff")
        ccbox.addItem("magenta", "#ff00ff")
        ccbox.addItem("purple", "#800080")
        ccbox.addItem("lime", "#00ff00")
        ccbox.addItem("black", "#000000")
        ccbox.addItem("dark grey", "#666666")
        ccbox.addItem("light grey", "#b3b3b3")
        ccbox.addItem("white", "#ffffff")
        ccbox.addItem("custom...", "#d1193b")
        ind = ccbox.findData(value.lower())
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

        self.SectionLayout.setWidget(count, QtWidgets.QFormLayout.LabelRole, Label)
        self.SectionLayout.setWidget(count, QtWidgets.QFormLayout.FieldRole, LineEdit)

    def remove_visible_items(self):
        if len(self.stack_visible) != 0:
            for i in range(0, len(self.stack_visible)):
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
            new_value = str(input_widget.itemData(input_widget.currentIndex()))
        else:
            myLogger.debug_message("Unsupported widget type passed!")
            return

        # write config file
        myConfig.write(section, variable, new_value)
        myLogger.debug_message("New value for " + str(variable) + ":" + new_value)


class SystemTabWidget(QtWidgets.QWidget, Ui_SystemTabWidget):
    def __init__(self, parent):
        self.mySystem = parent
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        # Embed widgets: not working, but why?!
        # self.ppWidget = ZoomWidget()
        # self.ppLayout.addWidget(self.ppWidget)

        self.mySystem.myPyplane.tabWidget.currentChanged.connect(self.on_change)

    def on_change(self):
        if self.mySystem.myPyplane.tabWidget.currentIndex()==len(self.mySystem.myPyplane.tabWidget)-1:
            self.mySystem.myPyplane.disable_menu_items()
        else:
            self.mySystem.myPyplane.update_ui()


class ZoomWidgetSimple(QtWidgets.QWidget, Ui_ZoomWidgetSimple):
    # TODO: Is this class really necessary? -> inheritance from ZoomWidget?
    def __init__(self, parent, parameter):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.mySystem = parent
        self.param = parameter # "x" or "y"
        self.ylabel_str = self.param
        self.xlabel_str = "t"

        # TODO: This should probably move to the Plot-class:
        self.latex_installed = self.mySystem.myPyplane.latex_installed
        self.Layout = QtWidgets.QVBoxLayout(self.frame)

        self.Canvas = Canvas(self, self.latex_installed)
        self.Layout.addWidget(self.Canvas)

        self.param_minLabel.setText("%smin" % (self.param))
        self.param_maxLabel.setText("%smax" % (self.param))
        self.xminLineEdit.setText(str(myConfig.read("%s-t-plot" % (self.param), "%s_tmin" % (self.param))))
        self.xmaxLineEdit.setText(str(myConfig.read("%s-t-plot" % (self.param), "%s_tmax" % (self.param))))
        self.yminLineEdit.setText(str(myConfig.read("%s-t-plot" % (self.param), "%s_%smin" % (self.param, self.param))))
        self.ymaxLineEdit.setText(str(myConfig.read("%s-t-plot" % (self.param), "%s_%smax" % (self.param, self.param))))

        self.Plot = Plot(self, self.Canvas)

        # connect buttons
        self.SetButton.clicked.connect(self.Plot.set_window_range)
        self.ZoomButton.clicked.connect(self.Canvas.toggle_zoom_mode)
        self.ZoomButton.setCheckable(True)


class ThreeDWidget(QtWidgets.QWidget, Ui_ThreeDWidget):
    # TODO: Is this class really necessary? -> inheritance from ZoomWidget?
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.mySystem = parent

        # Axis labels
        self.xlabel_str = "x"
        self.ylabel_str = "y"
        self.zlabel_str = "t"

        # TODO: This should probably move to the Plot-class:
        self.latex_installed = self.mySystem.myPyplane.latex_installed
        self.Layout = QtWidgets.QVBoxLayout(self.frame)

        self.Canvas = ThreeDCanvas(self, self.latex_installed)
        self.Layout.addWidget(self.Canvas)

        self.tminLineEdit.setText(str(myConfig.read("3d-plot", "3d_tmin")))
        self.tmaxLineEdit.setText(str(myConfig.read("3d-plot", "3d_tmax")))
        self.xminLineEdit.setText(str(myConfig.read("3d-plot", "3d_xmin")))
        self.xmaxLineEdit.setText(str(myConfig.read("3d-plot", "3d_xmax")))
        self.yminLineEdit.setText(str(myConfig.read("3d-plot", "3d_ymin")))
        self.ymaxLineEdit.setText(str(myConfig.read("3d-plot", "3d_ymax")))

        self.Plot = ThreeDPlot(self, self.Canvas)

        # connect buttons
        self.SetButton.clicked.connect(self.Plot.set_window_range)


class PhaseplaneWidget(QtWidgets.QWidget, Ui_ZoomWidget):
    def __init__(self, parent):
        self.mySystem = parent
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.latex_installed = self.mySystem.myPyplane.latex_installed
        self.Layout = QtWidgets.QVBoxLayout(self.frame)
        self.Canvas = Canvas(self, self.latex_installed)
        self.Layout.addWidget(self.Canvas)

        # Axis labels
        self.xlabel_str = "x"
        self.ylabel_str = "y"

        # set forward and backward integration true
        if myConfig.get_boolean("Trajectories", "traj_checkForwardByDefault"):
            self.forwardCheckbox.setChecked(True)
        if myConfig.get_boolean("Trajectories", "traj_checkBackwardByDefault"):
            self.backwardCheckbox.setChecked(True)

        self.xminLineEdit.setText(str(myConfig.read("Phaseplane", "pp_xmin")))
        self.xmaxLineEdit.setText(str(myConfig.read("Phaseplane", "pp_xmax")))
        self.yminLineEdit.setText(str(myConfig.read("Phaseplane", "pp_ymin")))
        self.ymaxLineEdit.setText(str(myConfig.read("Phaseplane", "pp_ymax")))

        self.Plot = PhasePlot(self, self.Canvas)
        self.Plot.set_window_range()

        self.VF = Vectorfield(self)
        self.SL = StreamlineHandler(self)
        self.Nullclines = NullclineHandler(self)
        self.Equilibria = EquilibriumHandler(self)

        # menu checkers
        self.mySystem.myPyplane.toggle_vectorfield_action.setChecked(self.VF.tgl)

        # connect buttons
        self.SetButton.clicked.connect(self.Plot.set_window_range)
        self.ZoomButton.clicked.connect(self.Canvas.toggle_zoom_mode)
        self.ZoomButton.setCheckable(True)
        self.RefreshButton.clicked.connect(self.Plot.refresh)
        self.CreateTrajectoryButton.clicked.connect(self.mySystem.Trajectories.create_trajectory)
        # linearize button and combo box
        # TODO: Fix next line!
        # self.connect(self.linBox, QtCore.SIGNAL('activated(QString)'), self.eq_chosen)
        self.linButton.clicked.connect(self.linearize_system)

        self.hide_linearization_objects()

    def hide_linearization_objects(self):
        self.linLabel.hide()
        self.linBox.hide()
        self.linButton.hide()

    def show_linearization_objects(self):
        self.linLabel.show()
        self.linButton.show()
        # clear combo box
        self.linBox.clear()
        # put equilibria in combo box
        eq_list = self.Equilibria.list_characterized_equilibria()
        self.linBox.addItems(eq_list)
        self.linBox.show()

    def eq_chosen(self, text):
        # TODO: highlight selected point
        pass

    def linearize_system(self):
        eq_identifier = str(self.linBox.currentText())
        equilibrium = self.Equilibria.get_equilibrium_by_character_identifier(eq_identifier)
        jac = self.Equilibria.approx_ep_jacobian(equilibrium.coordinates)

        # set system properties
        accuracy = int(myConfig.read("Linearization","lin_round_decimals"))
        xe = round(equilibrium.coordinates[0], accuracy)
        ye = round(equilibrium.coordinates[1], accuracy)
        equilibrium = (xe, ye)
        A00 = str(round(jac[0,0], accuracy))
        A01 = str(round(jac[0,1], accuracy))
        A11 = str(round(jac[1,1], accuracy))
        A10 = str(round(jac[1,0], accuracy))
        x_dot_string = A00 + "*(x-(" + str(xe) + ")) + (" + A01 + ")*(y-(" + str(ye) + "))"
        y_dot_string = A10 + "*(x-(" + str(xe) + ")) + (" + A11 + ")*(y-(" + str(ye) + "))"
        equation_string = (x_dot_string, y_dot_string)

        self.mySystem.myPyplane.new_linearized_system(equation_string, eq_identifier, equilibrium)

    def trajectory_direction(self):
        forward = self.forwardCheckbox.isChecked()
        backward = self.backwardCheckbox.isChecked()
        return [forward, backward]

    def read_init(self):
        """ read initial condition from line edits """
        x_init = float(self.xinitLineEdit.text())
        y_init = float(self.yinitLineEdit.text())
        return [x_init, y_init]
