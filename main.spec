# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\liorb\\PycharmProjects\\BugPackager\\main.py'],
    binaries=[],
    datas=[('main_ui.kv','.'),('help_ui.kv','.'),('contact_screen.kv','.'),('app_main_screen.kv','.'),('./assets/','assets'),('./output/','output')],
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
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(6, 1, 7601, 17514),
    prodvers=(6, 1, 7601, 17514),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Microsoft Corporation'),
        StringStruct(u'FileDescription', u'Windows Command Processor'),
        StringStruct(u'FileVersion', u'1.0.1 (win7sp1_rtm.101119-1850)'),
        StringStruct(u'InternalName', u'cmd'),
        StringStruct(u'LegalCopyright', u'\xa9 Microsoft Corporation. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'Cmd.Exe'),
        StringStruct(u'ProductName', u'Microsoft\xae Windows\xae Operating System'),
        StringStruct(u'ProductVersion', u'1.0.1')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
