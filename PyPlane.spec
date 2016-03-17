# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['core', 'D:\\Users\\winkler\\Uni\\Projekte\\Allgemein\\pyplane'],
             hiddenimports=['scipy.special._ufuncs_cxx'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyPlane.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='resources\\pyplane_icon_32px.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='PyPlane')
