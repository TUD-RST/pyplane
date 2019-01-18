About 
===== 
PyPlane is a free software for phase plane analysis of second order
dynamical systems written in PYTHON 3.6 and PyQT5 (compare MATLAB's
[pplane](http://math.rice.edu/~dfield/)).

![Screenshot](pyplane/resources/pyplane_screenshot.png?raw=true)

Features:
* Vector fields and streamlines for second order nonlinear
dynamical systems of the form x'=f(x,y), y'=g(x,y)
* Forward and backward solution trajectories for arbitrary
initial conditions in the phase plane
* Time dependent solutions x(t) and y(t)
* 3D visualization t(x,y)
* Nullclines
* Find equilibrium points and calculate the corresponding Jacobian
* Linearize a system around equilibrium points, characterize and
plot eigenvectors
* Add arbitrary function into the phase plane area (i.e. contour lines of
Ljapunov-functions)


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

[1] https://tu-dresden.de/ing/elektrotechnik/rst




Notes
=====

PyPlane runs either natively in a fully functional Python environment
under Linux/Windows/OSX or as a stand-alone executable under MS
Windows.

Prerequisites for running natively under Python
----------------------------------------------- 

PyPlane runs under Python version 3.5.x and 3.6.x with the following 
packages installed:

* NumPy (tested under version 1.13.3)
* SciPy (tested under version 1.0.0)
* Matplotlib (tested under version 1.5.3 and 2.1.0)
* SymPy (tested under version 1.1.1)
* PyQt5 (tested under version 5.9.1)

An optionally installed and accessible LaTeX/dvipng environment
produces much prettier results in the linearization tabs. If no LaTeX
is installed the program is still fully functional.

Call "python main.py" in the base directory of PyPlane in order to
launch the application.

Python 2
--------
The last version of this program which is fully compatible with 
Python 2.7 is [version 1.1](https://github.com/TUD-RST/pyplane/releases/tag/PyPlane_v1.1.0).


Prerequisites for the stand-alone version
-----------------------------------------

The [stand-alone version](https://github.com/TUD-RST/pyplane/releases)
is only available for MS Windows operating
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


Example systems
---------------
In the directory "library" you find several example systems which you can 
load via "Open - From File" or by pressing STRG+O


Important files in the base directory
=====================================

###### main.py
Run `python main.py` in order to launch the application

###### make_ui.py
Run this script in order to convert ui-files created by QT4 Designer to
py-files and to generate the resource file icons_rc.py

###### build_exe.py
Run this Python script on Windows machines in order to build a
stand-alone executable for MS Windows (which does not require a
separate Python installation). See the file How-To-Windows-Exe.txt for
information how to setup the pyinstaller environment.

###### InstallerPyPlane.nsi
Run this script from Nullsoft installer to build an installation
package for the stand-alone executable created by buid_exe.py
