# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import glob
from PyInstaller.utils.hooks import get_module_file_attribute

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

repo_dir = os.path.realpath('../..')
module_dir = os.path.join(repo_dir, 'pyplane')

# Config data and settings of PyPlane needs to be shipped as well
data_files = [(filename, './pyplane/library') for filename in glob.glob(os.path.join(module_dir, 'library', '*.ppf'))]
data_files += [(os.path.join(module_dir, 'config', 'default'), './pyplane/config')]
data_files += [(os.path.join(module_dir, 'core', 'config_description.py'), './pyplane/core')]

a = Analysis([os.path.join(repo_dir, 'run_pyplane.py')],
             pathex=[repo_dir, module_dir, os.path.join(module_dir, 'core')],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
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
          console=True , icon=os.path.join(module_dir, 'resources', 'pyplane_icon_32px.ico'))
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PyPlane')
