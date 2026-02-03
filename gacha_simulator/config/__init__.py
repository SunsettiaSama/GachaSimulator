# -*- coding: utf-8 -*-
"""
配置模块
包含所有抽卡池配置
"""

from .gacha_simulator_config import (
    CHARACTER_POOL_CONFIG,
    WEAPON_POOL_CONFIG,
    LIMITED_CHARACTER_CONFIG,
    STANDARD_POOL_CONFIG,
    NOVICE_POOL_CONFIG,
    PoolConfigManager
)

__all__ = [
    'CHARACTER_POOL_CONFIG',
    'WEAPON_POOL_CONFIG',
    'LIMITED_CHARACTER_CONFIG',
    'STANDARD_POOL_CONFIG',
    'NOVICE_POOL_CONFIG',
    'PoolConfigManager',
]
