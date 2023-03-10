# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\liorb\\PycharmProjects\\BugPackager\\main.py'],
    binaries=[],
    datas=[('main_ui.kv','.'),('app_db.db','.'),('help_ui.kv','.'),('app_main_screen_ui.kv','.'),('./assets/','assets'),('./output/','output'),('help_ui.kv','.'),('info_popup_ui.kv','.'),('contact_screen_ui.kv','.')],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
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
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='Bug Packer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='C:\\Users\\liorb\\PycharmProjects\\BugPackager\\assets\\icons\\icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)