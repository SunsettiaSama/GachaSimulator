# -*- coding: utf-8 -*-
"""
GachaSimulator - 高级抽卡模拟器包
包含角色池、武器池及配置管理
"""

from .base import AdvancedGachaSimulator, GachaResult
from .character import (
    CharacterPool, 
    create_standard_character_pool,
    create_limited_character_pool,
    create_novice_character_pool
)
from .weapon import (
    WeaponPool,
    create_standard_weapon_pool,
    create_custom_weapon_pool
)
from .config import (
    CHARACTER_POOL_CONFIG,
    WEAPON_POOL_CONFIG,
    LIMITED_CHARACTER_CONFIG,
    STANDARD_POOL_CONFIG,
    NOVICE_POOL_CONFIG,
    PoolConfigManager
)

__version__ = '1.0.0'
__author__ = 'GachaSimulator Team'

__all__ = [
    # 基础类
    'AdvancedGachaSimulator',
    'GachaResult',
    
    # 角色池
    'CharacterPool',
    'create_standard_character_pool',
    'create_limited_character_pool',
    'create_novice_character_pool',
    
    # 武器池
    'WeaponPool',
    'create_standard_weapon_pool',
    'create_custom_weapon_pool',
    
    # 配置
    'CHARACTER_POOL_CONFIG',
    'WEAPON_POOL_CONFIG',
    'LIMITED_CHARACTER_CONFIG',
    'STANDARD_POOL_CONFIG',
    'NOVICE_POOL_CONFIG',
    'PoolConfigManager',
]
