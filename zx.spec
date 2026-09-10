# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['zx.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='zx',
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

hiddenimports=[
    "stdlib",
    "stdlib.audio",
    "stdlib.files",
    "stdlib.fs",
    "stdlib.graphics",
    "stdlib.gui",
    "stdlib.internet",
    "stdlib.mathx",
    "stdlib.network",
    "stdlib.sound",
    "stdlib.webapp",
    "stdlib.window",
]

datas=[
    ("stdlib", "stdlib"),
    ("core", "core"),
]
