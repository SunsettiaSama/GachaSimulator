# -*- coding: utf-8 -*-
import sys
for k in list(sys.modules.keys()):
    if k.startswith('gacha_simulator'):
        del sys.modules[k]

from gacha_simulator import WeaponPool
import random

print('='*70)
print('Large Sample Test - Weapon Pool')
print('='*70)

random.seed(12345)
wp = WeaponPool()

print('\nConfig:')
print(f'  rate_up_prob: {wp.rate_up_prob} (25%)')
print(f'  guarantee_enabled: {wp.guarantee_enabled}')
print(f'  pity_enabled: {wp.pity_enabled}')
print()

# Draw until we get 1000 6-stars
print('Drawing until 1000 6-stars...')
for _ in range(100000):
    wp.single_draw()
    stats = wp.get_statistics()
    if stats['top_rarity_stats']['total'] >= 1000:
        break

print('\nResults:')
print(f"Total draws: {stats['total_draws']}")
print(f"Total 6-stars: {stats['top_rarity_stats']['total']}")
print(f"UP 6-stars: {stats['top_rarity_stats']['rate_up']}")
print(f"Non-UP 6-stars: {stats['top_rarity_stats']['non_rate_up']}")
print(f"UP rate: {stats['top_rarity_stats']['rate_up_ratio']*100:.2f}%")
print()

# Theoretical calculation
# With 25% base UP rate and guarantee mechanism:
# Expected pattern: 25% direct UP, 75% miss then guaranteed UP
# Average 6-stars per UP: 0.25*1 + 0.75*2 = 1.75
# UP rate: 1/1.75 = 57.14%
theoretical_up_rate = 1 / (1 + (1 - wp.rate_up_prob))
print(f'Theoretical UP rate: {theoretical_up_rate*100:.2f}%')
print()

if abs(stats['top_rarity_stats']['rate_up_ratio'] - theoretical_up_rate) < 0.05:
    print('PASS: UP rate matches theoretical expectation!')
else:
    print('WARNING: UP rate deviates from theory')
