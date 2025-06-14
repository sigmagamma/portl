# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\\portal2\\install_portal2_non_patch_arabic_win.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[
    ('Portal2 RTL Arabic testers.json', 'src\gamefiles\\portal2'),
    ('Portal2 RTL Arabic testers private.json', 'src\gamefiles\\portal2')],
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
    Tree('update_source', prefix='src\\gamefiles\\portal2\\update_source\\'),
    Tree('update_target_arabic', prefix='src\\gamefiles\\portal2\\update_target\\'),
    Tree('update_target_arabic', prefix='src\\gamefiles\\portal2\\temp_vpk\\'),
    a.zipfiles,
    a.datas,
    [],
    name='install_portal2_a_win_testers',
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