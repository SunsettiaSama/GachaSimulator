# -*- coding: utf-8 -*-
"""
灵活配置示例
展示如何自定义稀有度名称、概率和回报
"""

# 示例1: 默认配置（标准SSR/SR/R/N系统）
DEFAULT_CONFIG = {
    'base_probabilities': {
        'SSR': 0.006,
        'SR': 0.051,
        'R': 0.300,
        'N': 0.643
    },
    'pity_enabled': True,
    'pity_threshold': 73,
    'pity_increment': 0.06,
    'hard_pity': 90,
    'reward_enabled': True,
    'rewards': {
        'SSR': 2000,
        'SR': 200,
        'R': 50,
        'N': 20
    },
    'guarantee_enabled': True,
    'rate_up_rarity': 'SSR',  # 指定SSR需要UP
    'rate_up_prob': 0.5,
    'big_pity': 180,
}

# 示例2: 6-star系统（三档稀有度）
SIX_STAR_CONFIG = {
    'base_probabilities': {
        '6-star': 0.006,
        '5-star': 0.051,
        '4-star': 0.943
    },
    'pity_enabled': True,
    'pity_threshold': 73,
    'pity_increment': 0.06,
    'hard_pity': 90,
    'reward_enabled': True,
    'rewards': {
        '6-star': 2000,
        '5-star': 200,
        '4-star': 50
    },
    'guarantee_enabled': True,
    'rate_up_rarity': '6-star',  # 指定6-star需要UP
    'rate_up_prob': 0.5,
    'big_pity': 180,
}

# 示例3: UR系统（四档稀有度，概率不同）
UR_CONFIG = {
    'base_probabilities': {
        'UR': 0.01,
        'SSR': 0.05,
        'SR': 0.20,
        'R': 0.74
    },
    'pity_enabled': True,
    'pity_threshold': 50,
    'pity_increment': 0.05,
    'hard_pity': 80,
    'reward_enabled': True,
    'rewards': {
        'UR': 5000,
        'SSR': 1000,
        'SR': 100,
        'R': 10
    },
    'guarantee_enabled': True,
    'rate_up_rarity': 'UR',  # 指定UR需要UP
    'rate_up_prob': 0.5,
    'big_pity': 160,
}

# 示例4: 简化系统（仅两档稀有度，无大小保底）
SIMPLE_CONFIG = {
    'base_probabilities': {
        'Legendary': 0.02,
        'Common': 0.98
    },
    'pity_enabled': True,
    'pity_threshold': 30,
    'pity_increment': 0.05,
    'hard_pity': 50,
    'reward_enabled': True,
    'rewards': {
        'Legendary': 1000,
        'Common': 10
    },
    'guarantee_enabled': False,  # 不启用大小保底
    'rate_up_rarity': 'Legendary',
}

# 示例5: 五档稀有度系统
FIVE_TIER_CONFIG = {
    'base_probabilities': {
        'Mythic': 0.002,
        'Legendary': 0.008,
        'Epic': 0.050,
        'Rare': 0.300,
        'Common': 0.640
    },
    'pity_enabled': True,
    'pity_threshold': 80,
    'pity_increment': 0.06,
    'hard_pity': 100,
    'reward_enabled': True,
    'rewards': {
        'Mythic': 10000,
        'Legendary': 2000,
        'Epic': 200,
        'Rare': 50,
        'Common': 10
    },
    'guarantee_enabled': True,
    'rate_up_rarity': 'Mythic',  # 指定Mythic需要UP
    'rate_up_prob': 0.5,
    'big_pity': 200,
}

# 配置要求说明：
"""
1. base_probabilities 键必须唯一，概率之和必须为1
2. rewards 的键必须和 base_probabilities 的键完全一致
3. rate_up_rarity 必须在 base_probabilities 中存在
4. 如果未指定 rate_up_rarity，系统会自动选择概率最低的稀有度
"""

# 使用示例：
if __name__ == "__main__":
    from advanced_gacha import AdvancedGachaSimulator
    
    # 使用6-star配置
    gacha = AdvancedGachaSimulator(SIX_STAR_CONFIG)
    
    print(f"当前配置: 6-star系统")
    print(f"最高稀有度: {gacha.rate_up_rarity}")
    print(f"稀有度列表: {list(gacha.base_probabilities.keys())}")
    
    # 进行测试抽卡
    gacha.multi_draw(100)
    gacha.display_statistics()
