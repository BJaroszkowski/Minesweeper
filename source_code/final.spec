# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'flag.bmp', '.' ),
         ( 'FreeSansBold.ttf', '.' ),
         ( 'icon.png', '.' )
         ]

a = Analysis(['main.py'],
             pathex=['/path/to/source_code'],
             binaries=[],
             datas=added_files,
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='minesweeper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='minesweeper.ico',
          console=False)
