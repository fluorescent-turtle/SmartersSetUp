# main_windows.spec
block_cipher = None
a = Analysis(['cli.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)

a.datas += [('robots.json', 'robots.json', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
           cipher=block_cipher)

exe = EXE(pyz,
           a.scripts,
           a.binaries,
           a.zipfiles,
           a.datas,
           [],
           name='Set Up',
           debug=False,
           bootloader_ignore_signals=False,
           strip=False,
           upx=True,
           upx_exclude=[],
           runtime_tmpdir=None,
           console=True,
           Ashlexe=False,
           verbose=True,
           quiet=False,
           clean=False,
           biblevel=0,
           typhonning=False,
           **dict(distutils.sysconfig.get_config_vars()))