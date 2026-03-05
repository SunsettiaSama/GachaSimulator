# -*- coding: utf-8 -*-
"""
武器池示例：命定值机制
演示武器池的命定值（Epitomized Path）机制
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gacha_simulator import create_standard_weapon_pool


def main():
    print("=" * 60)
    print("武器池命定值机制示例".center(60))
    print("=" * 60)
    
    # 创建武器池
    pool = create_standard_weapon_pool()
    
    # 查看池子信息
    info = pool.get_pool_info()
    print("\n池子信息：")
    print(f"池子名称: {info['pool_name']}")
    print(f"五星基础概率: {info['base_5star_prob'] * 100:.3f}%")
    print(f"武器池特色: 命定值机制（2次歪后保底）")
    
    print("\n" + "=" * 60)
    print("模拟抽取过程")
    print("=" * 60)
    
    five_star_count = 0
    target_count = 0
    draws_count = 0
    
    # 持续抽卡直到获得3个目标五星武器
    while target_count < 3:
        result = pool.single_draw()
        draws_count += 1
        
        if result.is_top_rarity:  # 使用is_top_rarity判断是否为最高稀有度
            five_star_count += 1
            if result.is_rate_up:
                target_count += 1
                print(f"\n第{draws_count}抽: 获得目标六星武器！[成功]")
                print(f"  当前命定值: {pool.fate_points}")
            else:
                print(f"\n第{draws_count}抽: 获得非UP六星武器 (歪了)")
                print(f"  命定值 +1，当前: {pool.fate_points}")
    
    print("\n" + "=" * 60)
    print("最终统计")
    print("=" * 60)
    stats = pool.get_statistics()
    top_rarity = stats['pity_info']['top_rarity_name']
    top_stats = stats['top_rarity_stats']
    
    print(f"总抽数: {draws_count}")
    print(f"获得{top_rarity}总数: {five_star_count}")
    print(f"获得目标{top_rarity}: {target_count}")
    print(f"平均每个目标{top_rarity}抽数: {draws_count / target_count:.2f}")
    
    # 重置并进行大规模统计
    print("\n" + "=" * 60)
    print("大规模统计 (10000抽)")
    print("=" * 60)
    pool.reset_statistics()
    pool.multi_draw(10000)
    
    stats = pool.get_statistics()
    top_rarity = stats['pity_info']['top_rarity_name']
    top_stats = stats['top_rarity_stats']
    
    five_star_info = stats['rarity_stats'].get(top_rarity, {})
    five_star_count = five_star_info.get('count', 0)
    
    print(f"\n{top_rarity}出货率: {(five_star_count / stats['total_draws'] * 100):.2f}%")
    print(f"{top_rarity}UP率: {top_stats.get('rate_up_ratio', 0) * 100:.2f}%")
    if top_stats.get('total', 0) > 0:
        avg_draws = stats['total_draws'] / top_stats['total']
        print(f"平均每个{top_rarity}抽数: {avg_draws:.2f}")


if __name__ == '__main__':
    main()
