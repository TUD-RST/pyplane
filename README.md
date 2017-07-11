About 
===== 
PyPlane is a free software for phase plane analysis of second order
dynamical systems written in PYTHON 3.5 and PyQT5 (compare MATLAB's
[pplane](http://math.rice.edu/~dfield/)).

![Screenshot](/resources/pyplane_screenshot.png?raw=true)

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

PyPlane runs under Python version 3.5 with the following packages
installed:

* NumPy (tested under version 1.13)
* SciPy (tested under version 0.19.1)
* Matplotlib (tested under verison 1.5.3 and 2.0.2)
* SymPy (tested under verison 1.0)
* PyQt5 (tested under version 5.8.2)

An optionally installed and accessible LaTeX/dvipng environment
produces much prettier results in the linearization tabs. If no LaTeX
is installed the program is still fully functional.

Call "python main.py" in the base directory of PyPlane in order to
launch the application.

Python 2
--------
The last version of this program which is fully compatible with 
Python 2.7 is version 1.1.


Prerequisites for the stand-alone version
-----------------------------------------

(Currently a installer for PyPlane 1.1 is available only, but you
can build one for 2.0beta from source.)

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

Open issues in version 2.0beta
==============================

* When LaTeX is not installed on your system the plot dimensions might
  be such that the labels are not fully displayed.



Important files in the base directory
=====================================

###### main.py
Run `python main.py` in order to launch the application

###### make_ui.py
Run this script in order to convert ui-files created by QT4 Designer to
py-files and to generate the resource file icons_rc.py

###### build_exe.py
Run this Python script on windows machines in order to build a
stand-alone executable for MS Windows (which does not require a
separate Python installation)

###### InstallerPyPlane.nsi
Run this script from Nullsoft installer to build an installation
package for the stand-alone executable created by buid_exe.py
