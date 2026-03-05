# 示例代码

本目录包含GachaSimulator的使用示例，帮助你快速上手。

## 📁 示例文件

### 1. `basic_character_pool.py` - 基础角色池示例

演示标准角色池的基本用法：
- 创建标准角色池
- 单抽和十连抽卡
- 查看统计信息
- 大规模模拟测试

**运行方式：**
```bash
cd examples
python basic_character_pool.py
```

**关键功能：**
- `create_standard_character_pool()` - 创建标准角色池
- `pool.single_draw()` - 单次抽卡
- `pool.multi_draw(10)` - 十连抽卡
- `pool.get_statistics()` - 获取统计信息

---

### 2. `weapon_pool_fate.py` - 武器池命定值机制

演示武器池特有的命定值（Epitomized Path）机制：
- 命定值累积机制
- 2次歪后保底
- 武器池统计分析

**运行方式：**
```bash
cd examples
python weapon_pool_fate.py
```

**关键功能：**
- `create_standard_weapon_pool()` - 创建标准武器池
- `pool.fate_points` - 查看当前命定值
- 命定值在获得非UP五星时+1，获得UP五星或达到2时重置

---

### 3. `custom_pool.py` - 自定义配置示例

演示如何创建完全自定义的抽卡池：
- 自定义概率
- 自定义保底机制
- 自定义稀有度名称
- 自定义回报值

**运行方式：**
```bash
cd examples
python custom_pool.py
```

**关键功能：**
- 自定义`base_probabilities` - 基础概率
- 自定义`pity_threshold`和`hard_pity` - 保底机制
- 自定义稀有度名称（如"金色"、"紫色"等）

**配置示例：**
```python
custom_config = {
    'name': '福利池',
    'base_probabilities': {
        'SSR': 0.03,  # 3% SSR概率
        'SR': 0.10,
        'R': 0.40,
        'N': 0.47
    },
    'pity_threshold': 50,
    'hard_pity': 60,
    'rewards': {...},
    ...
}

pool = CharacterPool(custom_config, use_custom_config=True)
```

---

### 4. `run_webui.py` - Web界面启动

启动Web可视化界面，提供完整的图形化操作：
- 池子切换（角色池/武器池）
- 交互式抽卡
- 实时统计图表
- 历史记录查看

**运行方式：**
```bash
cd examples
python run_webui.py
```

然后在浏览器中访问：`http://127.0.0.1:5000`

---

## 🚀 快速开始

### 最简单的例子

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gacha_simulator import create_standard_character_pool

# 创建池子
pool = create_standard_character_pool()

# 抽一发
result = pool.single_draw()
print(f"获得: {result.rarity}, UP: {result.is_rate_up}")

# 十连
results = pool.multi_draw(10)
for r in results:
    print(f"{r.rarity} - {r.reward}")

# 查看统计
stats = pool.get_statistics()
print(f"SSR数量: {stats['count_SSR']}")
```

---

## 📊 核心API

### 创建池子

```python
# 标准角色池
from gacha_simulator import create_standard_character_pool
pool = create_standard_character_pool()

# 限定角色池
from gacha_simulator import create_limited_character_pool
pool = create_limited_character_pool()

# 新手角色池
from gacha_simulator import create_novice_character_pool
pool = create_novice_character_pool()

# 武器池
from gacha_simulator import create_standard_weapon_pool
pool = create_standard_weapon_pool()
```

### 抽卡操作

```python
# 单抽
result = pool.single_draw()

# 十连
results = pool.multi_draw(10)

# 大规模模拟
results = pool.multi_draw(100000)
```

### 统计信息

```python
# 获取统计
stats = pool.get_statistics()

# 获取池子信息
info = pool.get_pool_info()

# 计算理论统计
theoretical = pool.calculate_theoretical_stats()

# 计算经验统计
empirical = pool.calculate_empirical_stats()

# 重置统计
pool.reset_statistics()
```

---

## 💡 使用技巧

1. **大规模测试**：使用`multi_draw()`进行大规模模拟，可以快速验证概率机制
2. **自定义配置**：通过自定义配置可以模拟任何抽卡系统
3. **Web界面**：对于非技术用户，推荐使用Web界面进行交互
4. **统计分析**：使用`calculate_theoretical_stats()`和`calculate_empirical_stats()`对比理论与实际

---

## ❓ 常见问题

**Q: 如何修改SSR概率？**

A: 创建自定义配置，修改`base_probabilities`中的`SSR`值：
```python
custom_config = {'base_probabilities': {'SSR': 0.02, ...}}
pool = CharacterPool(custom_config, use_custom_config=True)
```

**Q: 如何关闭保底机制？**

A: 设置`pity_enabled=False`：
```python
custom_config = {'pity_enabled': False, ...}
```

**Q: 如何使用完全自定义的稀有度？**

A: 在`base_probabilities`中定义任意名称的稀有度：
```python
custom_config = {
    'base_probabilities': {
        '传说': 0.01,
        '史诗': 0.05,
        '精良': 0.24,
        '普通': 0.70
    },
    'rate_up_rarity': '传说',
    ...
}
```

---

更多信息请查看主项目README和docs目录中的文档。
