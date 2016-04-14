# -*- coding: utf-8 -*-
"""
Builds a Windows executable of PyPlane 

Make sure that pyinstaller is properly installed in your Python distribution!

Please note in order to build a properly working exe:
-> Include the statement "import FileDialog" in main.py (an error in matplotlib)

Created on Fri Mar 27 16:16:28 2015

@author: winkler
"""




import subprocess
import os.path
import shutil


infile      = 'main.py'
descrfile   = 'core\\config_description.py'
exename     = 'PyPlane'

config_dir  = 'config'
lib_dir     = 'library'

temp_dir   = 'windows\\temp'
build_dir  = 'windows\\build'
exe_dir    = build_dir + '\\' + exename + '\\'
paths      = 'core'


cmd = 'pyinstaller --clean --distpath=%s --workpath=%s --paths=%s \
    --hidden-import=scipy.special._ufuncs_cxx\
    --hidden-import=mpl_toolkits\
    --hidden-import=scipy.linalg.cython_blas\
    --hidden-import=scipy.linalg.cython_lapack\
    --icon=resources\pyplane_icon_32px.ico --name=%s %s' % (build_dir, temp_dir, paths, exename, infile)
print 'Calling:', cmd

if os.path.exists(build_dir):
    shutil.rmtree(build_dir, ignore_errors=True)

result = subprocess.call(cmd)

if result:
    print 'Compilation failed'
else:
    print 'Compilation success!'


# Copy the config directory to the build directory

shutil.copytree(config_dir, exe_dir+config_dir)
shutil.copytree(lib_dir, exe_dir+lib_dir)
os.mkdir(os.path.dirname(exe_dir+descrfile))
shutil.copyfile(descrfile, exe_dir+descrfile)


