# GachaSimulator - 高级抽卡模拟器

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

一个功能完整的抽卡模拟器，支持多种池子类型、保底机制、统计分析和Web可视化界面。

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [示例代码](#-示例代码) • [文档](#-文档)

</div>

---

## 📖 项目简介

GachaSimulator是一个用Python编写的高级抽卡模拟器，精确模拟了主流抽卡游戏的概率机制，包括：

- **线性保底机制**：软保底 + 硬保底
- **大小保底系统**：UP角色/武器保底
- **命定值机制**：武器池特有的2次歪后保底
- **回报系统**：模拟抽卡的资源回报
- **多池子支持**：角色池、武器池、新手池、限定池
- **统计分析**：理论与实际概率对比
- **Web可视化**：交互式Web界面

## ✨ 功能特性

### 核心机制

- ✅ **精确的概率模型**：完全符合主流游戏的抽卡机制
- ✅ **线性保底**：软保底后概率线性增长，硬保底必出
- ✅ **大小保底**：首次可能歪，第二次必出UP
- ✅ **命定值系统**（武器池）：2次歪后必定出目标
- ✅ **独立同分布（i.i.d.）**：每次抽卡相互独立
- ✅ **完整统计**：实时追踪所有抽卡数据

### 池子类型

| 池子类型 | 说明 | 特点 |
|---------|------|------|
| **标准角色池** | 常驻角色池 | 50% UP概率，180抽大保底 |
| **限定角色池** | 限定活动池 | 50% UP概率，180抽大保底 |
| **新手角色池** | 新手友好池 | 更高概率，提前保底 |
| **武器池** | 武器专武池 | 命定值机制，80抽硬保底 |

### 可视化界面

- 🎨 **现代化Web界面**：基于Flask + JavaScript
- 📊 **实时统计图表**：Chart.js驱动的可视化
- 🔄 **池子快速切换**：支持角色池/武器池切换
- 📜 **历史记录**：完整的抽卡历史追踪

### 高级功能

- 🛠️ **完全可定制**：自定义概率、保底、稀有度
- 📈 **大规模模拟**：支持百万级抽卡模拟
- 🔬 **统计分析**：理论统计 vs 经验统计对比
- 🤖 **强化学习集成**：RL环境接口（实验性）

## 🚀 快速开始

### 安装依赖

```bash
pip install flask
# 可选：用于强化学习功能
pip install gymnasium numpy
```

### 基础使用

```python
import sys
sys.path.insert(0, 'src')

from gacha_simulator import create_standard_character_pool

# 创建角色池
pool = create_standard_character_pool()

# 单抽
result = pool.single_draw()
print(f"获得: {result.rarity}, UP: {result.is_rate_up}")

# 十连
results = pool.multi_draw(10)
for r in results:
    print(f"{r.rarity} - 回报: {r.reward}")

# 查看统计
stats = pool.get_statistics()
print(f"SSR数量: {stats['count_SSR']}")
print(f"平均每SSR抽数: {stats['avg_draw_per_SSR']:.2f}")
```

### 启动Web界面

```bash
cd examples
python run_webui.py
```

然后在浏览器访问：`http://127.0.0.1:5000`

## 📂 项目结构

```
GachaSimulator/
├── src/                          # 源代码目录
│   ├── gacha_simulator/          # 核心抽卡模拟器
│   │   ├── base.py              # 基础抽卡逻辑
│   │   ├── character.py         # 角色池实现
│   │   ├── weapon.py            # 武器池实现
│   │   └── config/              # 配置管理
│   ├── webui/                   # Web界面
│   │   ├── app.py              # Flask应用
│   │   ├── templates/          # HTML模板
│   │   └── static/             # 静态资源（CSS/JS）
│   ├── visualize_tools/         # 可视化工具
│   ├── rl_env/                  # 强化学习环境
│   ├── main_menu.py            # 命令行菜单
│   ├── workflow.py             # 工作流程
│   └── ...                     # 其他工具脚本
├── examples/                    # 示例代码
│   ├── basic_character_pool.py # 基础角色池示例
│   ├── weapon_pool_fate.py    # 武器池命定值示例
│   ├── custom_pool.py         # 自定义配置示例
│   ├── run_webui.py           # Web界面启动
│   └── README.md              # 示例说明文档
├── docs/                        # 项目文档
│   ├── README.md              # 文档索引
│   └── visualize_tools/       # 可视化工具文档
├── config/                      # 配置文件目录
└── README.md                    # 本文件
```

## 💡 示例代码

### 武器池 - 命定值机制

```python
from gacha_simulator import create_standard_weapon_pool

pool = create_standard_weapon_pool()

# 持续抽卡直到获得UP五星
while True:
    result = pool.single_draw()
    if result.rarity == '五星':
        if result.is_rate_up:
            print(f"✓ 获得目标武器！命定值: {pool.fate_points}")
            break
        else:
            print(f"✗ 歪了！命定值 +1，当前: {pool.fate_points}")
```

### 自定义池子

```python
from gacha_simulator import CharacterPool

# 自定义高概率池
custom_config = {
    'name': '福利池',
    'base_probabilities': {
        'SSR': 0.03,  # 3% SSR（标准为0.6%）
        'SR': 0.10,
        'R': 0.40,
        'N': 0.47
    },
    'pity_threshold': 50,
    'hard_pity': 60,
    'big_pity': 120,
    'rewards': {'SSR': 2000, 'SR': 200, 'R': 50, 'N': 20}
}

pool = CharacterPool(custom_config, use_custom_config=True)
results = pool.multi_draw(100)
```

### 大规模统计分析

```python
pool = create_standard_character_pool()

# 模拟10万抽
pool.multi_draw(100000)

# 获取统计
stats = pool.get_statistics()
theoretical = pool.calculate_theoretical_stats()

print(f"实际SSR率: {stats['count_SSR'] / pool.total_draws * 100:.2f}%")
print(f"理论SSR率: {theoretical['avg_SSR_rate'] * 100:.2f}%")
print(f"平均每SSR: {stats['avg_draw_per_SSR']:.2f} 抽")
```

更多示例请查看 [`examples/`](examples/) 目录。

## 🎯 核心API

### 创建池子

```python
from gacha_simulator import (
    create_standard_character_pool,    # 标准角色池
    create_limited_character_pool,     # 限定角色池
    create_novice_character_pool,      # 新手角色池
    create_standard_weapon_pool,       # 武器池
)
```

### 抽卡操作

```python
# 单抽
result = pool.single_draw()

# 多连（count可以是任意正整数）
results = pool.multi_draw(count=10)

# 大规模模拟
results = pool.multi_draw(100000)
```

### 统计查询

```python
# 基础统计
stats = pool.get_statistics()
# 包含: count_SSR, count_SR, avg_draw_per_SSR, max_pity_SSR 等

# 池子信息
info = pool.get_pool_info()
# 包含: name, probabilities, pity_threshold, hard_pity 等

# 理论统计
theoretical = pool.calculate_theoretical_stats()

# 经验统计
empirical = pool.calculate_empirical_stats()

# 重置统计
pool.reset_statistics()
```

### 抽卡结果

```python
result = pool.single_draw()

result.rarity        # 稀有度：'SSR', 'SR', 'R', 'N'
result.is_rate_up    # 是否为UP：True/False
result.reward        # 回报值：整数
result.is_top_rarity # 是否为最高稀有度：True/False
```

## 📊 统计指标

| 指标 | 说明 |
|------|------|
| `count_SSR` | SSR总数 |
| `count_SR` | SR总数 |
| `count_rate_up_SSR` | UP的SSR数量 |
| `avg_draw_per_SSR` | 平均每个SSR所需抽数 |
| `max_pity_SSR` | 最大连续无SSR抽数 |
| `current_pity_SSR` | 当前SSR保底进度 |
| `guarantee_next_SSR` | 下次SSR是否保底UP |

## 🎨 Web界面功能

启动Web界面后，你可以：

1. **切换池子**：在角色池和武器池之间切换
2. **单抽/十连**：点击按钮进行抽卡
3. **查看统计**：实时查看各稀有度出货率
4. **历史记录**：查看最近的抽卡历史
5. **大规模模拟**：输入抽数进行批量模拟
6. **图表展示**：可视化统计数据

## 🔧 自定义配置

所有配置项：

```python
config = {
    'name': '池子名称',
    
    # 基础概率（必须）
    'base_probabilities': {
        'SSR': 0.006,
        'SR': 0.051,
        'R': 0.300,
        'N': 0.643
    },
    
    # 保底机制
    'pity_enabled': True,           # 是否启用保底
    'pity_threshold': 73,           # 软保底开始抽数
    'pity_increment': 0.06,         # 保底增长率
    'hard_pity': 90,                # 硬保底抽数
    
    # 回报机制
    'reward_enabled': True,         # 是否启用回报
    'rewards': {
        'SSR': 2000,
        'SR': 200,
        'R': 50,
        'N': 20
    },
    
    # 大小保底
    'guarantee_enabled': True,      # 是否启用大保底
    'rate_up_rarity': 'SSR',       # 需要UP的稀有度
    'rate_up_prob': 0.5,           # UP概率
    'big_pity': 180,               # 大保底抽数
}
```

## 📚 文档

- **[示例代码](examples/README.md)** - 快速上手示例
- **[完整文档](docs/README.md)** - 详细文档索引
- **[可视化工具](docs/visualize_tools/README.md)** - 可视化工具文档
- **[API参考](docs/visualize_tools/API_REFERENCE.md)** - API速查表

## 🛠️ 技术栈

- **核心**: Python 3.7+
- **Web框架**: Flask
- **前端**: HTML5 + CSS3 + JavaScript
- **图表**: Chart.js
- **强化学习**: Gymnasium (可选)
    - 基于强化学习的抽卡策略（待完善）

## 🧪 测试

项目包含多个测试脚本：

```bash
cd src

# 大样本测试
python large_sample_test.py

# 大保底测试
python test_big_pity.py

# 交互式菜单
python main_menu.py
```

## 📈 性能

- 单次抽卡: < 0.001ms
- 10连抽卡: < 0.01ms
- 100万次模拟: ~2秒
- 内存占用: < 50MB (不含历史记录)

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License

## ⚠️ 免责声明

本项目仅用于学习和研究目的。所有概率数据和机制仅为模拟，不代表任何真实游戏的实际机制。


---

<div align="center">

**[⬆ 回到顶部](#gachasimulator---高级抽卡模拟器)**

Made with ❤️ by SunsettiaSama
</div>
