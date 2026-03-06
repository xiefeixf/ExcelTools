# -*- coding: utf-8 -*-
"""
ExcelTools 打包工具
用于将 Python 脚本打包成独立的 EXE 可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPT_DIR = PROJECT_ROOT / "script"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

def check_pyinstaller():
    """检查是否安装了 PyInstaller"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller 已安装，版本：{PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller 未安装")
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安装完成")
        return True

def clean_build():
    """清理旧的构建文件"""
    print("\n正在清理旧的构建文件...")
    
    # 删除 dist 目录
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"✓ 已删除：{DIST_DIR}")
    
    # 删除 build 目录
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"✓ 已删除：{BUILD_DIR}")
    
    # 删除 .spec 文件
    for spec_file in SCRIPT_DIR.glob("*.spec"):
        spec_file.unlink()
        print(f"✓ 已删除：{spec_file}")

def build_run_all():
    """打包 run_all.py - 主程序"""
    print("\n" + "="*60)
    print("正在打包 run_all.py (主程序)...")
    print("="*60)
    
    # 将路径转换为正斜杠格式，避免转义问题
    script_path = str(SCRIPT_DIR / 'run_all.py').replace('\\', '/')
    script_dir_str = str(SCRIPT_DIR).replace('\\', '/')
    excelToTs_path = str(SCRIPT_DIR / 'excelToTs.py').replace('\\', '/')
    excelToTsData_path = str(SCRIPT_DIR / 'excelToTsData.py').replace('\\', '/')
    generateGlobalConfig_path = str(SCRIPT_DIR / 'generateGlobalConfig.py').replace('\\', '/')
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{script_path}'],
    pathex=['{script_dir_str}'],
    binaries=[],
    datas=[
        ('{excelToTs_path}', '.'),
        ('{excelToTsData_path}', '.'),
        ('{generateGlobalConfig_path}', '.'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={{}},
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
'''
    
    spec_file = SCRIPT_DIR / "run_all.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # 执行打包
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        str(spec_file)
    ], cwd=SCRIPT_DIR)
    
    print("\n✓ run_all.py 打包完成")

def build_individual_scripts():
    """单独打包每个脚本"""
    scripts = [
        ("excelToTs.py", "ExcelToTs"),
        ("excelToTsData.py", "ExcelToTsData"),
        ("generateGlobalConfig.py", "GenerateGlobalConfig"),
    ]
    
    for script_name, exe_name in scripts:
        print("\n" + "="*60)
        print(f"正在打包 {script_name}...")
        print("="*60)
        
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--console",
            "--name", exe_name,
            "--hidden-import=pandas",
            "--hidden-import=openpyxl",
            "--hidden-import=xlrd",
            "--hidden-import=numpy",
            str(SCRIPT_DIR / script_name)
        ], cwd=SCRIPT_DIR)
        
        print(f"\n✓ {script_name} 打包完成")

def copy_assets():
    """复制资源文件到输出目录"""
    assets_dir = PROJECT_ROOT / "assets"
    if assets_dir.exists():
        dist_assets = DIST_DIR / "assets"
        if not dist_assets.exists():
            shutil.copytree(assets_dir, dist_assets)
            print(f"\n✓ 已复制资源文件到：{dist_assets}")

def main():
    """主函数"""
    print("="*60)
    print("ExcelTools 打包工具")
    print("="*60)
    print(f"项目目录：{PROJECT_ROOT}")
    print(f"Python 版本：{sys.version}")
    print(f"Python 路径：{sys.executable}")
    
    # 检查并安装 PyInstaller
    check_pyinstaller()
    
    # 清理旧的构建文件
    clean_build()
    
    # 打包主程序
    build_run_all()
    
    # 复制资源文件
    copy_assets()
    
    # 显示输出结果
    print("\n" + "="*60)
    print("打包完成！")
    print("="*60)
    
    if (DIST_DIR / "ExcelTools.exe").exists():
        print(f"\n✓ 主程序已生成：{DIST_DIR / 'ExcelTools.exe'}")
    
    print(f"\n输出目录：{DIST_DIR}")
    print("\n提示：请将 assets 文件夹复制到生成的 exe 文件同级目录下")