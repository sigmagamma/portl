# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\portal\install_po_rtl_heb_win_rtl.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[(os.environ['modpath']+'\\resource\\closecaption_english.dat', 'src\gamefiles\\portal'),
    (os.environ['modpath']+'\\resource\\clientscheme.res', 'src\gamefiles\\portal'),
    ('Portal RTL.json', 'src\gamefiles\\portal'),
    (os.environ['modpath']+'\\scripts\\credits.txt', 'src\gamefiles\\portal'),
    (os.environ['modpath']+'\\surprise\\00_part1_entry-2.wav', 'src\gamefiles\\portal\surprise')],
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
    Tree('.\\materials', prefix='src\gamefiles\\portal\materials\\'),
    a.zipfiles,
    a.datas,
    [],
    name='install_portal_heb_win_rtl',
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
