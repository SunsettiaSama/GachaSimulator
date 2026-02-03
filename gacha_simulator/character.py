# -*- coding: utf-8 -*-
"""
角色池模块
基于 AdvancedGachaSimulator 创建角色祈愿池
"""

from .base import AdvancedGachaSimulator, GachaResult
from .config import CHARACTER_POOL_CONFIG, PoolConfigManager
from typing import Optional, Dict


class CharacterPool(AdvancedGachaSimulator):
    """
    角色池类
    继承自 AdvancedGachaSimulator，使用角色池配置
    """
    
    def __init__(self, config: Optional[Dict] = None, use_custom_config: bool = False):
        """
        初始化角色池
        
        Args:
            config: 自定义配置（可选）
            use_custom_config: 是否使用自定义配置（默认 False，使用默认角色池配置）
        """
        if use_custom_config and config:
            # 使用自定义配置
            super().__init__(config)
            self.pool_name = config.get('name', '自定义角色池')
            self.pool_description = config.get('description', '自定义角色祈愿')
        else:
            # 使用默认角色池配置
            pool_config = CHARACTER_POOL_CONFIG.copy()
            if config:
                # 合并用户自定义配置
                pool_config.update(config)
            super().__init__(pool_config)
            self.pool_name = pool_config['name']
            self.pool_description = pool_config['description']
        
        self.pool_type = 'character'
    
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
        }
    
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
        print(f"硬保底: {info['hard_pity']} 抽")
        if info['big_pity']:
            print(f"大保底: {info['big_pity']} 抽")
            print(f"UP概率: {info['rate_up_prob']*100:.1f}%")
        print("=" * 70)
    
    def __repr__(self):
        return f"CharacterPool(name='{self.pool_name}', draws={self.total_draws})"


# ==================== 预设角色池 ====================

def create_standard_character_pool() -> CharacterPool:
    """创建标准角色池（默认配置）"""
    return CharacterPool()


def create_limited_character_pool() -> CharacterPool:
    """创建限定角色池（高回报）"""
    limited_config = PoolConfigManager.get_config('limited_character')
    return CharacterPool(limited_config, use_custom_config=True)


def create_novice_character_pool() -> CharacterPool:
    """创建新手角色池（20抽必出）"""
    novice_config = PoolConfigManager.get_config('novice')
    return CharacterPool(novice_config, use_custom_config=True)


# ==================== 使用示例 ====================
if __name__ == '__main__':
    print("=" * 70)
    print("角色池测试".center(70))
    print("=" * 70)
    
    # 创建标准角色池
    char_pool = create_standard_character_pool()
    char_pool.display_pool_info()
    
    # 进行10连抽
    print(f"\n{'进行10连抽':-^70}")
    results = char_pool.multi_draw(10)
    print(f"抽卡结果: {results}")
    
    # 显示统计
    stats = char_pool.get_statistics()
    print(f"\n当前统计:")
    print(f"  总抽数: {stats['total_draws']}")
    print(f"  距上次五星: {stats['pity_info']['draws_since_top_rarity']}")
    print(f"  是否保底UP: {stats['pity_info']['is_guaranteed_rate_up']}")
    
    # 大量模拟
    print(f"\n{'模拟10万抽':-^70}")
    char_pool.multi_draw(100000)
    
    # 显示详细统计
    char_pool.display_statistics()
    
    # 理论 vs 实际
    theoretical = char_pool.calculate_theoretical_stats()
    empirical = char_pool.calculate_empirical_stats()
    
    print(f"\n{'理论 vs 实际':-^70}")
    print(f"期望抽数: 理论={theoretical['expected_draws_for_up']:.2f}, "
          f"实际={empirical['expected_draws_for_up']:.2f}")
    print(f"期望回报: 理论={theoretical['expected_total_reward']:.2f}, "
          f"实际={empirical['expected_total_reward']:.2f}")
    
    print("\n" + "=" * 70)
