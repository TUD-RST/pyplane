# -*- coding: utf-8 -*-
"""
Builds a Windows executable of PyPlane 

Make sure that pyinstaller is properly installed in your Python distribution!

Please note in order to build a properly working exe:
-> Set recursion limit in build_main.py of your PyInstaller installation
   (see howto_build_windows_exe.txt for more information)
-> Modify the function exec_command(...) in file lib\site-packages\PyInstaller\compat.py according to the
   instructions in howto_build_windows_exe.txt
-> Modify the file lib\site-packages\PyInstaller\hook-botocore.py according to the
   instructions in howto_build_windows_exe.txt
-> Set qt_bin_path and libzmq_path in this script appropriately
-> Run this script from an IDE, e.g. PyCharm, in order to avoid UTF-8 errors in pyinstaller

Created on Fri Mar 27 16:16:28 2015

@author: winkler
"""
import os
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# Some global stuff (adjust the qt_bin and libzmq paths!)
qt_bin_path = 'c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\PyQt5\\Qt\\bin'
libzmq_path = 'c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\zmq'

# The name of the exe to be built
exename = 'PyPlane'

# Main directory of the app's source code
app_dir = 'pyplane'

# The master file of the program
infile = 'main.py'

# Additional files in the app directory
descrfile ='core\\config_description.py'
iconfile = 'resources\\pyplane_icon_32px.ico'

# Sub-directories in the app directory
# (we need them without app_dir name prefix later!)
config_dir = 'config'
lib_dir = 'library'
core_dir = 'core'

# Directories where to build the app
temp_dir = os.path.join('windows', 'temp')
build_dir = os.path.join('windows', 'build')
exe_dir = os.path.join(build_dir, exename)


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

# We work with absolute paths in the following because of problems in PyInstaller
# From here all paths have to be absolute
a_script_dir = os.getcwd()

a_build_dir = os.path.join(a_script_dir, build_dir)
a_temp_dir = os.path.join(a_script_dir, temp_dir)
a_exe_dir = os.path.join(a_script_dir, exe_dir)
a_app_dir = os.path.join(a_script_dir, app_dir)
a_config_dir = os.path.join(a_app_dir, config_dir)
a_core_dir = os.path.join(a_app_dir, core_dir)
a_icon_file = os.path.join(a_app_dir, iconfile)
a_descr_file = os.path.join(a_app_dir, descrfile)
a_input_file = os.path.join(a_app_dir, infile)
a_lib_dir = os.path.join(a_app_dir, lib_dir)


# Build the command string
cmd = ['--clean',
       '--distpath=%s' % a_build_dir,
       '--workpath=%s' % a_temp_dir,
       '--paths=%s' % a_app_dir,
       '--paths=%s' % a_core_dir,
       '--paths=%s' % qt_bin_path,
       '--paths=%s' % libzmq_path,
       '--hidden-import=scipy.special._ufuncs_cxx',
       '--hidden-import=mpl_toolkits',
       '--hidden-import=scipy.linalg.cython_blas',
       '--hidden-import=scipy.linalg.cython_lapack',
       '--hidden-import=scipy._lib.messagestream',
       '--hidden-import=tkinter.filedialog',
       '--icon=%s' % a_icon_file,
       '--name=%s' % (exename),
       a_input_file]

print(cmd)

# Clean-up environment
if os.path.exists(a_build_dir):
    shutil.rmtree(a_build_dir, ignore_errors=True)

# Call pyinstaller
print('Executing command pyinstaller %s' % cmd)
pyinstaller_run(cmd)

# Copy the config directory to the build directory
shutil.copytree(a_config_dir, os.path.join(a_exe_dir, config_dir))
shutil.copytree(a_lib_dir, os.path.join(exe_dir, lib_dir))
os.mkdir(os.path.dirname(os.path.join(a_exe_dir, descrfile)))
print(os.path.dirname(os.path.join(a_exe_dir, descrfile)))
print(a_descr_file)
shutil.copyfile(a_descr_file, os.path.join(a_exe_dir, descrfile))
