# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['e:/安装包/ExcelTools/script/run_all.py'],
    pathex=['e:/安装包/ExcelTools/script'],
    binaries=[],
    datas=[
        ('e:/安装包/ExcelTools/script/excelToTs.py', '.'),
        ('e:/安装包/ExcelTools/script/excelToTsData.py', '.'),
        ('e:/安装包/ExcelTools/script/generateGlobalConfig.py', '.'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'numpy',
    ],
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
    a.datas,
    [],
    name='ExcelTools',
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
