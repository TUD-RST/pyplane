# -*- coding: utf-8 -*-

##############################################################################
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
##############################################################################

import configparser
import os
import ast

from core.Logging import myLogger


class ConfigHandler(object):
    """ this class handles the read and write methods for config
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str

        __dir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.abspath(os.path.join(__dir__, 'config/default'))

        try:
            data = self.config.read(filepath)
        except Exception as exc:
            myLogger.warn_message("input error!")
            myLogger.debug_message(str(exc))
            print("Input error")

        # fallback values
        # read config-descriptions from dictionary
        self.descr = {}

        with open('core/config_description.py', 'r') as dict:
            data = dict.read()
            self.descr = ast.literal_eval(data)


    def cancle_and_reload(self):
        self.__init__()


    def write(self, section, variable, new_value):
        """ this function saves a variable to config
        """
        self.config.set(str(section), str(variable), str(new_value))

    def read(self, section, variable):
        if self.config.has_option(str(section), str(variable)):
            value = self.config.get(str(section), str(variable))
            # TODO: check if the config value is of same type as fallback value
            myLogger.debug_message(str(variable) + "\": " + str(value) + " (config)")
            return value
        elif str(variable) in self.descr:
            # fallback value
            value = self.descr[str(variable)][1]
            myLogger.debug_message(str(variable) + "\": " + str(value) + " (fallback)")
            return value
        else:
            #pass
            myLogger.error_message("Error! A variable was called that does not exist.")

    def get_boolean(self, section, variable):
        if self.config.has_option(str(section), str(variable)):
            value = self.config.getboolean(str(section), str(variable))
            myLogger.debug_message(str(variable) + "\": " + str(value) + " (config)")
            return value
        elif str(variable) in self.descr:
        #self.descr.has_key(str(variable)):
            # fallback value
            value = self.descr[str(variable)][1]
            myLogger.debug_message(str(variable) + "\": " + str(value) + " (fallback)")
            return value
        else:
            #pass
            myLogger.error_message("Error! A variable was called that does not exist.")


    def apply_changes(self):
        # stores temporary config
        with open('config/default', 'w') as configfile:
            self.config.write(configfile)


# prepare configData for importing
myConfig = ConfigHandler()

