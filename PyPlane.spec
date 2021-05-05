# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import get_module_file_attribute

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

base_dir = os.getcwd()
pyplane_dir = os.path.join(base_dir, 'pyplane')

a = Analysis([os.path.join(pyplane_dir, 'main.py')],
             pathex=[pyplane_dir, os.path.join(pyplane_dir, 'core'), os.path.join(os.path.dirname(get_module_file_attribute('PyQt5')), 'Qt', 'bin'), os.path.dirname(get_module_file_attribute('zmq')), base_dir],
             binaries=[],
             datas=[],
             hiddenimports=['scipy.special._ufuncs_cxx', 'mpl_toolkits', 'scipy.linalg.cython_blas', 'scipy.linalg.cython_lapack', 'scipy._lib.messagestream', 'tkinter.filedialog'],
             hookspath=[os.path.join(base_dir, 'pyinstaller-hooks')],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PyPlane',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon=os.path.join(pyplane_dir, 'resources', 'pyplane_icon_32px.ico'))
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PyPlane')
