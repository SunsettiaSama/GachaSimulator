# -*- coding: utf-8 -*-
"""
Web界面启动示例
演示如何启动Web可视化界面
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from webui.app import run_server


def main():
    """启动Web界面"""
    print("启动抽卡模拟器Web界面...")
    print("\n功能说明：")
    print("  1. 角色池和武器池切换")
    print("  2. 单抽/十连抽卡")
    print("  3. 大规模模拟测试")
    print("  4. 实时统计图表")
    print("  5. 历史记录查看")
    print("\n启动后请在浏览器中访问显示的地址")
    print("-" * 60)
    
    # 启动服务器
    # host='0.0.0.0' 允许局域网访问
    # port=5000 端口号
    # debug=True 开启调试模式（生产环境建议设为False）
    run_server(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    main()
