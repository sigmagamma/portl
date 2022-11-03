# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\\blackmesa\\install_black_mesa_patch_arabic_win.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[
    (os.environ['modpath']+'\\resource\\closecaption_english.dat', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\bms_english.txt', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\clientscheme.res', 'src\gamefiles\\blackmesa'),
    ('Black Mesa Arabic.json', 'src\gamefiles\\blackmesa'),
    ('Black Mesa Arabic private.json', 'src\gamefiles\\blackmesa')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='install_black_mesa_a_win',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)