About 
===== 
PyPlane is a free software for phase plane analysis of second order
dynamical systems written in PYTHON and QT4. While having less
features, it aims to be a (partial) replacement for MATLAB's pplane.

![Screenshot](/resources/pyplane_screenshot.png?raw=true)

It has been originally developed by Klemens Fritzsche in 2013 and 2014 
at the Institute of Control Theory [1], Technische Universität Dresden. 
Supervisors: Carsten Knoll, Jan Winkler.

Since 2015 it is maintained and developed by Klemens Fritzsche and 
Jan Winkler at the Institute of Control Theory [1].

It is published under the GNU GENERAL PUBLIC LICENSE Version 3.

The most recent version of PyPlane can always be found at GitHub:

https://github.com/TUD-RST/pyplane

Please don't hesitate to report bugs, comments, or suggestions on
GitHub!

[1] http://www.et.tu-dresden.de/rst/




Notes
=====

PyPlane runs either natively in a fully functional Python environment
under Linux/ Windows/ MAC or as a stand-alone executable under MS
Windows.

Prerequisites for running natively under Python
----------------------------------------------- 

PyPlane runs under Python version 2.7 with the following packages
installed:

* NumPy (tested under version 1.9)
* SciPy (tested under version 0.15)
* Matplotlib (tested under verison 1.4.3)
* SymPy (tested under verison 0.7.6)
* PyQt4 (tested under version 4.11.3)

An optionally installed and accessible LaTeX/ dvipng environment
produces much prettier results in the linearization tabs. If no LaTeX
is installed the program is still fully functional.

Call "python main.py" in the base directory of PyPlane in order to
launch the application.


Prerequisites for the stand-alone version
-----------------------------------------

The stand-alone version is only available for MS Windows operating
systems on which no Python is installed. You just need to run the
provided installer file PyPlane_Setup.exe. It will create a directory
on your desktop in which all required files will be stored. A shortcut
for launching PyPlane will be placed on the desktop. No modifications
in the system registry will be done. As in the native Python version a
functional LaTeX installation will produce better formatting results
in the linearization tabs. But even without LaTeX the program is fully
functional.

Double-click on the PyPlane icon on the desktop in order to launch the
application. Start-up may take some time.

Open issues in version 1.0
==========================

* PyPlane will not launch if it detects a fully functional
  LaTeX-environment in which the package type1cm.sty is
  missing. Please place this style package in your LaTeX-installation.

* When having detected an equilibrium point the linearization tab is
  only shown if you double-click again on the detected equilibrium
  point.



Important files in the base directory
=====================================

main.py
-------
Run main.py in order to launch the application

make_ui.py
----------
Run this script in order to convert ui-files created by QT Designer to
py-files and to generate the resource file icons_rc.py

build_exe.py
------------
Run this Python script on windows machines in order to build a
stand-alone executable for MS Windows (which does not require a
separate Python installation)

InstallerPyPlane.nsi
--------------------
Run this script from Nullsoft installer to build an installation
package for the stand-alone executable created by buid_exe.py
