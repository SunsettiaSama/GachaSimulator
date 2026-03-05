# -*- coding: utf-8 -*-
"""
GachaSimulator 快速启动脚本
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def print_menu():
    """显示主菜单"""
    print("\n" + "=" * 60)
    print("GachaSimulator - 高级抽卡模拟器".center(60))
    print("=" * 60)
    print("\n请选择运行模式：")
    print("  1. 启动Web界面 (推荐)")
    print("  2. 运行基础示例 - 角色池")
    print("  3. 运行武器池示例 - 命定值机制")
    print("  4. 运行自定义池示例")
    print("  5. 交互式命令行菜单")
    print("  6. 大样本测试")
    print("  0. 退出")
    print("=" * 60)


def run_web():
    """启动Web界面"""
    from webui.app import run_server
    run_server(host='127.0.0.1', port=5000, debug=True)


def run_basic_example():
    """运行基础示例"""
    print("\n正在运行角色池基础示例...\n")
    os.system(f'python "{os.path.join(os.path.dirname(__file__), "examples", "basic_character_pool.py")}"')


def run_weapon_example():
    """运行武器池示例"""
    print("\n正在运行武器池命定值示例...\n")
    os.system(f'python "{os.path.join(os.path.dirname(__file__), "examples", "weapon_pool_fate.py")}"')


def run_custom_example():
    """运行自定义池示例"""
    print("\n正在运行自定义池示例...\n")
    os.system(f'python "{os.path.join(os.path.dirname(__file__), "examples", "custom_pool.py")}"')


def run_interactive_menu():
    """运行交互式菜单"""
    from main_menu import GachaMenu
    menu = GachaMenu()
    menu.run()


def run_large_test():
    """运行大样本测试"""
    print("\n正在运行大样本测试...\n")
    os.system(f'python "{os.path.join(os.path.dirname(__file__), "src", "large_sample_test.py")}"')


def main():
    """主函数"""
    while True:
        print_menu()
        choice = input("\n请输入选项 (0-6): ").strip()
        
        if choice == '0':
            print("\n感谢使用 GachaSimulator！")
            break
        elif choice == '1':
            run_web()
        elif choice == '2':
            run_basic_example()
        elif choice == '3':
            run_weapon_example()
        elif choice == '4':
            run_custom_example()
        elif choice == '5':
            run_interactive_menu()
        elif choice == '6':
            run_large_test()
        else:
            print("\n无效的选项，请重新输入！")
        
        if choice != '0' and choice != '1':
            input("\n按 Enter 键继续...")


if __name__ == '__main__':
    main()
