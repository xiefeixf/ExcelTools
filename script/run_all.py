# -*- coding: utf-8 -*-
"""
ExcelTools 主程序入口
协调执行所有转换脚本
"""

import os
import sys
from pathlib import Path

# 获取当前脚本所在目录
SCRIPT_DIR = Path(__file__).parent

def run_script(script_name):
    """运行指定的 Python 脚本"""
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        print(f"✗ 错误：脚本 {script_name} 不存在")
        return False
    
    print(f"\n{'='*60}")
    print(f"正在执行：{script_name}")
    print('='*60)
    
    # 将脚本目录添加到路径
    sys.path.insert(0, str(SCRIPT_DIR))
    
    try:
        # 导入并执行模块
        module_name = script_name.replace('.py', '')
        module = __import__(module_name)
        module.main()
        return True
    except Exception as e:
        print(f"✗ 错误：执行 {script_name} 时发生异常")
        print(f"详情：{e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("ExcelTools - Excel 转 TypeScript 工具")
    print("="*60)
    print()
    
    # 检查配置文件
    config_file = SCRIPT_DIR.parent / "routePath.txt"
    if not config_file.exists():
        print(f"⚠ 警告：未找到 routePath.txt 配置文件，将使用默认路径")
        print(f"请在项目根目录创建 routePath.txt 文件")
        print()
    
    # 按顺序执行所有脚本
    scripts = [
        ("excelToTs.py", "TypeScript 类型定义生成"),
        ("excelToTsData.py", "TypeScript 数据文件生成"),
        ("generateGlobalConfig.py", "全局配置文件生成")
    ]
    
    success_count = 0
    fail_count = 0
    
    for script_name, description in scripts:
        print(f"\n步骤 {success_count + fail_count + 1}/3: {description}")
        
        if run_script(script_name):
            print(f"✓ {script_name} 执行成功")
            success_count += 1
        else:
            print(f"✗ {script_name} 执行失败")
            fail_count += 1
            break  # 如果某一步失败，停止后续执行
    
    # 显示最终结果
    print("\n" + "="*60)
    if fail_count == 0:
        print("✓ 所有步骤执行完成！")
        print("="*60)
        print("\n生成的文件位于：")
        print("  - assets/Init/Config/ConfigType.ts (类型定义)")
        print("  - assets/Init/Config/ConfigData.ts (数据文件)")
        print("  - assets/Init/Config/GlobalConfig.ts (全局配置)")
    else:
        print(f"✗ 执行过程中出现错误，共成功 {success_count}/{len(scripts)} 个步骤")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()