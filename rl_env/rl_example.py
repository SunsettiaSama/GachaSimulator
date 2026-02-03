# -*- coding: utf-8 -*-
"""
强化学习训练示例
演示如何使用 GachaEnvironment 进行RL训练
"""

import numpy as np
from typing import Dict, Tuple
from gacha_environment import GachaEnvironment


class GachaRLWrapper:
    """
    抽卡环境的RL包装器
    提供标准的RL接口：reset(), step(), get_observation()
    """
    
    def __init__(self, 
                 max_steps: int = 1000,
                 budget: int = 100000,
                 target_pool: str = 'character',
                 reward_shaping: str = 'simple'):
        """
        初始化RL包装器
        
        Args:
            max_steps: 最大步数
            budget: 预算（总回报限制）
            target_pool: 目标池子（'character' 或 'weapon'）
            reward_shaping: 奖励塑形方式（'simple', 'dense', 'sparse'）
        """
        self.env = GachaEnvironment()
        self.max_steps = max_steps
        self.budget = budget
        self.target_pool = target_pool
        self.reward_shaping = reward_shaping
        
        # 训练状态
        self.current_step = 0
        self.cumulative_reward = 0
        self.total_cost = 0
        
        # 动作空间：0=不抽, 1=单抽, 2=十连
        self.action_space_size = 3
        
        # 状态空间维度（根据观测值计算）
        self.observation_size = self._get_observation_size()
    
    def reset(self) -> np.ndarray:
        """
        重置环境
        
        Returns:
            np.ndarray: 初始观测值
        """
        self.env.reset()
        self.current_step = 0
        self.cumulative_reward = 0
        self.total_cost = 0
        
        return self._get_observation()
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        执行一步动作
        
        Args:
            action: 动作编码
                0 - 不抽卡（跳过）
                1 - 单抽
                2 - 十连
        
        Returns:
            Tuple[observation, reward, done, info]:
                - observation: 新的观测值
                - reward: 即时奖励
                - done: 是否结束
                - info: 额外信息
        """
        self.current_step += 1
        reward = 0.0
        info = {'action': action}
        
        # 执行动作
        if action == 0:
            # 不抽卡
            info['draws'] = 0
            info['results'] = []
            # 给予小惩罚，鼓励探索
            reward = -0.1
        
        elif action == 1:
            # 单抽
            result, state = self.env.single_draw(self.target_pool)
            info['draws'] = 1
            info['results'] = [result]
            self.total_cost += 160  # 假设单抽160原石
            
            # 计算奖励
            reward = self._calculate_reward([result], state)
        
        elif action == 2:
            # 十连
            results, state = self.env.multi_draw(self.target_pool, 10)
            info['draws'] = 10
            info['results'] = results
            self.total_cost += 1600  # 假设十连1600原石
            
            # 计算奖励
            reward = self._calculate_reward(results, state)
        
        else:
            raise ValueError(f"无效的动作: {action}")
        
        # 累积奖励
        self.cumulative_reward += reward
        
        # 判断是否结束
        done = self._is_done()
        
        # 获取新的观测值
        observation = self._get_observation()
        
        # 额外信息
        info['step'] = self.current_step
        info['cumulative_reward'] = self.cumulative_reward
        info['total_cost'] = self.total_cost
        
        return observation, reward, done, info
    
    def _get_observation(self) -> np.ndarray:
        """
        获取当前观测值（状态向量）
        
        Returns:
            np.ndarray: 归一化的状态向量
        """
        state = self.env.get_state()
        pool_state = state[f'{self.target_pool}_pool']
        
        if not pool_state['enabled']:
            raise ValueError(f"目标池子 {self.target_pool} 未启用")
        
        pity_info = pool_state['pity_info']
        top_rarity_stats = pool_state['top_rarity_stats']
        current_probs = pool_state['current_probabilities']
        
        # 构造观测向量
        observation = [
            # 保底状态（归一化）
            pity_info.get('draws_since_top_rarity', 0) / 90.0,  # 距上次最高稀有度
            pity_info.get('draws_since_rate_up', 0) / 180.0,     # 距上次UP
            1.0 if pity_info.get('is_guaranteed_rate_up', False) else 0.0,  # 是否保底UP
            
            # 当前概率
            pity_info.get('current_top_rarity_prob', 0.006),  # 最高稀有度当前概率
            
            # 历史统计（归一化）
            min(pool_state.get('total_draws', 0) / 1000.0, 1.0),  # 总抽数
            min(top_rarity_stats.get('total', 0) / 100.0, 1.0),   # 最高稀有度总数
            top_rarity_stats.get('rate_up_ratio', 0.0),            # UP率
            
            # 预算状态（归一化）
            min(self.total_cost / self.budget, 1.0),        # 已用预算比例
            min(self.current_step / self.max_steps, 1.0),   # 已用步数比例
        ]
        
        return np.array(observation, dtype=np.float32)
    
    def _get_observation_size(self) -> int:
        """
        获取观测向量的维度
        
        Returns:
            int: 观测向量维度
        """
        # 临时获取一次观测来确定维度
        self.env.reset()
        obs = self._get_observation()
        return len(obs)
    
    def _calculate_reward(self, results, state) -> float:
        """
        计算奖励（奖励塑形）
        
        Args:
            results: 抽卡结果列表
            state: 环境状态
        
        Returns:
            float: 奖励值
        """
        pool_state = state[f'{self.target_pool}_pool']
        
        if self.reward_shaping == 'simple':
            # 简单奖励：基于稀有度
            reward = 0.0
            for r in results:
                if r.rarity == '5-star':
                    if r.is_rate_up:
                        reward += 100.0  # UP 5星
                    else:
                        reward += 30.0   # 非UP 5星
                elif r.rarity == '4-star':
                    reward += 1.0
                else:
                    reward -= 0.1  # 3星小惩罚
            return reward
        
        elif self.reward_shaping == 'dense':
            # 密集奖励：考虑保底进度
            reward = 0.0
            
            # 基础稀有度奖励
            for r in results:
                if r.rarity == '5-star':
                    if r.is_rate_up:
                        reward += 100.0
                    else:
                        reward += 30.0
                elif r.rarity == '4-star':
                    reward += 1.0
            
            # 保底进度奖励（接近保底时给予小奖励）
            draws_since = pool_state['pity_info']['draws_since_top_rarity']
            if draws_since >= 70:
                reward += (draws_since - 70) * 0.1  # 70抽后每抽增加0.1
            
            return reward
        
        elif self.reward_shaping == 'sparse':
            # 稀疏奖励：仅UP给奖励
            reward = 0.0
            for r in results:
                if r.rarity == '5-star' and r.is_rate_up:
                    reward = 100.0
            return reward
        
        else:
            raise ValueError(f"未知的奖励塑形方式: {self.reward_shaping}")
    
    def _is_done(self) -> bool:
        """
        判断是否结束
        
        Returns:
            bool: 是否结束
        """
        # 超过最大步数
        if self.current_step >= self.max_steps:
            return True
        
        # 超过预算
        if self.total_cost >= self.budget:
            return True
        
        # 可以添加其他终止条件，如获得足够的UP角色等
        
        return False
    
    def render(self):
        """
        渲染当前状态（终端输出）
        """
        state = self.env.get_state()
        pool_state = state[f'{self.target_pool}_pool']
        pity_info = pool_state['pity_info']
        
        print(f"步数: {self.current_step}/{self.max_steps} | "
              f"成本: {self.total_cost}/{self.budget} | "
              f"累积奖励: {self.cumulative_reward:.2f} | "
              f"保底: {pity_info['draws_since_top_rarity']}/90 | "
              f"大保底: {pity_info['draws_since_rate_up']}/180")


# ==================== 使用示例 ====================

def random_policy_test():
    """
    随机策略测试
    """
    print("=" * 80)
    print("随机策略测试".center(80))
    print("=" * 80)
    
    env = GachaRLWrapper(
        max_steps=100,
        budget=16000,  # 100抽预算
        target_pool='character',
        reward_shaping='dense'
    )
    
    print(f"\n环境信息:")
    print(f"  动作空间大小: {env.action_space_size}")
    print(f"  观测空间维度: {env.observation_size}")
    print(f"  最大步数: {env.max_steps}")
    print(f"  预算: {env.budget}")
    
    # 重置环境
    obs = env.reset()
    print(f"\n初始观测: {obs}")
    
    # 随机策略
    total_reward = 0
    step = 0
    
    print(f"\n开始随机策略测试...")
    while True:
        # 随机选择动作（偏向抽卡）
        action = np.random.choice([1, 2], p=[0.3, 0.7])  # 30%单抽, 70%十连
        
        # 执行动作
        obs, reward, done, info = env.step(action)
        total_reward += reward
        step += 1
        
        # 每10步显示一次
        if step % 10 == 0:
            env.render()
        
        # 显示重要事件
        if 'results' in info and info['results']:
            for r in info['results']:
                if r.rarity == '5-star':
                    print(f"  >>> 步骤 {step}: 抽到 {r}!")
        
        if done:
            print(f"\n结束! 总奖励: {total_reward:.2f}, 总步数: {step}")
            env.render()
            break
    
    # 显示最终统计
    print(f"\n{'最终统计':-^80}")
    env.env.display_statistics()


def greedy_policy_test():
    """
    贪心策略测试（总是选择十连）
    """
    print("\n" + "=" * 80)
    print("贪心策略测试（总是十连）".center(80))
    print("=" * 80)
    
    env = GachaRLWrapper(
        max_steps=100,
        budget=16000,
        target_pool='character',
        reward_shaping='simple'
    )
    
    obs = env.reset()
    total_reward = 0
    up_count = 0
    
    print(f"\n开始贪心策略测试...")
    while True:
        # 总是选择十连
        action = 2
        obs, reward, done, info = env.step(action)
        total_reward += reward
        
        # 统计UP
        if 'results' in info and info['results']:
            for r in info['results']:
                if r.rarity == '5-star' and r.is_rate_up:
                    up_count += 1
                    print(f"  >>> 第 {env.current_step} 步: 抽到UP 5星! (总计 {up_count} 个)")
        
        if done:
            print(f"\n结束! 总奖励: {total_reward:.2f}, UP总数: {up_count}")
            env.render()
            break
    
    print(f"\n策略效率: {total_reward / env.total_cost * 1000:.2f} 奖励/1000原石")


if __name__ == '__main__':
    # 运行随机策略测试
    random_policy_test()
    
    # 运行贪心策略测试
    greedy_policy_test()
    
    print("\n" + "=" * 80)
    print("测试完成！".center(80))
    print("=" * 80)
