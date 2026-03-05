# -*- coding: utf-8 -*-
"""
自定义配置示例
演示如何创建自定义概率和保底机制的抽卡池
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gacha_simulator import CharacterPool


def main():
    print("=" * 60)
    print("自定义抽卡池示例".center(60))
    print("=" * 60)
    
    # 自定义配置：高概率池（适合福利活动）
    high_rate_config = {
        'name': '福利池',
        'base_probabilities': {
            'SSR': 0.03,      # 3% SSR概率（是标准池的5倍）
            'SR': 0.10,       # 10% SR概率
            'R': 0.40,        # 40% R概率
            'N': 0.47         # 47% N概率
        },
        'pity_enabled': True,
        'pity_threshold': 50,   # 50抽开始软保底
        'pity_increment': 0.08,  # 更高的保底增长率
        'hard_pity': 60,         # 60抽硬保底
        'reward_enabled': True,
        'rewards': {
            'SSR': 2000,
            'SR': 200,
            'R': 50,
            'N': 20
        },
        'guarantee_enabled': True,
        'rate_up_rarity': 'SSR',
        'rate_up_prob': 0.5,
        'big_pity': 120
    }
    
    # 创建自定义池子
    pool = CharacterPool(high_rate_config, use_custom_config=True)
    
    info = pool.get_pool_info()
    print(f"\n池子名称: {info['pool_name']}")
    print(f"SSR基础概率: {high_rate_config['base_probabilities']['SSR'] * 100}% (标准池为0.8%)")
    print(f"软保底: {high_rate_config['pity_threshold']}抽")
    print(f"硬保底: {info['hard_pity']}抽")
    
    # 进行模拟抽卡
    print("\n" + "=" * 60)
    print("100连测试")
    print("=" * 60)
    
    results = pool.multi_draw(100)
    
    # 统计SSR抽数
    ssr_positions = []
    for i, r in enumerate(results, 1):
        if r.rarity == 'SSR' and r.is_top_rarity:
            ssr_positions.append(i)
    
    print(f"100抽中获得 {len(ssr_positions)} 个SSR")
    print(f"出货位置: {ssr_positions}")
    
    # 大规模统计
    print("\n" + "=" * 60)
    print("大规模统计 (10000抽)")
    print("=" * 60)
    pool.reset_statistics()
    pool.multi_draw(10000)
    
    stats = pool.get_statistics()
    ssr_info = stats['rarity_stats'].get('SSR', {})
    sr_info = stats['rarity_stats'].get('SR', {})
    
    ssr_count = ssr_info.get('count', 0)
    sr_count = sr_info.get('count', 0)
    
    print(f"\nSSR出货率: {(ssr_count / stats['total_draws'] * 100):.2f}%")
    print(f"SR出货率: {(sr_count / stats['total_draws'] * 100):.2f}%")
    
    top_stats = stats['top_rarity_stats']
    if top_stats.get('total', 0) > 0:
        avg_draws = stats['total_draws'] / top_stats['total']
        print(f"平均每个SSR抽数: {avg_draws:.2f}")
    
    # 对比标准池
    print("\n" + "=" * 60)
    print("自定义配置 - 稀有度池")
    print("=" * 60)
    
    # 创建一个完全自定义的稀有度系统
    custom_rarity_config = {
        'name': '星级池',
        'base_probabilities': {
            '金色': 0.01,
            '紫色': 0.05,
            '蓝色': 0.20,
            '绿色': 0.74
        },
        'pity_enabled': True,
        'pity_threshold': 70,
        'pity_increment': 0.06,
        'hard_pity': 90,
        'reward_enabled': True,
        'rewards': {
            '金色': 3000,
            '紫色': 300,
            '蓝色': 30,
            '绿色': 10
        },
        'guarantee_enabled': True,
        'rate_up_rarity': '金色',
        'rate_up_prob': 0.5,
        'big_pity': 180
    }
    
    custom_pool = CharacterPool(custom_rarity_config, use_custom_config=True)
    
    print(f"\n池子名称: {custom_pool.config['name']}")
    print("自定义稀有度:")
    for rarity, prob in custom_rarity_config['base_probabilities'].items():
        print(f"  {rarity}: {prob * 100:.1f}%")
    
    # 十连测试
    print("\n十连测试:")
    results = custom_pool.multi_draw(10)
    for i, r in enumerate(results, 1):
        print(f"  第{i}抽: {r.rarity} (回报: {r.reward})")


if __name__ == '__main__':
    main()
