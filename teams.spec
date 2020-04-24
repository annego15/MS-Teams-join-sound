# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['teams.py'],
             pathex=['/Users/andresneff/Documents/2. Freizeit/3.Programme/Teams'],
             binaries=[],
             datas=[('./error.wav', '.'), ('./login.wav', '.'), ('./logout.wav', '.'), ('./unmuted.wav', '.')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='teams',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='/Users/andresneff/Documents/2. Freizeit/3.Programme/Teams/microsoft_teams.icns')
