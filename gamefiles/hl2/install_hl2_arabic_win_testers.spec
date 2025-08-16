# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\..\\src\\hl2\\install_hl2_non_patch_arabic_win.py'],
    pathex=['..\\..\\'],
    binaries=[],
    datas=[
    ('Half Life 2 testers.json', 'src\gamefiles\\hl2'),
    ('Half Life 2 testers private.json', 'src\gamefiles\\hl2')],
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
    Tree('ep2_source', prefix='src\\gamefiles\\hl2\\ep2_source\\'),
    Tree('hl2_complete_source', prefix='src\\gamefiles\\hl2\\hl2_complete_source\\'),
    Tree('lostcoast_source', prefix='src\\gamefiles\\hl2\\lostcoast_source\\'),
    Tree('episodic_source', prefix='src\\gamefiles\\hl2\\episodic_source\\'),
    Tree('platform_source', prefix='src\\gamefiles\\hl2\\platform_source\\'),
    a.zipfiles,
    a.datas,
    [],
    name='install_hl2_a_win_testers',
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