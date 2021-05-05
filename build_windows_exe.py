# -*- coding: utf-8 -*-
"""
Builds a Windows executable of PyPlane using PyInstaller

Created on Fri Mar 27 16:16:28 2015

@author: winkler
"""
import os
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# The name of the exe to be built
exename = 'PyPlane'

# Specifacations for PyInstaller
spec_file = exename + '.spec'

# Main directory of the app's source code
app_dir = 'pyplane'

# Additional files in the app directory
descrfile = 'core\\config_description.py'

# Sub-directories in the app directory
# (we need them without app_dir name prefix later!)
config_dir = 'config'
lib_dir = 'library'
core_dir = 'core'

# Directories where to build the app
temp_dir = os.path.join('windows', 'temp')
build_dir = os.path.join('windows', 'build')
exe_dir = os.path.join(build_dir, exename)

# We work with absolute paths in the following because of problems in PyInstaller
# From here all paths have to be absolute
a_script_dir = os.getcwd()
a_build_dir = os.path.join(a_script_dir, build_dir)
a_temp_dir = os.path.join(a_script_dir, temp_dir)
a_exe_dir = os.path.join(a_script_dir, exe_dir)
a_app_dir = os.path.join(a_script_dir, app_dir)
a_config_dir = os.path.join(a_app_dir, config_dir)
a_core_dir = os.path.join(a_app_dir, core_dir)
a_lib_dir = os.path.join(a_app_dir, lib_dir)
a_descr_file = os.path.join(a_app_dir, descrfile)
a_spec_file = os.path.join(a_script_dir, spec_file)


# Build the command string
cmd = ['--clean',
       '--distpath=%s' % a_build_dir,
       '--workpath=%s' % a_temp_dir,
       a_spec_file]

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
