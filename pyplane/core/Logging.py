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

"""
Module implementing logging capabilities
"""

import time
import os
import sys
import appdirs
from PyQt5 import QtCore, QtWidgets, QtGui

__author__ = 'Klemens Fritzsche'

# Required by several other classes
# ToDo: Move this to sth. meaningful
basedir = os.path.dirname(os.path.dirname(sys.modules.get(__name__).__file__))

# Logfile goes here:
# Mac OS X: ~/Library/Logs/pyplane
# Unix    : ~/.cache/pyplane/log  # or under $XDG_CACHE_HOME if defined
# Windows : C:\Users\<username>\AppData\Local\pyplane\Logs
logfile_dir = appdirs.user_log_dir(appname="pyplane")
defaultLogFileName = os.path.join(logfile_dir, 'logmessages.txt')
if not os.path.exists(logfile_dir):
    os.makedirs(logfile_dir, exist_ok=True)

class Logger(object):
    """
    simple Logger, that prints messages to the screen
    and saves them to a file
    """

    def __init__(self, fname=None):
        if not isinstance(fname, str):
            fname = defaultLogFileName
        self.fname = fname
        self.create_file()

        self.msg_list = []

        self.err_flag = False
        self.signalemitter = QtCore.QObject()

        # TODO Read This from Config
        self.dbg_verbosity_level = 5
        # self.logtime = myConfig.get_boolean("Logging","log_showTime")

        self.t_zero = time.time()
        #         self.message(" ------ Logging started: %s -----" % time.ctime() )

        # hardcoded logging values for the time before existance of myConfig
        # instance
        self.show_error = True
        self.show_warning = True
        self.show_debug = True

        # The terminal on the GUI into which the messages are written. Will be set later.
        self.ppTerminal = None

    def initialize(self):
        """
        this function gets called after myConfig instance has been created.
        logging before that is possible with hardcoded values.
        """
        from .ConfigHandler import myConfig

        self.show_error = myConfig.get_boolean("Logging", "log_showError")
        self.show_warning = myConfig.get_boolean("Logging", "log_showWarning")
        self.show_debug = myConfig.get_boolean("Logging", "log_showDbg")

        myLogger.debug_message("Logging class initialized.")
        myLogger.message("Using logfile: {}".format(self.fname))

    def register_output(self, terminal):
        # output in logField
        assert isinstance(terminal, QtWidgets.QTextEdit)
        self.ppTerminal = terminal

    def sec_to_string(self, sec):
        """
        converts a given number (seconds) to a string
        hh:mm:ss
        """
        # use modulo %

        s = sec % 60

        mins = (sec - s) / 60
        m = mins % 60
        h = (mins - m) / 60

        string = "%02i:%02i:%04.1f" % (h, m, s)
        return string

    def message(self, msg, color='white'):

        assert (self.ppTerminal is not None)

        # set text color
        if color == 'white':
            self.ppTerminal.setTextColor(QtGui.QColor(255, 255, 255, 255))
        elif color == 'red':
            self.ppTerminal.setTextColor(QtGui.QColor(221, 30, 47, 255))
        elif color == 'gray':
            self.ppTerminal.setTextColor(QtGui.QColor(105, 105, 105, 255))
        else:
            # gray, too
            self.ppTerminal.setTextColor(QtGui.QColor(105, 105, 105, 255))

        t = time.time() - self.t_zero

        msg = "%s: %s" % (self.sec_to_string(t), msg)

        # Write message to terminal on GUI and ensure that the terminal is scrolled to the buttom
        # (i.e. the most recent entry is always shown)
        self.ppTerminal.append(msg)
        cursor = self.ppTerminal.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ppTerminal.setTextCursor(cursor)

        # Write message to internal list
        self.msg_list.append(msg)

        # Write message to log file
        self.append_to_file(msg)

    def error_message(self, msg):
        if self.show_error:
            self.err_flag = True
            self.message("(Error!  %s): %s" % (time.ctime().split()[3], msg), 'red')

    def warn_message(self, msg):
        if self.show_warning:
            assert isinstance(msg, str)
            self.message("(Warning!): %s" % msg, 'red')

    def debug_message(self, msg, level=5):
        if self.show_debug:
            self.message(msg, 'gray')

    def create_file(self):
        # erase all
        thefile = open(self.fname, 'w')
        thefile.close()

    def append_to_file(self, msg):
        # open in append mode
        with open(self.fname, 'a') as thefile:
            thefile.writelines(msg + '\n')

# prepare logservice for importing
myLogger = Logger()
