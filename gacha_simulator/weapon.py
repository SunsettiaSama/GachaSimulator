# -*- coding: utf-8 -*-
"""
武器池模块
基于 AdvancedGachaSimulator 创建神铸赋形武器池
"""

from .base import AdvancedGachaSimulator, GachaResult
from .config import WEAPON_POOL_CONFIG, PoolConfigManager
from typing import Optional, Dict


class WeaponPool(AdvancedGachaSimulator):
    """
    武器池类
    继承自 AdvancedGachaSimulator，使用武器池配置
    特点：概率略高、保底更早、大保底更少
    """
    
    def __init__(self, config: Optional[Dict] = None, use_custom_config: bool = False):
        """
        初始化武器池
        
        Args:
            config: 自定义配置（可选）
            use_custom_config: 是否使用自定义配置（默认 False，使用默认武器池配置）
        """
        if use_custom_config and config:
            # 使用自定义配置
            super().__init__(config)
            self.pool_name = config.get('name', '自定义武器池')
            self.pool_description = config.get('description', '自定义武器祈愿')
        else:
            # 使用默认武器池配置
            pool_config = WEAPON_POOL_CONFIG.copy()
            if config:
                # 合并用户自定义配置
                pool_config.update(config)
            super().__init__(pool_config)
            self.pool_name = pool_config['name']
            self.pool_description = pool_config['description']
        
        self.pool_type = 'weapon'
        
        # 武器池特有属性（命定值机制）
        self.fate_points = 0  # 命定值计数（0-2）
        self.fate_points_enabled = True
    
    def get_pool_info(self) -> Dict:
        """
        获取池子信息
        
        Returns:
            Dict: 池子基本信息
        """
        return {
            'pool_type': self.pool_type,
            'pool_name': self.pool_name,
            'pool_description': self.pool_description,
            'base_5star_prob': self.base_probabilities[self.rate_up_rarity],
            'hard_pity': self.hard_pity,
            'big_pity': self.big_pity if self.guarantee_enabled else None,
            'rate_up_prob': self.rate_up_prob if self.guarantee_enabled else None,
            'fate_points': self.fate_points if self.fate_points_enabled else None,
        }
    
    def single_draw(self) -> GachaResult:
        """
        单次抽卡（重写以实现命定值机制）
        
        Returns:
            GachaResult: 抽卡结果
        """
        result = super().single_draw()
        
        # 命定值机制：抽到非UP五星时增加命定值
        if self.fate_points_enabled and result.is_top_rarity and not result.is_rate_up:
            self.fate_points += 1
            # 命定值达到2时，下次必定UP
            if self.fate_points >= 2:
                self.is_guaranteed_rate_up = True
        
        # 抽到UP五星时重置命定值
        if result.is_top_rarity and result.is_rate_up:
            self.fate_points = 0
        
        return result
    
    def reset_statistics(self):
        """重置统计（包括命定值）"""
        super().reset_statistics()
        self.fate_points = 0
    
    def get_statistics(self) -> Dict:
        """
        获取详细统计信息（包括命定值）
        
        Returns:
            Dict: 统计信息字典
        """
        stats = super().get_statistics()
        
        # 添加命定值信息
        if self.fate_points_enabled:
            stats['fate_points_info'] = {
                'current_points': self.fate_points,
                'max_points': 2,
                'guaranteed_next': self.fate_points >= 2
            }
        
        return stats
    
    def display_pool_info(self):
        """显示池子信息（终端输出）"""
        info = self.get_pool_info()
        print("=" * 70)
        print(f"{info['pool_name']}".center(70))
        print("=" * 70)
        print(f"描述: {info['pool_description']}")
        print(f"池子类型: {info['pool_type']}")
        print(f"\n{'概率信息':-^70}")
        print(f"五星基础概率: {info['base_5star_prob']*100:.3f}%")
        print(f"软保底: {self.pity_threshold} 抽")
        print(f"硬保底: {info['hard_pity']} 抽")
        if info['big_pity']:
            print(f"大保底: {info['big_pity']} 抽")
            print(f"UP概率: {info['rate_up_prob']*100:.1f}%")
        if info['fate_points'] is not None:
            print(f"\n{'命定值机制':-^70}")
            print(f"当前命定值: {info['fate_points']}/2")
            print(f"说明: 抽到非UP五星时命定值+1，达到2时下次必定UP")
        print("=" * 70)
    
    def display_statistics(self):
        """显示统计信息（重写以显示命定值）"""
        super().display_statistics()
        
        # 显示命定值信息
        if self.fate_points_enabled:
            print(f"\n{'命定值信息':-^70}")
            print(f"当前命定值: {self.fate_points}/2")
            if self.fate_points >= 2:
                print(f"状态: 已触发命定值保底，下次必定UP！")
            else:
                print(f"状态: 距离命定值保底还需 {2 - self.fate_points} 次非UP五星")
    
    def __repr__(self):
        return f"WeaponPool(name='{self.pool_name}', draws={self.total_draws}, fate_points={self.fate_points})"


# ==================== 预设武器池 ====================

def create_standard_weapon_pool() -> WeaponPool:
    """创建标准武器池（默认配置）"""
    return WeaponPool()


def create_custom_weapon_pool(config: Dict) -> WeaponPool:
    """
    创建自定义武器池
    
    Args:
        config: 自定义配置字典
    
    Returns:
        WeaponPool: 武器池实例
    """
    return WeaponPool(config, use_custom_config=True)


# ==================== 使用示例 ====================
if __name__ == '__main__':
    print("=" * 70)
    print("武器池测试".center(70))
    print("=" * 70)
    
    # 创建标准武器池
    weapon_pool = create_standard_weapon_pool()
    weapon_pool.display_pool_info()
    
    # 进行10连抽
    print(f"\n{'进行10连抽':-^70}")
    results = weapon_pool.multi_draw(10)
    print(f"抽卡结果: {results}")
    
    # 显示统计
    stats = weapon_pool.get_statistics()
    print(f"\n当前统计:")
    print(f"  总抽数: {stats['total_draws']}")
    print(f"  距上次五星: {stats['pity_info']['draws_since_top_rarity']}")
    print(f"  命定值: {stats['fate_points_info']['current_points']}/2")
    print(f"  是否保底UP: {stats['pity_info']['is_guaranteed_rate_up']}")
    
    # 大量模拟
    print(f"\n{'模拟10万抽':-^70}")
    weapon_pool.multi_draw(100000)
    
    # 显示详细统计
    weapon_pool.display_statistics()
    
    # 理论 vs 实际
    theoretical = weapon_pool.calculate_theoretical_stats()
    empirical = weapon_pool.calculate_empirical_stats()
    
    print(f"\n{'理论 vs 实际':-^70}")
    print(f"期望抽数: 理论={theoretical['expected_draws_for_up']:.2f}, "
          f"实际={empirical['expected_draws_for_up']:.2f}")
    print(f"期望回报: 理论={theoretical['expected_total_reward']:.2f}, "
          f"实际={empirical['expected_total_reward']:.2f}")
    
    print("\n" + "=" * 70)
    
    # 测试命定值机制
    print("\n" + "=" * 70)
    print("命定值机制测试".center(70))
    print("=" * 70)
    
    weapon_pool2 = create_standard_weapon_pool()
    print("\n模拟抽取，直到触发命定值保底...")
    
    draws_count = 0
    while weapon_pool2.fate_points < 2 and draws_count < 500:
        result = weapon_pool2.single_draw()
        draws_count += 1
        
        if result.is_top_rarity:
            print(f"第 {draws_count} 抽: {result} | 命定值: {weapon_pool2.fate_points}/2")
            
            if weapon_pool2.fate_points >= 2:
                print("\n已触发命定值保底！下次必定UP五星武器！")
                
                # 再抽一次验证
                next_result = weapon_pool2.single_draw()
                print(f"验证抽: {next_result}")
                if next_result.is_rate_up:
                    print("✓ 命定值机制生效！抽到UP五星武器！")
                break
    
    print("\n" + "=" * 70)
