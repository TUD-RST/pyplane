About
=====
PyPlane is a free software for phase plane analysis of second order 
dynamical systems written in PYTHON and QT4. While having less features, 
it  aims to be a (partial) replacement for MATLAB's pplane.

![Screenshot](/resources/pyplane_screenshot.png?raw=true)

It has been originally developed by Klemens Fritzsche in 2013 and 2014 
at the Institute of Control Theory [1], Technische Universität Dresden. 
Supervisors: Carsten Knoll, Jan Winkler.

Since 2015 it is maintained and developed by Klemens Fritzsche and 
Jan Winkler at the Institute of Control Theory [1].

It is published under the GNU GENERAL PUBLIC LICENSE Version 3.

[1] http://www.et.tu-dresden.de/rst/


Notes
=====

main.py
-------
Run main.py in order to launch the application

make_ui.py
----------
Run this script in order to convert ui-files created by QT Designer to 
py-files and to generate the resource file icons_rc.py

build_exe.py
------------
Run this Python script on windows machines in order to build a stand-alone
executable for MS Windows (which does not require a separate 
Python installation)

InstallerPyPlane.nsi
--------------------
Run this script from Nullsoft installer to build an installation package for 
the stand-alone executable created by buid_exe.py
