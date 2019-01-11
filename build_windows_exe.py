# -*- coding: utf-8 -*-
"""
Builds a Windows executable of PyPlane 

Make sure that pyinstaller is properly installed in your Python distribution!

Please note in order to build a properly working exe:
-> Set recursion limit in build_main.py of your PyInstaller installation
   (see HowTo-Windows-Exe.txt for more information)
-> Modify the function exec_command(...) in file lib\site-packages\PyInstaller\compat.py according to the
   instructions in How-To-Windows-Exe.txt
-> Modify the file lib\site-packages\PyInstaller\hook-botocore.py according to the
   instructions in How-To-Windows-Exe.txt
-> Set qt_bin_path and libzmq_path in this script appropriately

Created on Fri Mar 27 16:16:28 2015

@author: winkler
"""
import os
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# The name of the exe to be built
exename = 'PyPlane'

# Main directory of the app's source code
app_dir = 'pyplane\\'

# The master file of the program
infile = app_dir + 'main.py'

# Additional files in the app directory
descrfile = app_dir + 'core\\config_description.py'
iconfile = app_dir + 'resources\\pyplane_icon_32px.ico'

# Directories (adjust the qt_bin and libzmq paths!)
config_dir = app_dir + 'config'
lib_dir = app_dir + 'library'
temp_dir = 'windows\\temp'
build_dir = 'windows\\build'
exe_dir = build_dir + '\\' + exename + '\\'
qt_bin_path = 'c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\PyQt5\\Qt\\bin'
libzmq_path = 'c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\zmq'
additional_paths = app_dir + 'core'

# Check if dirs exist
if not os.path.exists(qt_bin_path):
    print("The QT directory %s does not exist!\n\n \
          Please set the directory appropriately (see HowTo-Windows-Exe.txt for more information!)" 
           % qt_bin_path)
    exit(-1)
    
if not os.path.exists(libzmq_path):
    print("The LIB ZMG directory %s does not exist!\n\n\
           Please set the directory appropriately (see HowTo-Windows-Exe.txt for more information!)" 
           % libzmq_path)
    exit(-1)

# The path of this script, we work with absolute paths in the following because of problems in PyInstaller
base_path = os.getcwd()

# Build the command string
cmd = ['--clean',
       '--distpath=%s' % os.path.join(base_path, build_dir),
       '--workpath=%s' % os.path.join(base_path, temp_dir),
       '--paths=%s' % os.path.join(qt_bin_path),
       '--paths=%s' % os.path.join(libzmq_path),
       '--paths=%s' % os.path.join(base_path, additional_paths),
       '--hidden-import=scipy.special._ufuncs_cxx',
       '--hidden-import=mpl_toolkits',
       '--hidden-import=scipy.linalg.cython_blas',
       '--hidden-import=scipy.linalg.cython_lapack',
       '--hidden-import=scipy._lib.messagestream',
       '--hidden-import=tkinter.filedialog',
       '--icon=%s' % os.path.join(base_path, iconfile),
       '--name=%s' % (exename),
       os.path.join(base_path, infile)]

# Clean-up environment
if os.path.exists(build_dir):
    shutil.rmtree(build_dir, ignore_errors=True)

# Call pyinstaller
print('Executing command pyinstaller %s' % cmd)
pyinstaller_run(cmd)

# Copy the config directory to the build directory
shutil.copytree(config_dir, exe_dir + config_dir)
shutil.copytree(lib_dir, exe_dir + lib_dir)
os.mkdir(os.path.dirname(exe_dir + descrfile))
shutil.copyfile(descrfile, exe_dir + descrfile)
