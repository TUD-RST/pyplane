# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:37:57 2015

Converts the ui-files in the directory gui into py-files using pyuic5

Run this directly from the command line with python path properly set

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

# --from-imports -> Ensure that we have "from . import incons_rc" in files using user defined icons
exec_command(["pyuic5", "../pyplane/gui/Ui_PyPlane.ui", "--from-imports", "-o", "../pyplane/gui/Ui_PyPlane.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_PyPlane_about.ui", "--from-imports", "-o", "../pyplane/gui/Ui_PyPlane_about.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_SettingsWidget.ui", "-o", "../pyplane/gui/Ui_SettingsWidget.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_SystemTabWidget.ui", "-o", "../pyplane/gui/Ui_SystemTabWidget.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_ThreeDWidget.ui", "-o", "../pyplane/gui/Ui_ThreeDWidget.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_ZoomWidgetSimple.ui", "-o", "../pyplane/gui/Ui_ZoomWidgetSimple.py"])
exec_command(["pyuic5", "../pyplane/gui/Ui_ZoomWidget.ui", "-o", "../pyplane/gui/Ui_ZoomWidget.py"])

# Has to be done manually since pyrcc5 is an exe, icoms_rc.py must go into the root directory!
# pyrcc resources/icons.qrc -o icons_rc.py
exec_command(["pyrcc5", "../pyplane/resources/icons.qrc", "-o", "../pyplane/gui/icons_rc.py"])