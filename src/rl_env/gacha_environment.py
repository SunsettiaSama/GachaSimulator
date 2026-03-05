# -*- coding: utf-8 -*-
"""
双池抽卡环境
包含角色池和武器池，用于强化学习训练
"""

from typing import Dict, List, Tuple, Optional
import copy
from advanced_gacha import AdvancedGachaSimulator, GachaResult


class GachaEnvironment:
    """
    双池抽卡环境
    包含两个独立的池子：角色池和武器池
    每个池子维护独立的状态和保底机制
    """
    
    # 默认角色池配置
    DEFAULT_CHARACTER_CONFIG = {
        'base_probabilities': {
            '5-star': 0.006,   # 0.6% 基础概率
            '4-star': 0.051,   # 5.1%
            '3-star': 0.943,   # 94.3%
        },
        'pity_enabled': True,
        'pity_threshold': 73,      # 73抽后开始增加概率
        'pity_increment': 0.06,    # 每抽增加6%概率
        'hard_pity': 90,           # 90抽必出（硬保底）
        'reward_enabled': True,
        'rewards': {
            '5-star': 3000,   # 5星角色回报3000
            '4-star': 300,    # 4星角色回报300
            '3-star': 30,     # 3星武器回报30
        },
        'guarantee_enabled': True,
        'rate_up_rarity': '5-star',
        'rate_up_prob': 0.5,       # 50%是UP角色
        'big_pity': 180,           # 180抽必出UP角色（大保底）
    }
    
    # 默认武器池配置
    DEFAULT_WEAPON_CONFIG = {
        'base_probabilities': {
            '5-star': 0.007,   # 0.7% 基础概率（武器池概率略高）
            '4-star': 0.060,   # 6.0%
            '3-star': 0.933,   # 93.3%
        },
        'pity_enabled': True,
        'pity_threshold': 62,      # 62抽后开始增加概率（武器池软保底更早）
        'pity_increment': 0.07,    # 每抽增加7%概率（增长更快）
        'hard_pity': 80,           # 80抽必出（硬保底，比角色池少）
        'reward_enabled': True,
        'rewards': {
            '5-star': 2500,   # 5星武器回报2500（比角色略低）
            '4-star': 250,    # 4星武器回报250
            '3-star': 25,     # 3星武器回报25
        },
        'guarantee_enabled': True,
        'rate_up_rarity': '5-star',
        'rate_up_prob': 0.75,      # 75%是UP武器（武器池定轨后更容易）
        'big_pity': 160,           # 160抽必出UP武器（大保底，比角色池少）
    }
    
    def __init__(self, 
                 character_config: Optional[Dict] = None,
                 weapon_config: Optional[Dict] = None,
                 enable_character_pool: bool = True,
                 enable_weapon_pool: bool = True):
        """
        初始化双池环境
        
        Args:
            character_config: 角色池配置，None则使用默认配置
            weapon_config: 武器池配置，None则使用默认配置
            enable_character_pool: 是否启用角色池
            enable_weapon_pool: 是否启用武器池
        """
        # 配置处理
        self.character_config = character_config if character_config else self.DEFAULT_CHARACTER_CONFIG.copy()
        self.weapon_config = weapon_config if weapon_config else self.DEFAULT_WEAPON_CONFIG.copy()
        
        # 初始化角色池
        self.enable_character_pool = enable_character_pool
        self.character_pool = None
        if self.enable_character_pool:
            self.character_pool = AdvancedGachaSimulator(self.character_config)
        
        # 初始化武器池
        self.enable_weapon_pool = enable_weapon_pool
        self.weapon_pool = None
        if self.enable_weapon_pool:
            self.weapon_pool = AdvancedGachaSimulator(self.weapon_config)
        
        # 全局统计
        self.total_draws = 0
        self.total_rewards = 0
        
    def reset(self):
        """
        重置环境（重置两个池子的所有状态）
        
        Returns:
            Dict: 当前状态
        """
        if self.character_pool:
            self.character_pool.reset_statistics()
        
        if self.weapon_pool:
            self.weapon_pool.reset_statistics()
        
        self.total_draws = 0
        self.total_rewards = 0
        
        return self.get_state()
    
    def draw(self, pool_type: str, count: int = 1) -> Tuple[List[GachaResult], Dict]:
        """
        在指定池子中抽卡
        
        Args:
            pool_type: 池子类型，'character' 或 'weapon'
            count: 抽卡次数
        
        Returns:
            Tuple[List[GachaResult], Dict]: (抽卡结果列表, 更新后的状态)
        """
        if pool_type == 'character':
            if not self.enable_character_pool:
                raise ValueError("角色池未启用")
            results = self.character_pool.multi_draw(count)
        elif pool_type == 'weapon':
            if not self.enable_weapon_pool:
                raise ValueError("武器池未启用")
            results = self.weapon_pool.multi_draw(count)
        else:
            raise ValueError(f"无效的池子类型: {pool_type}，必须是 'character' 或 'weapon'")
        
        # 更新全局统计
        self.total_draws += count
        if pool_type == 'character' and self.character_pool:
            self.total_rewards += sum(r.reward for r in results)
        elif pool_type == 'weapon' and self.weapon_pool:
            self.total_rewards += sum(r.reward for r in results)
        
        return results, self.get_state()
    
    def single_draw(self, pool_type: str) -> Tuple[GachaResult, Dict]:
        """
        在指定池子中单抽
        
        Args:
            pool_type: 池子类型，'character' 或 'weapon'
        
        Returns:
            Tuple[GachaResult, Dict]: (抽卡结果, 更新后的状态)
        """
        results, state = self.draw(pool_type, count=1)
        return results[0], state
    
    def multi_draw(self, pool_type: str, count: int = 10) -> Tuple[List[GachaResult], Dict]:
        """
        在指定池子中多连抽
        
        Args:
            pool_type: 池子类型，'character' 或 'weapon'
            count: 抽卡次数（默认10连）
        
        Returns:
            Tuple[List[GachaResult], Dict]: (抽卡结果列表, 更新后的状态)
        """
        return self.draw(pool_type, count)
    
    def get_state(self) -> Dict:
        """
        获取当前环境状态（包含两个池子的状态）
        
        Returns:
            Dict: 当前状态，包含角色池和武器池的保底信息、统计信息等
        """
        state = {
            'total_draws': self.total_draws,
            'total_rewards': self.total_rewards,
        }
        
        # 角色池状态
        if self.character_pool:
            char_stats = self.character_pool.get_statistics()
            state['character_pool'] = {
                'enabled': True,
                'total_draws': char_stats['total_draws'],
                'total_rewards': char_stats['total_rewards'],
                'pity_info': char_stats['pity_info'],
                'top_rarity_stats': char_stats['top_rarity_stats'],
                'current_probabilities': self.character_pool._calculate_current_probabilities(),
            }
        else:
            state['character_pool'] = {'enabled': False}
        
        # 武器池状态
        if self.weapon_pool:
            weapon_stats = self.weapon_pool.get_statistics()
            state['weapon_pool'] = {
                'enabled': True,
                'total_draws': weapon_stats['total_draws'],
                'total_rewards': weapon_stats['total_rewards'],
                'pity_info': weapon_stats['pity_info'],
                'top_rarity_stats': weapon_stats['top_rarity_stats'],
                'current_probabilities': self.weapon_pool._calculate_current_probabilities(),
            }
        else:
            state['weapon_pool'] = {'enabled': False}
        
        return state
    
    def get_statistics(self) -> Dict:
        """
        获取详细统计信息（包含两个池子的完整统计）
        
        Returns:
            Dict: 包含角色池、武器池和全局统计的字典
        """
        statistics = {
            'global': {
                'total_draws': self.total_draws,
                'total_rewards': self.total_rewards,
            }
        }
        
        # 角色池统计
        if self.character_pool:
            char_stats = self.character_pool.get_statistics()
            char_theoretical = self.character_pool.calculate_theoretical_stats()
            statistics['character_pool'] = {
                'enabled': True,
                'statistics': char_stats,
                'theoretical': char_theoretical,
            }
        else:
            statistics['character_pool'] = {'enabled': False}
        
        # 武器池统计
        if self.weapon_pool:
            weapon_stats = self.weapon_pool.get_statistics()
            weapon_theoretical = self.weapon_pool.calculate_theoretical_stats()
            statistics['weapon_pool'] = {
                'enabled': True,
                'statistics': weapon_stats,
                'theoretical': weapon_theoretical,
            }
        else:
            statistics['weapon_pool'] = {'enabled': False}
        
        return statistics
    
    def calculate_reward(self, pool_type: str, results: List[GachaResult]) -> float:
        """
        计算本次抽卡的奖励值（用于RL训练）
        
        Args:
            pool_type: 池子类型
            results: 抽卡结果列表
        
        Returns:
            float: 奖励值
        """
        # 基础回报
        base_reward = sum(r.reward for r in results)
        
        # 额外奖励：抽到UP最高稀有度
        up_bonus = 0
        for r in results:
            if r.is_top_rarity and r.is_rate_up:
                up_bonus += 5000  # UP角色/武器额外奖励
        
        return base_reward + up_bonus
    
    def display_statistics(self):
        """
        显示详细统计信息（终端输出）
        """
        print("=" * 80)
        print("双池抽卡环境 - 统计报告".center(80))
        print("=" * 80)
        
        print(f"\n{'全局统计':-^80}")
        print(f"总抽数: {self.total_draws}")
        print(f"总回报: {self.total_rewards}")
        
        # 角色池统计
        if self.character_pool and self.character_pool.total_draws > 0:
            print(f"\n{'角色池':-^80}")
            self.character_pool.display_statistics()
        elif self.character_pool:
            print(f"\n{'角色池':-^80}")
            print("未进行抽卡")
        
        # 武器池统计
        if self.weapon_pool and self.weapon_pool.total_draws > 0:
            print(f"\n{'武器池':-^80}")
            self.weapon_pool.display_statistics()
        elif self.weapon_pool:
            print(f"\n{'武器池':-^80}")
            print("未进行抽卡")
        
        print("=" * 80)
    
    def get_pool_config(self, pool_type: str) -> Dict:
        """
        获取指定池子的配置
        
        Args:
            pool_type: 池子类型，'character' 或 'weapon'
        
        Returns:
            Dict: 池子配置
        """
        if pool_type == 'character':
            return copy.deepcopy(self.character_config)
        elif pool_type == 'weapon':
            return copy.deepcopy(self.weapon_config)
        else:
            raise ValueError(f"无效的池子类型: {pool_type}")
    
    def get_pool(self, pool_type: str) -> AdvancedGachaSimulator:
        """
        获取指定池子对象（直接访问）
        
        Args:
            pool_type: 池子类型，'character' 或 'weapon'
        
        Returns:
            AdvancedGachaSimulator: 池子对象
        """
        if pool_type == 'character':
            if not self.enable_character_pool:
                raise ValueError("角色池未启用")
            return self.character_pool
        elif pool_type == 'weapon':
            if not self.enable_weapon_pool:
                raise ValueError("武器池未启用")
            return self.weapon_pool
        else:
            raise ValueError(f"无效的池子类型: {pool_type}")
    
    def __repr__(self):
        char_status = "启用" if self.enable_character_pool else "禁用"
        weapon_status = "启用" if self.enable_weapon_pool else "禁用"
        return (f"GachaEnvironment(角色池={char_status}, 武器池={weapon_status}, "
                f"总抽数={self.total_draws}, 总回报={self.total_rewards})")


# ==================== 使用示例 ====================

if __name__ == '__main__':
    print("=" * 80)
    print("双池抽卡环境 - 演示".center(80))
    print("=" * 80)
    
    # 创建环境
    env = GachaEnvironment()
    print(f"\n环境创建成功: {env}")
    
    # 获取初始状态
    state = env.get_state()
    print(f"\n初始状态:")
    print(f"  角色池启用: {state['character_pool']['enabled']}")
    print(f"  武器池启用: {state['weapon_pool']['enabled']}")
    
    # 在角色池中抽10次
    print(f"\n{'角色池 - 10连抽':-^80}")
    results, state = env.multi_draw('character', 10)
    print(f"抽卡结果: {[str(r) for r in results]}")
    print(f"角色池保底状态: 距上次5-star={state['character_pool']['pity_info']['draws_since_top_rarity']}")
    
    # 在武器池中抽10次
    print(f"\n{'武器池 - 10连抽':-^80}")
    results, state = env.multi_draw('weapon', 10)
    print(f"抽卡结果: {[str(r) for r in results]}")
    print(f"武器池保底状态: 距上次5-star={state['weapon_pool']['pity_info']['draws_since_top_rarity']}")
    
    # 进行大量模拟
    print(f"\n{'大规模模拟测试':-^80}")
    print("角色池模拟10万抽...")
    env.multi_draw('character', 100000)
    
    print("武器池模拟10万抽...")
    env.multi_draw('weapon', 100000)
    
    # 显示详细统计
    print()
    env.display_statistics()
    
    # 获取统计数据
    stats = env.get_statistics()
    
    # 角色池理论值 vs 实际值
    if stats['character_pool']['enabled']:
        char_theoretical = stats['character_pool']['theoretical']
        char_empirical = env.character_pool.calculate_empirical_stats()
        
        print(f"\n{'角色池 - 理论值 vs 实际值':-^80}")
        print(f"期望抽数: 理论={char_theoretical['expected_draws_for_up']:.2f}, "
              f"实际={char_empirical['expected_draws_for_up']:.2f}")
        print(f"期望回报: 理论={char_theoretical['expected_total_reward']:.2f}, "
              f"实际={char_empirical['expected_total_reward']:.2f}")
    
    # 武器池理论值 vs 实际值
    if stats['weapon_pool']['enabled']:
        weapon_theoretical = stats['weapon_pool']['theoretical']
        weapon_empirical = env.weapon_pool.calculate_empirical_stats()
        
        print(f"\n{'武器池 - 理论值 vs 实际值':-^80}")
        print(f"期望抽数: 理论={weapon_theoretical['expected_draws_for_up']:.2f}, "
              f"实际={weapon_empirical['expected_draws_for_up']:.2f}")
        print(f"期望回报: 理论={weapon_theoretical['expected_total_reward']:.2f}, "
              f"实际={weapon_empirical['expected_total_reward']:.2f}")
    
    print("\n" + "=" * 80)
    print("演示完成！".center(80))
    print("=" * 80)
