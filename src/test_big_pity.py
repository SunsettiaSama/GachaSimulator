# -*- coding: utf-8 -*-
"""
测试武器池大小保底机制
"""
import sys
# 清除缓存
for mod in list(sys.modules.keys()):
    if mod.startswith('gacha_simulator'):
        del sys.modules[mod]

from gacha_simulator import WeaponPool
import random

print('=== Testing Weapon Pool Big/Small Pity (pity_enabled=False) ===')
print()

weapon_pool = WeaponPool()
print(f'Weapon pool config:')
print(f'  pity_enabled: {weapon_pool.pity_enabled}')
print(f'  hard_pity: {weapon_pool.hard_pity}')
print(f'  big_pity: {weapon_pool.big_pity}')
print(f'  rate_up_prob: {weapon_pool.rate_up_prob} (25%)')
print()

# 测试1：小保底（硬保底）
print('Test 1: Hard pity at draw 80')
weapon_pool.draws_since_top_rarity = 79
current_probs = weapon_pool._calculate_current_probabilities()
print(f'  6-star prob at draw 80: {current_probs["6-star"]*100:.0f}%')
result = weapon_pool.single_draw()
print(f'  Result: {result}')
print(f'  Is 6-star: {result.is_top_rarity}')
print()

# 测试2：大保底（80抽必出UP）
print('Test 2: Big pity - guarantee rate-up')
weapon_pool2 = WeaponPool()
# 模拟歪了一次
weapon_pool2.is_guaranteed_rate_up = True
weapon_pool2.draws_since_top_rarity = 79
weapon_pool2.draws_since_rate_up = 79

print(f'  is_guaranteed_rate_up: {weapon_pool2.is_guaranteed_rate_up}')
print(f'  draws_since_rate_up: {weapon_pool2.draws_since_rate_up}')

result = weapon_pool2.single_draw()
print(f'  Result: {result}')
print(f'  Is 6-star: {result.is_top_rarity}')
print(f'  Is rate-up: {result.is_rate_up}')
print()

# 测试3：模拟多次抽卡，验证UP概率约为25%
print('Test 3: Rate-up probability (should be ~25%)')
weapon_pool3 = WeaponPool()
random.seed(12345)

up_count = 0
non_up_count = 0

# 模拟抽到100个6星
for i in range(10000):
    result = weapon_pool3.single_draw()
    if result.is_top_rarity:
        if result.is_rate_up:
            up_count += 1
        else:
            non_up_count += 1
        
        if up_count + non_up_count >= 100:
            break

total_6star = up_count + non_up_count
up_rate = up_count / total_6star if total_6star > 0 else 0

print(f'  Total 6-stars: {total_6star}')
print(f'  UP 6-stars: {up_count}')
print(f'  Non-UP 6-stars: {non_up_count}')
print(f'  UP rate: {up_rate*100:.1f}% (expected: 25%)')
print()

if 20 <= up_rate * 100 <= 30:
    print('Result: UP rate is close to 25% - PASS')
else:
    print('Result: UP rate deviates from 25% - may need more samples')
