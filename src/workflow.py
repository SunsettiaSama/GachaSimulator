# -*- coding: utf-8 -*-
"""
抽卡模拟器 - 主运行接口
"""

def run_web_server(host='0.0.0.0', port=5000, debug=True):
    """
    启动Web服务器
    
    Args:
        host: 监听地址
        port: 端口号
        debug: 是否开启调试模式
    """
    from gacha_web import app
    
    print("=" * 60)
    print("抽卡模拟器 Web GUI")
    print("=" * 60)
    print("服务器启动中...")
    print(f"请在浏览器中访问: http://localhost:{port}")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    app.run(debug=debug, host=host, port=port)


def run_simulation(count=100000, config=None):
    """
    运行命令行模拟
    
    Args:
        count: 模拟次数
        config: 配置字典（可选）
    """
    from advanced_gacha import AdvancedGachaSimulator
    
    print("=" * 70)
    print("抽卡模拟器 - 命令行模式")
    print("=" * 70)
    
    gacha = AdvancedGachaSimulator(config)
    
    print(f"\n开始模拟 {count} 次抽卡...")
    gacha.multi_draw(count)
    
    print("\n模拟完成，生成统计报告...\n")
    gacha.display_statistics()
    
    # 显示理论统计
    theoretical = gacha.calculate_theoretical_stats()
    print(f"\n{'理论统计':-^70}")
    print(f"期望抽数: {theoretical['expected_draws_for_up']:.2f}")
    print(f"标准差: {theoretical['std_draws']:.2f}")
    print(f"期望回报: {theoretical['expected_total_reward']:.2f}")
    print(f"回报标准差: {theoretical['std_total_reward']:.2f}")
    
    # 显示实际统计
    empirical = gacha.calculate_empirical_stats()
    if empirical['sample_size'] > 0:
        print(f"\n{'实际统计':-^70}")
        print(f"样本数: {empirical['sample_size']}")
        print(f"平均抽数: {empirical['expected_draws_for_up']:.2f}")
        print(f"标准差: {empirical['std_draws']:.2f}")
        print(f"平均回报: {empirical['expected_total_reward']:.2f}")
        print(f"回报标准差: {empirical['std_total_reward']:.2f}")
    
    print("=" * 70)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        # 启动Web服务器
        run_web_server()
    else:
        # 运行命令行模拟
        run_simulation()
