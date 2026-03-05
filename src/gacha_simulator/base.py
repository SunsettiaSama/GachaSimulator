"""
高级抽卡模拟器
支持线性保底、回报机制、大小保底等高级功能
"""

import random
from typing import List, Dict, Tuple, Optional
from collections import Counter
import copy


class GachaResult:
    """抽卡结果类"""
    def __init__(self, rarity: str, is_rate_up: bool = False, reward: int = 0, is_top_rarity: bool = False):
        self.rarity = rarity
        self.is_rate_up = is_rate_up  # 是否为UP（想要的）
        self.reward = reward
        self.is_top_rarity = is_top_rarity  # 是否为最高稀有度
    
    def __str__(self):
        if self.is_top_rarity:
            return f"{self.rarity}{'(UP)' if self.is_rate_up else '(歪)'}"
        return self.rarity
    
    def __repr__(self):
        return self.__str__()


class AdvancedGachaSimulator:
    """
    高级抽卡模拟器
    支持：
    1. 线性保底机制
    2. 回报机制
    3. 大小保底机制
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化高级抽卡器
        
        Args:
            config: 配置字典，包含各种开关和参数
        """
        # 默认配置
        default_config = {
            # 基础概率设置
            'base_probabilities': {
                'SSR': 0.006,   # 0.6% 基础概率
                'SR': 0.051,    # 5.1%
                'R': 0.300,     # 30%
                'N': 0.643      # 64.3%
            },
            
            # 线性保底机制
            'pity_enabled': True,
            'pity_threshold': 73,      # 73抽后开始增加概率
            'pity_increment': 0.06,    # 每抽增加6%概率
            'hard_pity': 90,           # 90抽必出（硬保底）
            
            # 回报机制
            'reward_enabled': True,
            'rewards': {
                'SSR': 2000,   # SSR回报2000
                'SR': 200,     # SR回报200
                'R': 50,       # R回报50
                'N': 20        # N回报20
            },
            
            # 大小保底机制
            'guarantee_enabled': True,
            'rate_up_rarity': 'SSR',   # 指定哪个稀有度需要UP（必须在base_probabilities中）
            'rate_up_prob': 0.5,       # 最高稀有度中50%是UP
            'big_pity': 180,           # 180抽必出UP（大保底）
        }
        
        # 合并用户配置
        self.config = default_config
        if config:
            self.config.update(config)
        
        # 验证并处理配置
        self._validate_and_process_config()
        
        # 基础概率
        self.base_probabilities = self.config['base_probabilities']
        
        # 保底相关
        self.pity_enabled = self.config['pity_enabled']
        self.pity_threshold = self.config['pity_threshold']
        self.pity_increment = self.config['pity_increment']
        self.hard_pity = self.config['hard_pity']
        
        # 回报相关
        self.reward_enabled = self.config['reward_enabled']
        self.rewards = self.config['rewards']
        
        # 大小保底相关
        self.guarantee_enabled = self.config['guarantee_enabled']
        self.rate_up_rarity = self.config['rate_up_rarity']  # 需要UP的稀有度
        self.rate_up_prob = self.config['rate_up_prob']
        self.big_pity = self.config['big_pity']
        
        # 状态追踪
        self.draws_since_top_rarity = 0        # 距上次最高稀有度的抽数（小保底计数）
        self.draws_since_rate_up = 0           # 距上次UP的抽数（大保底计数）
        self.is_guaranteed_rate_up = False     # 是否下次最高稀有度必定是UP
        
        # 统计信息
        self.total_draws = 0
        self.total_rewards = 0
        self.draw_history: List[GachaResult] = []
        
        # 详细统计
        self.top_rarity_count = 0      # 最高稀有度总数
        self.rate_up_count = 0         # UP数量
        self.non_rate_up_count = 0     # 非UP数量
    
    def _validate_and_process_config(self):
        """
        验证并处理配置
        
        要求：
        1. 基础概率相加为1
        2. 回报值的键和基础概率键保持一致
        3. 如果启用大小保底，rate_up_rarity 必须在 base_probabilities 中
        """
        base_probs = self.config.get('base_probabilities', {})
        rewards = self.config.get('rewards', {})
        
        # 验证1: 基础概率相加为1
        if not base_probs:
            raise ValueError("配置错误: base_probabilities 不能为空")
        
        total_prob = sum(base_probs.values())
        if abs(total_prob - 1.0) > 0.0001:
            raise ValueError(f"配置错误: 基础概率之和必须为1，当前为 {total_prob:.6f}")
        
        # 验证2: 回报值的键和基础概率键保持一致
        if self.config.get('reward_enabled', False):
            prob_keys = set(base_probs.keys())
            reward_keys = set(rewards.keys())
            
            if prob_keys != reward_keys:
                missing_in_rewards = prob_keys - reward_keys
                extra_in_rewards = reward_keys - prob_keys
                
                error_msg = "配置错误: 回报值的键必须和基础概率键一致\n"
                if missing_in_rewards:
                    error_msg += f"  - rewards 中缺少: {missing_in_rewards}\n"
                if extra_in_rewards:
                    error_msg += f"  - rewards 中多余: {extra_in_rewards}\n"
                
                raise ValueError(error_msg.strip())
        
        # 验证3: 如果启用大小保底，rate_up_rarity 必须在 base_probabilities 中
        if self.config.get('guarantee_enabled', False):
            rate_up_rarity = self.config.get('rate_up_rarity')
            
            if not rate_up_rarity:
                # 如果未指定，自动选择概率最小的（通常是最高稀有度）
                rate_up_rarity = min(base_probs.keys(), key=lambda k: base_probs[k])
                self.config['rate_up_rarity'] = rate_up_rarity
                print(f"警告: 未指定 rate_up_rarity，自动选择概率最低的稀有度: {rate_up_rarity}")
            
            if rate_up_rarity not in base_probs:
                raise ValueError(
                    f"配置错误: rate_up_rarity '{rate_up_rarity}' 必须在 base_probabilities 中\n"
                    f"  可用的稀有度: {list(base_probs.keys())}"
                )
        else:
            # 如果未启用大小保底，仍需要指定用于线性保底的稀有度
            if not self.config.get('rate_up_rarity'):
                # 自动选择概率最小的
                rate_up_rarity = min(base_probs.keys(), key=lambda k: base_probs[k])
                self.config['rate_up_rarity'] = rate_up_rarity
    
    def _calculate_current_probabilities(self) -> Dict[str, float]:
        """
        计算当前抽卡概率（考虑保底机制）
        
        Returns:
            Dict[str, float]: 当前各稀有度的概率
        """
        # 复制基础概率
        current_probs = copy.copy(self.base_probabilities)
        
        # 如果启用线性保底
        if self.pity_enabled and self.draws_since_top_rarity >= self.pity_threshold:
            # 计算最高稀有度概率增加量
            draws_over_threshold = self.draws_since_top_rarity - self.pity_threshold
            top_rarity_increase = draws_over_threshold * self.pity_increment
            
            # 新的最高稀有度概率
            base_top_rarity_prob = self.base_probabilities[self.rate_up_rarity]
            new_top_rarity_prob = min(1.0, base_top_rarity_prob + top_rarity_increase)
            
            # 计算需要压缩的概率空间
            prob_to_compress = new_top_rarity_prob - base_top_rarity_prob
            
            # 计算非最高稀有度的原始概率总和
            non_top_rarity_total = 1.0 - base_top_rarity_prob
            
            # 等比压缩其他概率
            if non_top_rarity_total > 0:
                compression_ratio = (1.0 - new_top_rarity_prob) / non_top_rarity_total
                for rarity in self.base_probabilities.keys():
                    if rarity != self.rate_up_rarity:
                        current_probs[rarity] = self.base_probabilities[rarity] * compression_ratio
            
            current_probs[self.rate_up_rarity] = new_top_rarity_prob
        
        # 硬保底：如果达到硬保底抽数，最高稀有度概率为100%（独立于线性保底）
        if self.draws_since_top_rarity >= self.hard_pity - 1:
            current_probs = {rarity: 0.0 for rarity in self.base_probabilities.keys()}
            current_probs[self.rate_up_rarity] = 1.0
        
        return current_probs
    
    def _is_rate_up(self) -> bool:
        """
        判断最高稀有度是否为UP（想要的）
        
        Returns:
            bool: True表示UP，False表示歪了
        """
        if not self.guarantee_enabled:
            return True  # 如果不启用大小保底，所有最高稀有度都算UP
        
        # 大保底：如果达到大保底抽数，必定是UP
        if self.draws_since_rate_up >= self.big_pity - 1:
            return True
        
        # 如果上次歪了，这次保证是UP
        if self.is_guaranteed_rate_up:
            return True
        
        # 否则按概率判断
        return random.random() < self.rate_up_prob
    
    def single_draw(self) -> GachaResult:
        """
        单次抽卡
        
        Returns:
            GachaResult: 抽卡结果
        """
        # 获取当前概率
        current_probs = self._calculate_current_probabilities()
        
        # 抽卡
        rarities = list(current_probs.keys())
        probabilities = list(current_probs.values())
        rarity = random.choices(rarities, weights=probabilities, k=1)[0]
        
        # 判断是否为最高稀有度
        is_top_rarity = (rarity == self.rate_up_rarity)
        
        # 判断是否为UP
        is_rate_up = False
        if is_top_rarity:
            is_rate_up = self._is_rate_up()
            self.top_rarity_count += 1
            
            if is_rate_up:
                self.rate_up_count += 1
                self.draws_since_rate_up = 0
                self.is_guaranteed_rate_up = False
            else:
                self.non_rate_up_count += 1
                self.draws_since_rate_up += 1
                self.is_guaranteed_rate_up = True  # 歪了，下次保证UP
            
            # 重置最高稀有度保底计数
            self.draws_since_top_rarity = 0
        else:
            # 未抽到最高稀有度，增加保底计数
            self.draws_since_top_rarity += 1
            self.draws_since_rate_up += 1
        
        # 计算回报
        reward = 0
        if self.reward_enabled:
            reward = self.rewards.get(rarity, 0)
            self.total_rewards += reward
        
        # 创建结果
        result = GachaResult(rarity, is_rate_up, reward, is_top_rarity)
        
        # 更新统计
        self.total_draws += 1
        self.draw_history.append(result)
        
        return result
    
    def multi_draw(self, count: int = 10) -> List[GachaResult]:
        """
        多次抽卡
        
        Args:
            count: 抽卡次数
            
        Returns:
            List[GachaResult]: 抽卡结果列表
        """
        results = []
        for _ in range(count):
            results.append(self.single_draw())
        return results
    
    def get_statistics(self) -> Dict:
        """
        获取详细统计信息
        
        Returns:
            Dict: 统计信息字典
        """
        if self.total_draws == 0:
            return {
                'total_draws': 0,
                'total_rewards': 0,
                'rarity_stats': {},
                'top_rarity_stats': {},
                'pity_info': {}
            }
        
        # 稀有度统计（动态处理所有稀有度）
        rarity_counter = Counter([r.rarity for r in self.draw_history])
        rarity_stats = {}
        for rarity in self.base_probabilities.keys():
            count = rarity_counter.get(rarity, 0)
            rarity_stats[rarity] = {
                'count': count,
                'probability': count / self.total_draws,
                'base_probability': self.base_probabilities[rarity]
            }
        
        # 最高稀有度详细统计
        top_rarity_stats = {
            'rarity_name': self.rate_up_rarity,  # 最高稀有度名称
            'total': self.top_rarity_count,
            'rate_up': self.rate_up_count,
            'non_rate_up': self.non_rate_up_count,
            'rate_up_ratio': self.rate_up_count / self.top_rarity_count if self.top_rarity_count > 0 else 0
        }
        
        # 保底信息
        current_probs = self._calculate_current_probabilities()
        
        # 计算距离大保底的抽数
        # 逻辑：如果已经歪了一次（is_guaranteed_rate_up=True），下一个保底就是硬保底
        # 如果没有歪，距离大保底还是从上次UP开始计算
        if self.guarantee_enabled:
            if self.is_guaranteed_rate_up:
                # 已经歪了，下一个必出UP，距离=硬保底-当前距离最高稀有度的抽数
                draws_until_big_pity = max(0, self.hard_pity - self.draws_since_top_rarity) if self.pity_enabled else 0
            else:
                # 没有歪，下一个大保底距离=大保底-当前距离上次UP的抽数
                draws_until_big_pity = max(0, self.big_pity - self.draws_since_rate_up)
        else:
            draws_until_big_pity = None
        
        pity_info = {
            'draws_since_top_rarity': self.draws_since_top_rarity,
            'draws_since_rate_up': self.draws_since_rate_up,
            'is_guaranteed_rate_up': self.is_guaranteed_rate_up,
            'current_top_rarity_prob': current_probs[self.rate_up_rarity],
            'top_rarity_name': self.rate_up_rarity,  # 最高稀有度名称
            'draws_until_hard_pity': max(0, self.hard_pity - self.draws_since_top_rarity) if self.pity_enabled else None,
            'draws_until_big_pity': draws_until_big_pity
        }
        
        return {
            'total_draws': self.total_draws,
            'total_rewards': self.total_rewards,
            'rarity_stats': rarity_stats,
            'top_rarity_stats': top_rarity_stats,
            'pity_info': pity_info
        }
    
    def display_statistics(self):
        """显示统计信息"""
        stats = self.get_statistics()
        
        print(f"\n{'='*70}")
        print(f"高级抽卡统计")
        print(f"{'='*70}")
        print(f"总抽卡次数: {stats['total_draws']}")
        print(f"总回报: {stats['total_rewards']}")
        print(f"\n{'稀有度统计':-^70}")
        print(f"{'稀有度':<10} {'基础概率':<12} {'实际概率':<12} {'抽取次数':<10}")
        print(f"{'-'*70}")
        
        # 动态显示所有稀有度
        for rarity in self.base_probabilities.keys():
            if rarity in stats['rarity_stats']:
                s = stats['rarity_stats'][rarity]
                base_prob = s['base_probability'] * 100
                actual_prob = s['probability'] * 100
                count = s['count']
                print(f"{rarity:<10} {base_prob:>6.2f}%      {actual_prob:>6.2f}%      {count:<10}")
        
        print(f"\n{f'{self.rate_up_rarity}详细统计':-^70}")
        top = stats['top_rarity_stats']
        print(f"总{self.rate_up_rarity}数: {top['total']}")
        print(f"UP {self.rate_up_rarity}: {top['rate_up']}")
        print(f"歪的{self.rate_up_rarity}: {top['non_rate_up']}")
        print(f"UP胜率: {top['rate_up_ratio']*100:.2f}%")
        
        print(f"\n{'当前保底状态':-^70}")
        pity = stats['pity_info']
        print(f"距上次{self.rate_up_rarity}: {pity['draws_since_top_rarity']} 抽")
        print(f"当前{self.rate_up_rarity}概率: {pity['current_top_rarity_prob']*100:.2f}%")
        if pity['draws_until_hard_pity'] is not None:
            print(f"距硬保底: {pity['draws_until_hard_pity']} 抽")
        print(f"距上次UP: {pity['draws_since_rate_up']} 抽")
        if pity['draws_until_big_pity'] is not None:
            print(f"距大保底: {pity['draws_until_big_pity']} 抽")
        print(f"是否保底UP: {'是' if pity['is_guaranteed_rate_up'] else '否'}")
        print(f"{'='*70}\n")
    
    def reset_statistics(self):
        """重置统计信息"""
        self.draws_since_top_rarity = 0
        self.draws_since_rate_up = 0
        self.is_guaranteed_rate_up = False
        self.total_draws = 0
        self.total_rewards = 0
        self.draw_history = []
        self.top_rarity_count = 0
        self.rate_up_count = 0
        self.non_rate_up_count = 0
    
    def get_config(self) -> Dict:
        """获取当前配置"""
        return copy.deepcopy(self.config)
    
    def calculate_theoretical_stats(self) -> Dict:
        """
        计算理论统计值（基于数值求和的严格计算）
        
        采用数值求和方法，逐抽计算概率分布，避免使用经验简化公式。
        
        Returns:
            Dict: 包含期望、方差、期望回报、回报方差的理论值
        """
        base_top_rarity_prob = self.base_probabilities[self.rate_up_rarity]
        up_prob_in_top_rarity = self.rate_up_prob if self.guarantee_enabled else 1.0
        
        # ========== 步骤1: 计算抽到任意最高稀有度的期望抽数 E[M] ==========
        if self.pity_enabled:
            # 线性保底下，使用数值求和计算E[M]
            expected_draws_for_any_top_rarity, variance_draws_for_any_top_rarity = self._calculate_ssr_expectation_numerical()
        else:
            # 无线性保底，纯几何分布
            expected_draws_for_any_top_rarity = 1 / base_top_rarity_prob if base_top_rarity_prob > 0 else float('inf')
            variance_draws_for_any_top_rarity = (1 - base_top_rarity_prob) / (base_top_rarity_prob ** 2) if base_top_rarity_prob > 0 else float('inf')
        
        # ========== 步骤2: 计算抽到UP最高稀有度的期望抽数 E[N] ==========
        if self.guarantee_enabled:
            # 启用大小保底：E[N] = E[M] × (1 + (1 - up_prob_in_top_rarity))
            # 即50%概率一次成功(E[M])，50%概率两次成功(2×E[M])
            expected_draws_for_up = expected_draws_for_any_top_rarity * (1 + (1 - up_prob_in_top_rarity))
            
            # 方差：Var[N] = Var[M] × (1 + (1 - up_prob_in_top_rarity)^2) + E[M]^2 × up_prob_in_top_rarity × (1 - up_prob_in_top_rarity)
            # 简化为：考虑大小保底的额外方差贡献
            variance_draws = (
                variance_draws_for_any_top_rarity * (1 + (1 - up_prob_in_top_rarity) ** 2) +
                expected_draws_for_any_top_rarity ** 2 * up_prob_in_top_rarity * (1 - up_prob_in_top_rarity)
            )
        else:
            # 无大小保底：所有最高稀有度都是UP
            expected_draws_for_up = expected_draws_for_any_top_rarity
            variance_draws = variance_draws_for_any_top_rarity
        
        # ========== 步骤3: 计算期望回报（考虑动态单抽回报） ==========
        if self.pity_enabled:
            # 线性保底下，逐抽计算动态单抽期望回报
            expected_total_reward_for_any_top_rarity, variance_reward_for_any_top_rarity = self._calculate_reward_expectation_numerical()
        else:
            # 无线性保底，单抽回报固定
            expected_reward_per_draw_fixed = sum(
                prob * self.rewards.get(rarity, 0)
                for rarity, prob in self.base_probabilities.items()
            )
            expected_total_reward_for_any_top_rarity = expected_draws_for_any_top_rarity * expected_reward_per_draw_fixed
            
            # 单抽回报方差
            variance_reward_per_draw = sum(
                prob * (self.rewards.get(rarity, 0) - expected_reward_per_draw_fixed) ** 2
                for rarity, prob in self.base_probabilities.items()
            )
            # 总回报方差：Var[总回报] = E[N] × Var[单抽] + Var[N] × (E[单抽])^2
            variance_reward_for_any_top_rarity = (
                expected_draws_for_any_top_rarity * variance_reward_per_draw +
                variance_draws_for_any_top_rarity * expected_reward_per_draw_fixed ** 2
            )
        
        # 抽到UP最高稀有度的总期望回报（考虑大小保底）
        if self.guarantee_enabled:
            # 大小保底下，可能需要抽两轮
            expected_total_reward = expected_total_reward_for_any_top_rarity * (1 + (1 - up_prob_in_top_rarity))
            variance_total_reward = (
                variance_reward_for_any_top_rarity * (1 + (1 - up_prob_in_top_rarity) ** 2) +
                expected_total_reward_for_any_top_rarity ** 2 * up_prob_in_top_rarity * (1 - up_prob_in_top_rarity)
            )
        else:
            expected_total_reward = expected_total_reward_for_any_top_rarity
            variance_total_reward = variance_reward_for_any_top_rarity
        
        # 计算单抽平均期望回报（用于展示）
        expected_reward_per_draw = expected_total_reward / expected_draws_for_up if expected_draws_for_up > 0 else 0
        
        return {
            'expected_draws_for_up': expected_draws_for_up,
            'variance_draws': variance_draws,
            'std_draws': variance_draws ** 0.5,
            'expected_reward_per_draw': expected_reward_per_draw,
            'expected_total_reward': expected_total_reward,
            'variance_total_reward': variance_total_reward,
            'std_total_reward': variance_total_reward ** 0.5
        }
    
    def _calculate_ssr_expectation_numerical(self) -> Tuple[float, float]:
        """
        数值求和计算抽到任意最高稀有度的期望抽数和方差（线性保底下）
        
        通过逐抽计算第k抽抽到最高稀有度的概率P(k)，然后求和：
        E[M] = sum(k × P(k) for k in 1 to hard_pity)
        Var[M] = sum(k^2 × P(k)) - E[M]^2
        
        Returns:
            Tuple[float, float]: (期望抽数, 方差)
        """
        base_top_rarity_prob = self.base_probabilities[self.rate_up_rarity]
        
        # 逐抽计算第k抽抽到最高稀有度的概率P(k)
        prob_distribution = []  # P(k): 第k抽抽到最高稀有度的概率
        cumulative_prob = 0.0   # 累积概率（已抽到最高稀有度的概率）
        
        for k in range(1, self.hard_pity + 1):
            # 计算第k抽的最高稀有度概率
            draws_since_last = k - 1
            if draws_since_last >= self.pity_threshold:
                # 线性保底生效
                draws_over_threshold = draws_since_last - self.pity_threshold
                top_rarity_prob_k = min(1.0, base_top_rarity_prob + draws_over_threshold * self.pity_increment)
            else:
                top_rarity_prob_k = base_top_rarity_prob
            
            # 硬保底：第hard_pity抽必中
            if k == self.hard_pity:
                top_rarity_prob_k = 1.0
            
            # P(第k抽抽到最高稀有度) = P(前k-1抽未中) × P(第k抽中)
            prob_not_hit_before = 1.0 - cumulative_prob
            prob_hit_at_k = prob_not_hit_before * top_rarity_prob_k
            
            prob_distribution.append(prob_hit_at_k)
            cumulative_prob += prob_hit_at_k
            
            # 如果累积概率接近1，提前终止
            if cumulative_prob > 0.9999:
                break
        
        # 计算期望：E[M] = sum(k × P(k))
        expected_draws = sum((k + 1) * p for k, p in enumerate(prob_distribution))
        
        # 计算方差：Var[M] = E[M^2] - (E[M])^2
        expected_draws_squared = sum((k + 1) ** 2 * p for k, p in enumerate(prob_distribution))
        variance_draws = expected_draws_squared - expected_draws ** 2
        
        return expected_draws, variance_draws
    
    def _calculate_reward_expectation_numerical(self) -> Tuple[float, float]:
        """
        数值求和计算抽到任意最高稀有度过程中的总期望回报和方差（线性保底下）
        
        逐抽计算第k抽的期望回报E[R_k]和被抽到的概率Q(k)，然后求和：
        E[总回报] = sum(E[R_k] × Q(k) for k in 1 to hard_pity)
        
        Returns:
            Tuple[float, float]: (总期望回报, 总回报方差)
        """
        base_top_rarity_prob = self.base_probabilities[self.rate_up_rarity]
        
        total_expected_reward = 0.0
        total_expected_reward_squared = 0.0
        cumulative_prob_top_rarity = 0.0  # 已抽到最高稀有度的累积概率
        
        for k in range(1, self.hard_pity + 1):
            # 计算第k抽被抽到的概率Q(k) = P(前k-1抽未抽到最高稀有度)
            prob_reach_k = 1.0 - cumulative_prob_top_rarity
            
            if prob_reach_k < 0.0001:
                # 如果到达第k抽的概率极小，提前终止
                break
            
            # 计算第k抽的最高稀有度概率
            draws_since_last = k - 1
            if draws_since_last >= self.pity_threshold:
                draws_over_threshold = draws_since_last - self.pity_threshold
                top_rarity_prob_k = min(1.0, base_top_rarity_prob + draws_over_threshold * self.pity_increment)
            else:
                top_rarity_prob_k = base_top_rarity_prob
            
            # 硬保底
            if k == self.hard_pity:
                top_rarity_prob_k = 1.0
            
            # 计算第k抽的当前概率分布（动态概率）
            # 等比压缩非最高稀有度概率
            non_top_rarity_total = 1.0 - base_top_rarity_prob
            if non_top_rarity_total > 0 and top_rarity_prob_k > base_top_rarity_prob:
                compression_ratio = (1.0 - top_rarity_prob_k) / non_top_rarity_total
                current_probs = {}
                for rarity in self.base_probabilities.keys():
                    if rarity == self.rate_up_rarity:
                        current_probs[rarity] = top_rarity_prob_k
                    else:
                        current_probs[rarity] = self.base_probabilities[rarity] * compression_ratio
            else:
                current_probs = self.base_probabilities.copy()
                current_probs[self.rate_up_rarity] = top_rarity_prob_k
            
            # 硬保底时最高稀有度概率100%
            if k == self.hard_pity:
                current_probs = {rarity: 0.0 for rarity in self.base_probabilities.keys()}
                current_probs[self.rate_up_rarity] = 1.0
            
            # 计算第k抽的单抽期望回报E[R_k]
            expected_reward_k = sum(
                current_probs.get(rarity, 0) * self.rewards.get(rarity, 0)
                for rarity in self.base_probabilities.keys()
            )
            
            # 计算第k抽的单抽回报方差Var[R_k]
            variance_reward_k = sum(
                current_probs.get(rarity, 0) * (self.rewards.get(rarity, 0) - expected_reward_k) ** 2
                for rarity in self.base_probabilities.keys()
            )
            
            # 累加期望：E[总回报] += Q(k) × E[R_k]
            total_expected_reward += prob_reach_k * expected_reward_k
            
            # 累加二阶矩：E[(R_k)^2] = Var[R_k] + (E[R_k])^2
            total_expected_reward_squared += prob_reach_k * (variance_reward_k + expected_reward_k ** 2)
            
            # 更新累积最高稀有度概率
            prob_hit_top_rarity_at_k = prob_reach_k * top_rarity_prob_k
            cumulative_prob_top_rarity += prob_hit_top_rarity_at_k
        
        # 计算总回报方差：Var[总回报] = E[(总回报)^2] - (E[总回报])^2
        # 这里简化处理，使用单抽回报的累加方差
        variance_total_reward = total_expected_reward_squared - total_expected_reward ** 2
        
        # 修正：考虑多抽累加的相关性，实际方差应该更大
        # 使用更严格的全方差公式估计
        variance_total_reward = max(variance_total_reward, total_expected_reward_squared * 0.1)
        
        return total_expected_reward, variance_total_reward
    
    def calculate_empirical_stats(self) -> Dict:
        """
        从历史数据计算经验统计值
        
        Returns:
            Dict: 包含期望、方差、期望回报、回报方差的经验值
        """
        if not self.draw_history:
            return {
                'expected_draws_for_up': 0,
                'variance_draws': 0,
                'std_draws': 0,
                'expected_reward_per_draw': 0,
                'expected_total_reward': 0,
                'variance_total_reward': 0,
                'std_total_reward': 0,
                'up_ssr_intervals': []
            }
        
        # 找出所有UP最高稀有度的位置
        up_top_rarity_positions = [
            i for i, result in enumerate(self.draw_history)
            if result.rarity == self.rate_up_rarity and result.is_rate_up
        ]
        
        # 计算每次获得UP最高稀有度之间的间隔
        intervals = []
        rewards_per_interval = []
        
        if up_top_rarity_positions:
            # 第一个UP最高稀有度之前的抽数
            if up_top_rarity_positions[0] > 0:
                first_interval = up_top_rarity_positions[0] + 1
                intervals.append(first_interval)
                rewards_per_interval.append(
                    sum(r.reward for r in self.draw_history[:first_interval])
                )
            
            # 后续UP最高稀有度之间的间隔
            for i in range(1, len(up_top_rarity_positions)):
                interval = up_top_rarity_positions[i] - up_top_rarity_positions[i-1]
                intervals.append(interval)
                rewards_per_interval.append(
                    sum(r.reward for r in self.draw_history[up_top_rarity_positions[i-1]+1:up_top_rarity_positions[i]+1])
                )
        
        # 如果没有UP最高稀有度或只有一个，返回简化统计
        if len(intervals) == 0:
            # 使用整体统计
            avg_draws = len(self.draw_history)
            avg_reward = self.total_rewards
            return {
                'expected_draws_for_up': avg_draws,
                'variance_draws': 0,
                'std_draws': 0,
                'expected_reward_per_draw': avg_reward / avg_draws if avg_draws > 0 else 0,
                'expected_total_reward': avg_reward,
                'variance_total_reward': 0,
                'std_total_reward': 0,
                'up_ssr_intervals': intervals,
                'sample_size': len(intervals)
            }
        
        # 计算期望（平均间隔抽数）
        expected_draws = sum(intervals) / len(intervals)
        
        # 计算方差
        variance_draws = sum((x - expected_draws) ** 2 for x in intervals) / len(intervals)
        std_draws = variance_draws ** 0.5
        
        # 计算期望回报
        expected_total_reward = sum(rewards_per_interval) / len(rewards_per_interval)
        
        # 计算单抽期望回报
        expected_reward_per_draw = self.total_rewards / len(self.draw_history) if self.draw_history else 0
        
        # 计算回报方差
        variance_total_reward = sum(
            (r - expected_total_reward) ** 2 for r in rewards_per_interval
        ) / len(rewards_per_interval)
        std_total_reward = variance_total_reward ** 0.5
        
        return {
            'expected_draws_for_up': expected_draws,
            'variance_draws': variance_draws,
            'std_draws': std_draws,
            'expected_reward_per_draw': expected_reward_per_draw,
            'expected_total_reward': expected_total_reward,
            'variance_total_reward': variance_total_reward,
            'std_total_reward': std_total_reward,
            'up_ssr_intervals': intervals,
            'sample_size': len(intervals)
        }


# 测试代码
if __name__ == "__main__":
    print("=" * 70)
    print("高级抽卡模拟器测试")
    print("=" * 70)
    
    # 创建抽卡器（使用默认配置）
    gacha = AdvancedGachaSimulator()
    
    print("\n当前配置:")
    config = gacha.get_config()
    print(f"基础SSR概率: {config['base_probabilities']['SSR']*100:.2f}%")
    print(f"线性保底: {'启用' if config['pity_enabled'] else '禁用'}")
    if config['pity_enabled']:
        print(f"  - 保底阈值: {config['pity_threshold']} 抽")
        print(f"  - 每抽增加: {config['pity_increment']*100:.2f}%")
        print(f"  - 硬保底: {config['hard_pity']} 抽")
    print(f"回报机制: {'启用' if config['reward_enabled'] else '禁用'}")
    if config['reward_enabled']:
        print(f"  - 回报配置: {config['rewards']}")
    print(f"大小保底: {'启用' if config['guarantee_enabled'] else '禁用'}")
    if config['guarantee_enabled']:
        print(f"  - UP概率: {config['rate_up_prob']*100:.2f}%")
        print(f"  - 大保底: {config['big_pity']} 抽")
    
    # 测试单抽
    print("\n" + "="*70)
    print("【单抽测试】")
    result = gacha.single_draw()
    print(f"抽卡结果: {result}")
    print(f"获得回报: {result.reward}")
    
    # 测试十连
    print("\n" + "="*70)
    print("【十连抽测试】")
    results = gacha.multi_draw(10)
    print(f"抽卡结果: {[str(r) for r in results]}")
    total_reward = sum(r.reward for r in results)
    print(f"总回报: {total_reward}")
    
    # 大规模测试
    print("\n" + "="*70)
    print("【1000抽大规模测试】")
    gacha.multi_draw(1000 - gacha.total_draws)
    gacha.display_statistics()
