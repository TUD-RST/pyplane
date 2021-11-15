# -*- coding: utf-8 -*-
"""
Builds a Windows executable of PyPlane using PyInstaller

Created on Fri Mar 27 16:16:28 2015

@author: winkler
"""
import os
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# Specifacations for PyInstaller
spec_file = 'PyPlane.spec'

# Directories where to build into
script_dir = os.getcwd()
build_dir = os.path.join(script_dir, 'build')
temp_dir = os.path.join(script_dir, 'temp')

# Build the command string
cmd = ['--clean', '--distpath=%s' % build_dir, '--workpath=%s' % temp_dir, spec_file]

# Clean-up environment
if os.path.exists(build_dir):
    shutil.rmtree(build_dir, ignore_errors=True)

# Call pyinstaller
print('Executing pyinstaller %s' % ' '.join(cmd))
pyinstaller_run(cmd)
