# -*- coding: utf-8 -*-
"""
基础示例：角色池抽卡
演示如何使用标准角色池进行抽卡
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gacha_simulator import create_standard_character_pool


def main():
    print("=" * 60)
    print("角色池抽卡示例".center(60))
    print("=" * 60)
    
    # 创建标准角色池
    pool = create_standard_character_pool()
    
    # 查看池子信息
    info = pool.get_pool_info()
    print("\n池子信息：")
    print(f"池子名称: {info['pool_name']}")
    print(f"池子类型: {info['pool_type']}")
    print(f"五星基础概率: {info['base_5star_prob'] * 100:.3f}%")
    print(f"硬保底: {info['hard_pity']}抽")
    if info.get('big_pity'):
        print(f"大保底: {info['big_pity']}抽")
    
    # 单抽测试
    print("\n" + "=" * 60)
    print("单抽测试")
    print("=" * 60)
    result = pool.single_draw()
    print(f"稀有度: {result.rarity}")
    print(f"是否UP: {result.is_rate_up}")
    print(f"回报值: {result.reward}")
    
    # 十连测试
    print("\n" + "=" * 60)
    print("十连测试")
    print("=" * 60)
    results = pool.multi_draw(10)
    for i, r in enumerate(results, 1):
        up_marker = " [UP]" if r.is_rate_up else ""
        print(f"第{i}抽: {r.rarity}{up_marker} (回报: {r.reward})")
    
    # 查看统计信息
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)
    stats = pool.get_statistics()
    print(f"总抽数: {stats['total_draws']}")
    print(f"总回报: {stats['total_rewards']}")
    print(f"各稀有度统计:")
    for rarity, info_dict in stats['rarity_stats'].items():
        count = info_dict['count']
        percentage = (count / stats['total_draws'] * 100) if stats['total_draws'] > 0 else 0
        print(f"  {rarity}: {count} ({percentage:.2f}%)")
    
    # 大规模模拟
    print("\n" + "=" * 60)
    print("大规模模拟 (10000抽)")
    print("=" * 60)
    pool.reset_statistics()
    pool.multi_draw(10000)
    
    stats = pool.get_statistics()
    
    print("\n实际统计:")
    top_rarity = stats['pity_info']['top_rarity_name']
    top_stats = stats['top_rarity_stats']
    
    for rarity, info_dict in stats['rarity_stats'].items():
        count = info_dict['count']
        percentage = (count / stats['total_draws'] * 100) if stats['total_draws'] > 0 else 0
        print(f"  {rarity}: {count} ({percentage:.2f}%)")
    
    print(f"\n{top_rarity}详细统计:")
    if top_stats.get('total', 0) > 0:
        avg_draws = stats['total_draws'] / top_stats['total']
        print(f"  平均每{top_rarity}抽数: {avg_draws:.2f}")
    else:
        print(f"  平均每{top_rarity}抽数: N/A (未抽到)")
    print(f"  {top_rarity}总数: {top_stats.get('total', 0)}")
    print(f"  UP {top_rarity}数: {top_stats.get('rate_up', 0)}")
    if top_stats.get('total', 0) > 0:
        print(f"  UP率: {top_stats.get('rate_up_ratio', 0) * 100:.2f}%")


if __name__ == '__main__':
    main()
