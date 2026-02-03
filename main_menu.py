# -*- coding: utf-8 -*-
"""
抽卡模拟器 - 主菜单
提供交互式命令行界面
"""

import sys
from typing import Optional
from gacha_simulator import (
    CharacterPool,
    WeaponPool,
    create_standard_character_pool,
    create_limited_character_pool,
    create_novice_character_pool,
    create_standard_weapon_pool,
    PoolConfigManager
)


class GachaMenu:
    """抽卡模拟器主菜单类"""
    
    def __init__(self):
        self.character_pool: Optional[CharacterPool] = None
        self.weapon_pool: Optional[WeaponPool] = None
        self.current_pool = None
        self.current_pool_type = None
        self.running = True
    
    def clear_screen(self):
        """清屏（跨平台）"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        """显示横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    🎲 抽卡模拟器 v1.0 🎲                         ║
║                                                                  ║
║                  体验真实的抽卡概率与保底机制                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_main_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 70)
        print("主菜单".center(70))
        print("=" * 70)
        print("\n【池子管理】")
        print("  1. 创建角色池")
        print("  2. 创建武器池")
        print("  3. 切换当前池子")
        print("  4. 查看当前池子信息")
        print("\n【抽卡操作】")
        print("  5. 单抽 (1 抽)")
        print("  6. 十连 (10 抽)")
        print("  7. 自定义抽数")
        print("  8. 大量模拟 (10万抽)")
        print("\n【统计分析】")
        print("  9. 查看当前统计")
        print("  10. 查看理论统计")
        print("  11. 理论 vs 实际对比")
        print("  12. 重置当前池子")
        print("\n【其他】")
        print("  13. 查看所有可用池子配置")
        print("  0. 退出")
        print("\n" + "=" * 70)
    
    def create_character_pool_menu(self):
        """创建角色池子菜单"""
        print("\n" + "=" * 70)
        print("创建角色池".center(70))
        print("=" * 70)
        print("\n请选择角色池类型：")
        print("  1. 标准角色池 (90抽硬保底, 180抽大保底)")
        print("  2. 限定角色池 (高回报)")
        print("  3. 新手角色池 (20抽必出)")
        print("  0. 返回")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == '1':
            self.character_pool = create_standard_character_pool()
            print("\n✓ 已创建标准角色池")
            self.character_pool.display_pool_info()
            self.current_pool = self.character_pool
            self.current_pool_type = '角色池'
        elif choice == '2':
            self.character_pool = create_limited_character_pool()
            print("\n✓ 已创建限定角色池")
            self.character_pool.display_pool_info()
            self.current_pool = self.character_pool
            self.current_pool_type = '角色池'
        elif choice == '3':
            self.character_pool = create_novice_character_pool()
            print("\n✓ 已创建新手角色池")
            self.character_pool.display_pool_info()
            self.current_pool = self.character_pool
            self.current_pool_type = '角色池'
        elif choice == '0':
            return
        else:
            print("\n✗ 无效选项")
        
        input("\n按 Enter 继续...")
    
    def create_weapon_pool_menu(self):
        """创建武器池子菜单"""
        print("\n" + "=" * 70)
        print("创建武器池".center(70))
        print("=" * 70)
        print("\n请选择武器池类型：")
        print("  1. 标准武器池 (80抽硬保底, 160抽大保底, 命定值机制)")
        print("  0. 返回")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == '1':
            self.weapon_pool = create_standard_weapon_pool()
            print("\n✓ 已创建标准武器池")
            self.weapon_pool.display_pool_info()
            self.current_pool = self.weapon_pool
            self.current_pool_type = '武器池'
        elif choice == '0':
            return
        else:
            print("\n✗ 无效选项")
        
        input("\n按 Enter 继续...")
    
    def switch_pool_menu(self):
        """切换池子菜单"""
        print("\n" + "=" * 70)
        print("切换池子".center(70))
        print("=" * 70)
        
        available_pools = []
        if self.character_pool:
            available_pools.append(('1', '角色池', self.character_pool))
        if self.weapon_pool:
            available_pools.append(('2', '武器池', self.weapon_pool))
        
        if not available_pools:
            print("\n✗ 尚未创建任何池子，请先创建")
            input("\n按 Enter 继续...")
            return
        
        print("\n可用的池子：")
        for idx, name, pool in available_pools:
            status = " (当前)" if pool == self.current_pool else ""
            print(f"  {idx}. {name}{status}")
        print("  0. 返回")
        
        choice = input("\n请输入选项: ").strip()
        
        for idx, name, pool in available_pools:
            if choice == idx:
                self.current_pool = pool
                self.current_pool_type = name
                print(f"\n✓ 已切换到 {name}")
                input("\n按 Enter 继续...")
                return
        
        if choice != '0':
            print("\n✗ 无效选项")
            input("\n按 Enter 继续...")
    
    def check_current_pool(self) -> bool:
        """检查是否选择了池子"""
        if self.current_pool is None:
            print("\n✗ 请先创建并选择一个池子")
            input("\n按 Enter 继续...")
            return False
        return True
    
    def single_draw(self):
        """单抽"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'单抽':-^70}")
        result = self.current_pool.single_draw()
        print(f"抽卡结果: {result}")
        print(f"回报: {result.reward}")
        
        stats = self.current_pool.get_statistics()
        print(f"\n保底状态:")
        print(f"  距上次五星: {stats['pity_info']['draws_since_top_rarity']}")
        print(f"  是否保底UP: {'是' if stats['pity_info']['is_guaranteed_rate_up'] else '否'}")
        
        if self.current_pool_type == '武器池' and hasattr(self.current_pool, 'fate_points'):
            print(f"  命定值: {self.current_pool.fate_points}/2")
        
        input("\n按 Enter 继续...")
    
    def multi_draw_10(self):
        """十连"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'十连抽':-^70}")
        results = self.current_pool.multi_draw(10)
        
        print(f"抽卡结果:")
        for i, result in enumerate(results, 1):
            print(f"  第 {i} 抽: {result} (回报: {result.reward})")
        
        # 统计五星
        five_star_count = sum(1 for r in results if r.is_top_rarity)
        if five_star_count > 0:
            print(f"\n🎉 本次十连抽到 {five_star_count} 个五星！")
        
        stats = self.current_pool.get_statistics()
        print(f"\n保底状态:")
        print(f"  距上次五星: {stats['pity_info']['draws_since_top_rarity']}")
        print(f"  是否保底UP: {'是' if stats['pity_info']['is_guaranteed_rate_up'] else '否'}")
        
        if self.current_pool_type == '武器池' and hasattr(self.current_pool, 'fate_points'):
            print(f"  命定值: {self.current_pool.fate_points}/2")
        
        input("\n按 Enter 继续...")
    
    def custom_draw(self):
        """自定义抽数"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'自定义抽数':-^70}")
        try:
            count = int(input("请输入抽卡次数: "))
            if count <= 0:
                print("\n✗ 抽卡次数必须大于0")
                input("\n按 Enter 继续...")
                return
            
            print(f"\n正在进行 {count} 次抽卡...")
            results = self.current_pool.multi_draw(count)
            
            # 统计
            five_star_count = sum(1 for r in results if r.is_top_rarity)
            up_count = sum(1 for r in results if r.is_top_rarity and r.is_rate_up)
            
            print(f"\n抽卡完成！")
            print(f"  总抽数: {count}")
            print(f"  五星总数: {five_star_count}")
            print(f"  UP五星: {up_count}")
            
            if five_star_count > 0:
                print(f"  UP率: {up_count/five_star_count*100:.2f}%")
            
        except ValueError:
            print("\n✗ 请输入有效的数字")
        
        input("\n按 Enter 继续...")
    
    def large_simulation(self):
        """大量模拟"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'大量模拟 (10万抽)':-^70}")
        confirm = input("这将进行10万次抽卡模拟，继续吗? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\n已取消")
            input("\n按 Enter 继续...")
            return
        
        print("\n正在模拟...")
        self.current_pool.multi_draw(100000)
        print("\n✓ 模拟完成！")
        
        self.current_pool.display_statistics()
        
        input("\n按 Enter 继续...")
    
    def view_statistics(self):
        """查看当前统计"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'当前统计':-^70}")
        self.current_pool.display_statistics()
        
        input("\n按 Enter 继续...")
    
    def view_theoretical_stats(self):
        """查看理论统计"""
        if not self.check_current_pool():
            return
        
        print(f"\n{'理论统计':-^70}")
        theoretical = self.current_pool.calculate_theoretical_stats()
        
        print(f"期望抽数 (抽到UP五星): {theoretical['expected_draws_for_up']:.2f}")
        print(f"抽数标准差: {theoretical['std_draws']:.2f}")
        print(f"单抽期望回报: {theoretical['expected_reward_per_draw']:.2f}")
        print(f"总期望回报: {theoretical['expected_total_reward']:.2f}")
        print(f"回报标准差: {theoretical['std_total_reward']:.2f}")
        
        input("\n按 Enter 继续...")
    
    def compare_stats(self):
        """理论 vs 实际对比"""
        if not self.check_current_pool():
            return
        
        stats = self.current_pool.get_statistics()
        if stats['total_draws'] == 0:
            print("\n✗ 尚未进行抽卡，无法对比")
            input("\n按 Enter 继续...")
            return
        
        print(f"\n{'理论 vs 实际对比':-^70}")
        
        theoretical = self.current_pool.calculate_theoretical_stats()
        empirical = self.current_pool.calculate_empirical_stats()
        
        if empirical['sample_size'] == 0:
            print("\n✗ 样本数不足（未抽到UP五星），无法计算实际统计")
            input("\n按 Enter 继续...")
            return
        
        print(f"\n样本数: {empirical['sample_size']} 个UP五星\n")
        
        print(f"{'指标':<20} {'理论值':>15} {'实际值':>15} {'偏差':>15}")
        print("-" * 70)
        
        draws_diff = abs(theoretical['expected_draws_for_up'] - empirical['expected_draws_for_up']) / theoretical['expected_draws_for_up'] * 100
        print(f"{'期望抽数':<20} {theoretical['expected_draws_for_up']:>15.2f} {empirical['expected_draws_for_up']:>15.2f} {draws_diff:>14.2f}%")
        
        std_diff = abs(theoretical['std_draws'] - empirical['std_draws']) / theoretical['std_draws'] * 100
        print(f"{'抽数标准差':<20} {theoretical['std_draws']:>15.2f} {empirical['std_draws']:>15.2f} {std_diff:>14.2f}%")
        
        reward_diff = abs(theoretical['expected_total_reward'] - empirical['expected_total_reward']) / theoretical['expected_total_reward'] * 100
        print(f"{'期望回报':<20} {theoretical['expected_total_reward']:>15.2f} {empirical['expected_total_reward']:>15.2f} {reward_diff:>14.2f}%")
        
        reward_std_diff = abs(theoretical['std_total_reward'] - empirical['std_total_reward']) / theoretical['std_total_reward'] * 100
        print(f"{'回报标准差':<20} {theoretical['std_total_reward']:>15.2f} {empirical['std_total_reward']:>15.2f} {reward_std_diff:>14.2f}%")
        
        print("\n" + "=" * 70)
        
        input("\n按 Enter 继续...")
    
    def reset_pool(self):
        """重置当前池子"""
        if not self.check_current_pool():
            return
        
        confirm = input("\n确认重置当前池子的所有统计数据吗? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self.current_pool.reset_statistics()
            print("\n✓ 池子已重置")
        else:
            print("\n已取消")
        
        input("\n按 Enter 继续...")
    
    def view_all_configs(self):
        """查看所有配置"""
        print(f"\n{'所有可用池子配置':-^70}")
        PoolConfigManager.list_pools()
        input("\n按 Enter 继续...")
    
    def run(self):
        """运行主菜单"""
        self.clear_screen()
        self.display_banner()
        
        while self.running:
            self.display_main_menu()
            
            if self.current_pool:
                print(f"\n当前选择: {self.current_pool_type} | 总抽数: {self.current_pool.total_draws}")
            else:
                print(f"\n当前选择: 无 (请先创建池子)")
            
            choice = input("\n请输入选项: ").strip()
            
            if choice == '1':
                self.create_character_pool_menu()
            elif choice == '2':
                self.create_weapon_pool_menu()
            elif choice == '3':
                self.switch_pool_menu()
            elif choice == '4':
                if self.check_current_pool():
                    self.current_pool.display_pool_info()
                    input("\n按 Enter 继续...")
            elif choice == '5':
                self.single_draw()
            elif choice == '6':
                self.multi_draw_10()
            elif choice == '7':
                self.custom_draw()
            elif choice == '8':
                self.large_simulation()
            elif choice == '9':
                self.view_statistics()
            elif choice == '10':
                self.view_theoretical_stats()
            elif choice == '11':
                self.compare_stats()
            elif choice == '12':
                self.reset_pool()
            elif choice == '13':
                self.view_all_configs()
            elif choice == '0':
                print("\n感谢使用！再见！")
                self.running = False
            else:
                print("\n✗ 无效选项")
                input("\n按 Enter 继续...")


# ==================== 主程序 ====================
if __name__ == '__main__':
    try:
        menu = GachaMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n程序已中断，再见！")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
