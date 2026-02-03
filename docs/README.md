# GachaSimulator 项目文档

欢迎来到 GachaSimulator 项目文档中心！

## 📚 文档导航

### Visualize Tools 可视化工具包

一个基于 matplotlib 和 tkinter 的 Python 可视化工具包，提供便捷的图表展示、绘图和数据标注功能。

**📖 完整文档：** [visualize_tools/README.md](visualize_tools/README.md)

**🚀 快速入门：** [visualize_tools/QUICKSTART.md](visualize_tools/QUICKSTART.md)

**📋 API 速查：** [visualize_tools/API_REFERENCE.md](visualize_tools/API_REFERENCE.md)

---

## 项目结构

```
GachaSimulator/
├── docs/                           # 项目文档
│   └── visualize_tools/            # Visualize Tools 文档
│       ├── README.md               # 完整说明文档
│       ├── QUICKSTART.md           # 快速入门指南
│       └── API_REFERENCE.md        # API 速查表
├── visualize_tools/                # 可视化工具包
│   ├── __init__.py
│   └── utils.py                    # 核心工具模块
├── advanced_gacha.py               # 高级抽卡模拟器
├── gacha_environment.py            # 双池抽卡环境（角色池+武器池）
├── gacha_web.py                    # Flask Web 服务
├── rl_example.py                   # 强化学习示例
├── config_examples.py              # 配置示例
└── run.py                          # 主入口文件
```

---

## 快速链接

### 核心模块文档

- **Visualize Tools**
  - [完整文档](visualize_tools/README.md) - 详细介绍所有功能和 API
  - [快速入门](visualize_tools/QUICKSTART.md) - 5 分钟上手指南
  - [API 参考](visualize_tools/API_REFERENCE.md) - 快速查找函数和参数

### 项目文件

- `advanced_gacha.py` - 抽卡模拟器核心逻辑
- `gacha_environment.py` - RL 训练环境（双池系统）
- `gacha_web.py` - Web 界面后端
- `rl_example.py` - RL 训练示例代码
- `run.py` - 启动脚本

---

## 使用建议

### 新手用户
1. 从 [Visualize Tools 快速入门](visualize_tools/QUICKSTART.md) 开始
2. 查看基础示例代码
3. 参考 [API 速查表](visualize_tools/API_REFERENCE.md) 查找函数

### 高级用户
1. 直接查看 [完整 API 文档](visualize_tools/README.md)
2. 深入研究源代码 `visualize_tools/utils.py`
3. 根据需求自定义和扩展功能

---

## 更新日志

### 2026-02-02
- 创建 Visualize Tools 完整文档
- 添加快速入门指南
- 添加 API 速查表

---

## 贡献指南

欢迎贡献代码和文档！

---

**最后更新：** 2026-02-02
