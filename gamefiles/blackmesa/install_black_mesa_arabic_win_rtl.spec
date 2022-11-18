# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\\blackmesa\\install_black_mesa_patch_arabic_rtl_win.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[
    (os.environ['modpath']+'\\resource\\closecaption_uarabic.dat', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\bms_english.txt', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\clientscheme.res', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\credits_english.txt', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\resource\\crowbarcollective_english.txt', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\scripts\\credits.txt', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\ui\\routeview-audio.qml', 'src\gamefiles\\blackmesa'),
    (os.environ['modpath']+'\\ui\\l10n.qml', 'src\gamefiles\\blackmesa'),
    ('Black Mesa Arabic RTL.json', 'src\gamefiles\\blackmesa'),
    ('Black Mesa Arabic RTL private.json', 'src\gamefiles\\blackmesa')],
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
    name='install_black_mesa_a_win_rtl',
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