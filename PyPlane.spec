# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['core', 'D:\\winkler\\Uni\\Projekte\\Allgemein\\pyplane\\pyplane'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy.special._ufuncs_cxx', 'mpl_toolkits', 'scipy.linalg.cython_blas', 'scipy.linalg.cython_lapack'],
             hookspath=[],
             runtime_hooks=['runtime_hook_pyqt4.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyPlane',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='resources\\pyplane_icon_32px.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyPlane')
