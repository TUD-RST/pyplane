# -*- mode: python -*-

block_cipher = None


a = Analysis(['d:\\winkler\\Uni\\Projekte\\Allgemein\\pyplane\\pyplane-jcwinkler\\pyplane\\main.py'],
             pathex=['c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'c:\\Progs\\WinPython-64bit-3.6.3.0Qt5\\python-3.6.3.amd64\\Lib\\site-packages\\zmq', 'd:\\winkler\\Uni\\Projekte\\Allgemein\\pyplane\\pyplane-jcwinkler\\pyplane\\core', 'd:\\winkler\\Uni\\Projekte\\Allgemein\\pyplane\\pyplane-jcwinkler'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy.special._ufuncs_cxx', 'mpl_toolkits', 'scipy.linalg.cython_blas', 'scipy.linalg.cython_lapack', 'scipy._lib.messagestream', 'tkinter.filedialog'],
             hookspath=[],
             runtime_hooks=[],
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
          console=True , icon='d:\\winkler\\Uni\\Projekte\\Allgemein\\pyplane\\pyplane-jcwinkler\\pyplane\\resources\\pyplane_icon_32px.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyPlane')
