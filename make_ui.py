# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:37:57 2015

Converts the ui-files in the directory gui into py-files using pyuic4

@author: winkler

Uses code in exec_command from Pit Garbe
"""

import platform
import subprocess

MAC      = "Mac OS"
WINDOWS  = "Windows"
PLATFORM = platform.system()


def exec_command(cmd, ok_return_value=0):
    """
    Run given command, check return value
    :param cmd: Command to execute
    :param ok_return_value: The expected return value after successful completion
    """

    try:
        # hides the command window for cli tools that are run (in Windows)
        info = None
        if PLATFORM == WINDOWS:
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = subprocess.SW_HIDE
            cmd[0] = cmd[0] + '.bat'

        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             startupinfo=info)
        out, err = p.communicate()
    except OSError:
        raise

    if ok_return_value is not None and p.returncode != ok_return_value:
        raise RuntimeError("Command Failed: {c} ({e})".format(c=cmd,
                                                              e=str(err)))
    else:
        print(("Successfully executed command {c}".format(c=cmd)))


# ToDo: 
# Read in all ui-files automatically and convert them

exec_command(["pyuic5", "gui/Ui_PyPlane.ui", "-o", "gui/Ui_PyPlane.py"])
exec_command(["pyuic5", "gui/Ui_PyPlane_about.ui", "-o", "gui/Ui_PyPlane_about.py"])
exec_command(["pyuic5", "gui/Ui_SettingsWidget.ui", "-o", "gui/Ui_SettingsWidget.py"])
exec_command(["pyuic5", "gui/Ui_SystemTabWidget.ui", "-o", "gui/Ui_SystemTabWidget.py"])
exec_command(["pyuic5", "gui/Ui_ThreeDWidget.ui", "-o", "gui/Ui_ThreeDWidget.py"])
exec_command(["pyuic5", "gui/Ui_ZoomWidgetSimple.ui", "-o", "gui/Ui_ZoomWidgetSimple.py"])
exec_command(["pyuic5", "gui/Ui_ZoomWidget.ui", "-o", "gui/Ui_ZoomWidget.py"])

# Has to be done manually since pyrcc5 is an exe
# pyrcc resources/icons.qrc -o gui/icons_rc.py
#exec_command(["pyrcc5", "resources/icons.qrc", "-o", "gui/icons_rc.py"])