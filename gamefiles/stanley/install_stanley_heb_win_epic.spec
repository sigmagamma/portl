# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\stanley\install_stanley_heb_win_patch_epic.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[
    (os.environ['modpath']+'\\resource\\subtitles_english.dat', 'src\gamefiles\\stanley'),
    (os.environ['modpath']+'\\resource\\basemodui_english.txt', 'src\gamefiles\\stanley'),
    (os.environ['modpath']+'\\resource\\basemodui_scheme.res', 'src\gamefiles\\stanley'),
    (os.environ['modpath']+'\\resource\\gameui_english.txt', 'src\gamefiles\\stanley'),
    (os.environ['modpath']+'\\resource\\ui\\basemodui\\mainmenu_tsp.res', 'src\gamefiles\\stanley'),
    (os.environ['modpath']+'\\cfg\\config.cfg', 'src\gamefiles\\stanley'),
    ('The Stanley Parable RTL.json', 'src\gamefiles\\stanley'),
    ('gameinfo.txt', 'src\gamefiles\\stanley')],
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
    Tree(os.environ['modpath']+'\\materials', prefix='src\gamefiles\\stanley\materials\\'),
    a.zipfiles,
    a.datas,
    [],
    name='install_stanley_heb_win_epic',
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
    uac_admin=True,
)
