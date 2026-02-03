# -*- coding: utf-8 -*-
"""
抽卡池配置文件
包含角色池和武器池的默认配置
"""

# ==================== 角色池配置 ====================
CHARACTER_POOL_CONFIG = {
    'name': '角色祈愿',
    'description': '概率UP！限定六星角色',
    
    # 基础概率设置
    'base_probabilities': {
        '6-star': 0.008,   # 0.8% 基础六星概率
        '5-star': 0.080,   # 8.0% 五星概率
        '4-star': 0.912,   # 91.2% 四星概率
    },
    
    # 线性保底机制
    'pity_enabled': True,
    'pity_threshold': 73,      # 73抽后开始增加概率
    'pity_increment': 0.06,    # 每抽增加6%概率
    'hard_pity': 90,           # 90抽必出六星（硬保底）
    
    # 回报机制
    'reward_enabled': True,
    'rewards': {
        '6-star': 3000,   # 六星角色回报3000
        '5-star': 300,    # 五星角色回报300
        '4-star': 30,     # 四星武器回报30
    },
    
    # 大小保底机制
    'guarantee_enabled': True,
    'rate_up_rarity': '6-star',    # 指定六星需要UP
    'rate_up_prob': 0.5,           # 50%是UP角色
    'big_pity': 180,               # 180抽必出UP角色（大保底）
}


# ==================== 武器池配置 ====================
WEAPON_POOL_CONFIG = {
    'name': '神铸赋形',
    'description': '概率UP！限定六星武器',
    
    # 基础概率设置
    'base_probabilities': {
        '6-star': 0.04,   # 4.0% 基础六星概率（武器池概率略高）
        '5-star': 0.15,   # 15.0% 五星概率
        '4-star': 0.81,   # 81.0% 四星概率
    },
    
    # 取消线性保底机制，改为独立同分布抽取
    'pity_enabled': False,
    'pity_threshold': 62,      # 不使用
    'pity_increment': 0.07,    # 不使用
    'hard_pity': 80,           # 80抽必出六星（硬保底）
    
    # 回报机制
    'reward_enabled': True,
    'rewards': {
        '6-star': 2500,   # 六星武器回报2500（比角色略低）
        '5-star': 250,    # 五星武器回报250
        '4-star': 25,     # 四星武器回报25
    },
    
    # 大小保底机制（命定值机制）
    'guarantee_enabled': True,
    'rate_up_rarity': '6-star',    # 指定六星需要UP
    'rate_up_prob': 0.25,          # 25%是UP武器
    'big_pity': 80,                # 80抽必出UP武器（命定值）
}


# ==================== 限定角色池配置示例 ====================
LIMITED_CHARACTER_CONFIG = {
    'name': '限定角色祈愿',
    'description': '超稀有！限定六星角色概率UP',
    
    'base_probabilities': {
        '6-star': 0.008,
        '5-star': 0.080,
        '4-star': 0.912,
    },
    
    'pity_enabled': True,
    'pity_threshold': 73,
    'pity_increment': 0.06,
    'hard_pity': 90,
    
    'reward_enabled': True,
    'rewards': {
        '6-star': 5000,   # 限定角色回报更高
        '5-star': 300,
        '4-star': 30,
    },
    
    'guarantee_enabled': True,
    'rate_up_rarity': '6-star',
    'rate_up_prob': 0.5,
    'big_pity': 180,
}


# ==================== 常驻池配置示例 ====================
STANDARD_POOL_CONFIG = {
    'name': '常驻祈愿',
    'description': '常驻角色和武器',
    
    'base_probabilities': {
        '6-star': 0.008,
        '5-star': 0.080,
        '4-star': 0.912,
    },
    
    'pity_enabled': True,
    'pity_threshold': 73,
    'pity_increment': 0.06,
    'hard_pity': 90,
    
    'reward_enabled': True,
    'rewards': {
        '6-star': 2000,   # 常驻六星回报较低
        '5-star': 200,
        '4-star': 20,
    },
    
    # 常驻池无大小保底
    'guarantee_enabled': False,
    'rate_up_rarity': '6-star',
    'rate_up_prob': 1.0,      # 无UP机制
    'big_pity': 90,
}


# ==================== 新手池配置示例 ====================
NOVICE_POOL_CONFIG = {
    'name': '新手祈愿',
    'description': '新手专属，20抽必出六星角色！',
    
    'base_probabilities': {
        '6-star': 0.008,
        '5-star': 0.080,
        '4-star': 0.912,
    },
    
    'pity_enabled': True,
    'pity_threshold': 10,      # 10抽后开始增加概率
    'pity_increment': 0.10,    # 增长更快
    'hard_pity': 20,           # 20抽必出（新手福利）
    
    'reward_enabled': True,
    'rewards': {
        '6-star': 3000,
        '5-star': 300,
        '4-star': 30,
    },
    
    'guarantee_enabled': False,
    'rate_up_rarity': '6-star',
    'rate_up_prob': 1.0,
    'big_pity': 20,
}


# ==================== 配置管理器 ====================
class PoolConfigManager:
    """池子配置管理器"""
    
    CONFIGS = {
        'character': CHARACTER_POOL_CONFIG,
        'weapon': WEAPON_POOL_CONFIG,
        'limited_character': LIMITED_CHARACTER_CONFIG,
        'standard': STANDARD_POOL_CONFIG,
        'novice': NOVICE_POOL_CONFIG,
    }
    
    @classmethod
    def get_config(cls, pool_type: str) -> dict:
        """
        获取指定类型的池子配置
        
        Args:
            pool_type: 池子类型 ('character', 'weapon', 'limited_character', 'standard', 'novice')
        
        Returns:
            dict: 配置字典
        """
        if pool_type not in cls.CONFIGS:
            raise ValueError(f"未知的池子类型: {pool_type}，可用类型: {list(cls.CONFIGS.keys())}")
        return cls.CONFIGS[pool_type].copy()
    
    @classmethod
    def list_pools(cls):
        """列出所有可用的池子类型"""
        print("可用的池子类型：")
        for pool_type, config in cls.CONFIGS.items():
            print(f"  - {pool_type}: {config['name']} - {config['description']}")
    
    @classmethod
    def add_custom_config(cls, pool_type: str, config: dict):
        """
        添加自定义配置
        
        Args:
            pool_type: 池子类型名称
            config: 配置字典
        """
        cls.CONFIGS[pool_type] = config
        print(f"已添加自定义配置: {pool_type}")


# ==================== 使用示例 ====================
if __name__ == '__main__':
    print("=" * 70)
    print("抽卡池配置管理器".center(70))
    print("=" * 70)
    
    # 列出所有池子
    PoolConfigManager.list_pools()
    
    # 获取角色池配置
    print(f"\n{'角色池配置':-^70}")
    char_config = PoolConfigManager.get_config('character')
    print(f"池子名称: {char_config['name']}")
    print(f"描述: {char_config['description']}")
    print(f"六星概率: {char_config['base_probabilities']['6-star']*100:.2f}%")
    print(f"硬保底: {char_config['hard_pity']} 抽")
    print(f"大保底: {char_config['big_pity']} 抽")
    
    # 获取武器池配置
    print(f"\n{'武器池配置':-^70}")
    weapon_config = PoolConfigManager.get_config('weapon')
    print(f"池子名称: {weapon_config['name']}")
    print(f"描述: {weapon_config['description']}")
    print(f"六星概率: {weapon_config['base_probabilities']['6-star']*100:.2f}%")
    print(f"硬保底: {weapon_config['hard_pity']} 抽")
    print(f"大保底: {weapon_config['big_pity']} 抽")
    print(f"UP概率: {weapon_config['rate_up_prob']*100:.1f}%")
    print(f"线性保底: {'已禁用' if not weapon_config['pity_enabled'] else '已启用'}")
    
    print("\n" + "=" * 70)
