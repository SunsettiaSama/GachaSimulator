# Visualize Tools 可视化工具包

## 📚 目录

- [简介](#简介)
- [依赖项](#依赖项)
- [核心组件](#核心组件)
  - [ChartApp - 图表查看器](#chartapp---图表查看器)
  - [PlotLib - 绘图库](#plotlib---绘图库)
  - [_Propose_Data_GUI - 数据标注工具](#_propose_data_gui---数据标注工具)
- [使用示例](#使用示例)
- [API 参考](#api-参考)

---

## 简介

`visualize_tools` 是一个基于 **matplotlib** 和 **tkinter** 的 Python 可视化工具包，提供便捷的图表展示、绘图和数据标注功能。

**主要特性：**
- 📊 **多图表管理**：通过交互式 GUI 浏览多个图表
- 🎨 **丰富的绘图类型**：线图、散点图、直方图、极坐标图、3D 散点图等
- 💾 **图表保存**：一键导出当前图表为 PNG 文件
- 🏷️ **数据标注**：批量标注图像数据并导出为 Excel

---

## 依赖项

```bash
pip install tkinter matplotlib numpy pandas scipy pillow
```

**主要依赖：**
- `tkinter` - GUI 界面
- `matplotlib` - 绘图引擎
- `numpy` - 数值计算
- `pandas` - 数据处理
- `scipy` - 科学计算（信号处理）
- `Pillow (PIL)` - 图像处理

---

## 核心组件

### ChartApp - 图表查看器

**描述：** 一个基于 Tkinter 的交互式图表查看器，允许用户在多个 matplotlib 图表之间切换浏览。

**核心功能：**
- ⏮️ **前后切换**：Previous/Next 按钮切换图表
- 💾 **保存当前图表**：Save 按钮导出为 PNG
- 🔄 **循环浏览**：图表列表循环展示

**使用示例：**

```python
import tkinter as tk
import matplotlib.pyplot as plt
from visualize_tools.utils import ChartApp

# 创建多个图表
figs = []

# 图表1
fig1, ax1 = plt.subplots()
ax1.plot([1, 2, 3], [4, 5, 6])
ax1.set_title("Chart 1")
figs.append(fig1)

# 图表2
fig2, ax2 = plt.subplots()
ax2.plot([1, 2, 3], [6, 5, 4])
ax2.set_title("Chart 2")
figs.append(fig2)

# 启动查看器
root = tk.Tk()
root.title("Matplotlib Charts in Tkinter")
app = ChartApp(root, figs)
root.mainloop()
```

---

### PlotLib - 绘图库

**描述：** 一个高级绘图类，封装了常用的 matplotlib 绘图操作，支持多种图表类型和自动管理图表列表。

#### 主要方法

##### 1. `plot()` - 基础线图

绘制单条曲线。

**参数：**
- `y` (array-like): Y 轴数据
- `x` (array-like, optional): X 轴数据（默认索引）
- `title` (str): 图表标题
- `xlabel`, `ylabel` (str): 坐标轴标签
- `color` (str): 线条颜色（默认 'skyblue'）
- `legend` (str): 图例标签
- `xlim`, `ylim` (tuple): 坐标轴范围
- `dpi` (int): 图像分辨率
- `style` (str): 线型（'-', '--', '-.', ':'）
- `alpha` (float): 透明度（0-1）
- `add_fig` (bool): 是否添加到图表列表（默认 True）

**示例：**
```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plot_lib.plot(y, x=x, title='Sine Wave', xlabel='Time', ylabel='Amplitude', color='blue')
plot_lib.show()
```

---

##### 2. `plots()` - 多子图绘制

绘制多个子图（垂直排列）。

**参数：**
- `data_lis` (list of tuples): [(x1, y1), (x2, y2), ...]
- `titles` (list): 各子图标题
- `labels` (list of tuples): [(xlabel1, ylabel1), ...]
- `xlims`, `ylims` (list of tuples): 坐标轴范围列表
- `coordinate_systems` (list): 坐标系类型列表（'linear', 'loglog', 'semilogy'）
- `color`, `alpha`: 线条颜色和透明度

**示例：**
```python
import numpy as np

x = np.linspace(0, 10, 100)
data_lis = [
    (x, np.sin(x)),
    (x, np.cos(x)),
    (x, np.exp(-x/10))
]

titles = ['Sine', 'Cosine', 'Exponential Decay']
labels = [('Time', 'Amplitude'), ('Time', 'Amplitude'), ('Time', 'Value')]

plot_lib.plots(data_lis, titles=titles, labels=labels, color='red')
plot_lib.show()
```

---

##### 3. `scatter()` - 散点图

绘制 2D 散点图。

**参数：**
- `x`, `y` (array-like): 数据点坐标
- `s` (float): 点的大小
- `marker` (str): 标记样式（'o', 's', '^', 'x', ...）
- `alpha` (float): 透明度

**示例：**
```python
x = np.random.randn(100)
y = np.random.randn(100)

plot_lib.scatter(x, y, title='Random Scatter', xlabel='X', ylabel='Y', 
                 s=10, color='green', alpha=0.6)
plot_lib.show()
```

---

##### 4. `scatters()` - 多子图散点图

绘制多个散点图子图。

**参数：**
- `data_lis` (list of tuples): [(x1, y1), (x2, y2), ...]
- `s` (float): 点大小（默认 0.8）
- 其他参数同 `plots()`

**示例：**
```python
data_lis = [
    (np.random.randn(100), np.random.randn(100)),
    (np.random.randn(100), np.random.randn(100))
]

plot_lib.scatters(data_lis, titles=['Dataset 1', 'Dataset 2'], s=5)
plot_lib.show()
```

---

##### 5. `hist()` - 直方图

绘制直方图（频率分布）。

**参数：**
- `x` (array-like): 数据
- `bins` (int): 直方图箱数（默认 50）
- `density` (bool): 是否归一化（默认 True）

**示例：**
```python
data = np.random.normal(0, 1, 1000)

plot_lib.hist(data, bins=30, title='Normal Distribution', 
              xlabel='Value', ylabel='Frequency', density=True)
plot_lib.show()
```

---

##### 6. `rose_hist()` - 极坐标直方图（风玫瑰图）

绘制极坐标直方图，常用于风向分布等。

**参数：**
- `x` (array-like): 角度数据（度）
- `y_datas` (array-like, optional): 对应的数值数据（如风速）
- `separate_bins` (int): 扇形区间数（默认 20）
- `density` (bool): 是否归一化
- `geographic_orientation` (bool): 是否使用地理方向标签（N, NE, E, ...）
- `bridge_axis` (bool): 是否显示桥梁轴线
- `log_y` (bool): Y 轴是否使用对数坐标
- `top_n_density` (int): 标注密度最高的 N 个区间
- `highlight_max_speed` (bool): 是否高亮最高平均风速区间

**示例：**
```python
# 模拟风向数据（度）
wind_directions = np.random.uniform(0, 360, 1000)
wind_speeds = np.random.uniform(5, 20, 1000)

plot_lib.rose_hist(wind_directions, y_datas=wind_speeds, 
                   title='Wind Direction Distribution',
                   separate_bins=16, 
                   geographic_orientation=True,
                   top_n_density=3)
plot_lib.show()
```

---

##### 7. `rose_scatter()` - 极坐标散点图

绘制极坐标散点图。

**参数：**
- `theta` (array-like): 角度（弧度）
- `rho` (array-like): 半径
- `cmap` (str): 颜色映射（'viridis', 'plasma', 'jet', ...）
- `c_data` (array-like): 颜色数据（用于渲染颜色）
- `colorbar` (bool): 是否显示颜色条
- `color_label` (str): 颜色条标签
- `norm` (matplotlib.colors.Normalize): 颜色归一化对象

**示例：**
```python
theta = np.linspace(0, 2*np.pi, 200)
rho = np.random.uniform(1, 10, 200)
colors = rho  # 使用半径作为颜色

plot_lib.rose_scatter(theta, rho, title='Polar Scatter', 
                      cmap='viridis', c_data=colors, 
                      colorbar=True, color_label='Radius')
plot_lib.show()
```

---

##### 8. `scatter_3d()` - 3D 散点图（柱坐标）

绘制 3D 散点图，支持柱坐标系（theta, rho, z）。

**参数：**
- `theta` (array-like): 角度（弧度）
- `rho` (array-like): 半径
- `z` (array-like): 高度
- `marker`, `color`, `edgecolor`, `s`, `alpha`: 标记样式

**特殊功能：**
- 自动添加地理方向标签（N, NE, E, ...）
- 自动绘制柱坐标网格
- 自定义 Z 轴刻度

**示例：**
```python
theta = np.random.uniform(0, 2*np.pi, 300)
rho = np.random.uniform(5, 30, 300)
z = np.random.uniform(0, 50, 300)

plot_lib.scatter_3d(theta, rho, z, title='3D Wind Data',
                    s=10, color='skyblue', alpha=0.5)
plot_lib.show()
```

---

##### 9. `animate()` - 动画生成

生成动态图表动画，支持导出为 GIF 或 MP4。

**参数：**
- `data_lis` (list of tuples): [(x_frames, y_frames), ...] 
  - `x_frames`, `y_frames`: 形状为 (num_frames, num_points) 的数组
- `fps` (int): 帧率
- `save_path` (str): 保存路径（.gif 或 .mp4）
- `dynamic_adjust` (list of tuples): [(x_adjust, y_adjust), ...] 是否动态调整坐标轴

**示例：**
```python
# 生成动画数据（50帧，每帧100个点）
num_frames = 50
num_points = 100
x_frames = np.zeros((num_frames, num_points))
y_frames = np.zeros((num_frames, num_points))

for i in range(num_frames):
    x_frames[i, :] = np.linspace(0, 10, num_points)
    y_frames[i, :] = np.sin(x_frames[i, :] + i * 0.1)

data_lis = [(x_frames, y_frames)]

ani = plot_lib.animate(data_lis, fps=10, save_path='animation.gif',
                       title=['Moving Sine Wave'],
                       labels=[('X', 'Y')])
```

---

##### 10. `show_sample()` - 信号样本展示

展示时域信号及其功率谱密度（PSD）。

**参数：**
- `data` (array-like): 时域信号
- `fs` (float): 采样频率（Hz）
- `nperseg` (int): Welch 方法的窗口长度
- `scatter` (bool): 是否使用散点图（默认 False）

**示例：**
```python
fs = 1000  # 采样频率 1000 Hz
t = np.linspace(0, 1, fs)
signal = np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.1, fs)

plot_lib.show_sample(signal, fs=fs, nperseg=256)
plot_lib.show()
```

---

##### 11. `show()` - 显示所有图表

启动 ChartApp GUI 显示所有已创建的图表。

**示例：**
```python
# 创建多个图表后
plot_lib.plot([1, 2, 3], [4, 5, 6], title='Chart 1')
plot_lib.plot([1, 2, 3], [6, 5, 4], title='Chart 2')

# 显示所有图表
plot_lib.show()
```

---

### _Propose_Data_GUI - 数据标注工具

**描述：** 一个基于 Tkinter 的图像批量标注 GUI 工具，支持快速浏览图像并输入标注数据，导出为 Excel。

**核心功能：**
- 🖼️ **图像浏览**：逐张浏览图像文件
- ⌨️ **快速标注**：输入框输入标注值
- 📊 **Excel 导出**：保存标注数据到 Excel
- 🔄 **断点续传**：加载已有的标注数据，跳过已完成的图像
- ⚡ **快捷键支持**：
  - `Enter` - 下一张
  - `Left Arrow` - 上一张
  - `Ctrl+S` - 保存到 Excel

**使用示例：**

```python
from tkinter import Tk
from visualize_tools.utils import _Propose_Data_GUI

root = Tk()
app = _Propose_Data_GUI(
    root,
    save_excel_root='annotations.xlsx',
    default_img_root=r'C:\Images',
    image_list=[]  # 留空则弹出文件夹选择对话框
)
root.mainloop()
```

**工作流程：**
1. 启动 GUI，选择包含图像的文件夹
2. 加载已有的 Excel 数据（如有）
3. 逐张浏览图像，输入标注值
4. 实时保存到内存，手动保存到 Excel
5. 自动过滤已标注的图像

---

## 使用示例

### 示例 1：创建多种图表并查看

```python
from visualize_tools.utils import PlotLib
import numpy as np

# 初始化绘图库
plot_lib = PlotLib()

# 1. 线图
x = np.linspace(0, 10, 100)
plot_lib.plot(np.sin(x), x=x, title='Sine Wave', color='blue')

# 2. 散点图
x_scatter = np.random.randn(200)
y_scatter = np.random.randn(200)
plot_lib.scatter(x_scatter, y_scatter, title='Random Points', s=5, alpha=0.6)

# 3. 直方图
data = np.random.normal(0, 1, 1000)
plot_lib.hist(data, bins=30, title='Normal Distribution', density=True)

# 4. 极坐标图
theta = np.linspace(0, 2*np.pi, 100)
rho = np.abs(np.sin(3*theta))
plot_lib.rose_scatter(theta, rho, title='Rose Pattern')

# 显示所有图表
plot_lib.show()
```

---

### 示例 2：风工程数据可视化

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 模拟风向和风速数据
wind_dir = np.random.uniform(0, 360, 5000)  # 风向（度）
wind_speed = np.random.lognormal(2, 0.5, 5000)  # 风速（m/s）

# 风玫瑰图
plot_lib.rose_hist(
    wind_dir, 
    y_datas=wind_speed,
    title='Wind Direction Distribution',
    separate_bins=16,
    geographic_orientation=True,
    bridge_axis=False,
    top_n_density=3,
    highlight_max_speed=True
)

# 3D 风数据散点图
theta = np.deg2rad(wind_dir)
rho = wind_speed
z = np.random.uniform(10, 100, 5000)  # 高度（m）

plot_lib.scatter_3d(theta, rho, z, title='3D Wind Field', s=2, alpha=0.3)

plot_lib.show()
```

---

### 示例 3：批量图像标注

```python
import os
from tkinter import Tk
from visualize_tools.utils import _Propose_Data_GUI

# 准备图像列表
image_folder = r'C:\MyImages'
image_list = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
              if f.endswith(('.png', '.jpg', '.jpeg'))]

# 启动标注工具
root = Tk()
app = _Propose_Data_GUI(
    root,
    save_excel_root='image_labels.xlsx',
    default_img_root=image_folder,
    image_list=image_list
)
root.mainloop()
```

---

## API 参考

### ChartApp

| 方法 | 参数 | 描述 |
|------|------|------|
| `__init__(root, figs)` | `root`: Tkinter 根窗口<br>`figs`: matplotlib 图表列表 | 初始化图表查看器 |
| `show_previous()` | 无 | 显示上一张图表 |
| `show_next()` | 无 | 显示下一张图表 |
| `save_current_chart()` | 无 | 保存当前图表为 PNG |

---

### PlotLib

| 方法 | 主要参数 | 返回值 | 描述 |
|------|----------|--------|------|
| `plot(y, x, ...)` | `y`, `x`, `title`, `color`, `legend` | `(fig, ax)` | 绘制线图 |
| `plots(data_lis, ...)` | `data_lis`, `titles`, `labels` | `(fig, axes)` | 多子图线图 |
| `scatter(x, y, ...)` | `x`, `y`, `s`, `marker`, `color` | `(fig, ax)` | 散点图 |
| `scatters(data_lis, ...)` | `data_lis`, `titles`, `s` | `(fig, axes)` | 多子图散点图 |
| `hist(x, ...)` | `x`, `bins`, `density` | `(fig, ax)` | 直方图 |
| `rose_hist(x, ...)` | `x`, `y_datas`, `separate_bins` | `(fig, ax)` | 极坐标直方图 |
| `rose_scatter(theta, rho, ...)` | `theta`, `rho`, `cmap`, `c_data` | `(fig, ax)` | 极坐标散点图 |
| `scatter_3d(theta, rho, z, ...)` | `theta`, `rho`, `z` | `(fig, ax)` | 3D 散点图 |
| `animate(data_lis, ...)` | `data_lis`, `fps`, `save_path` | `ani` | 生成动画 |
| `show_sample(data, fs, ...)` | `data`, `fs`, `nperseg` | `(fig, axes)` | 信号时频分析 |
| `show()` | 无 | 无 | 显示所有图表 |

---

### _Propose_Data_GUI

| 方法 | 参数 | 描述 |
|------|------|------|
| `__init__(root, save_excel_root, ...)` | `root`, `save_excel_root`, `default_img_root`, `image_list` | 初始化标注工具 |
| `next_image()` | 无 | 下一张图像 |
| `prev_image()` | 无 | 上一张图像 |
| `save_to_excel()` | 无 | 保存到 Excel |

---

## 全局设置

```python
# 设置全局字体大小
GLOBAL_FONT_SIZE = 10

# matplotlib 样式
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.size'] = GLOBAL_FONT_SIZE
```

---

## 常见问题

### Q: 如何自定义图表样式？

A: 可以通过传递 `fig` 和 `ax` 参数来使用自定义的图表对象：

```python
import matplotlib.pyplot as plt
from visualize_tools.utils import PlotLib

# 创建自定义图表
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('#f0f0f0')

# 使用自定义图表
plot_lib = PlotLib()
plot_lib.plot([1, 2, 3], [4, 5, 6], fig=fig, ax=ax, color='red')
plot_lib.show()
```

---

### Q: 如何保存所有图表？

A: 使用 `ChartApp` 的保存功能，或直接遍历 `plot_lib.figs`：

```python
for i, fig in enumerate(plot_lib.figs):
    fig.savefig(f'chart_{i}.png', dpi=300, bbox_inches='tight')
```

---

### Q: 动画保存为 MP4 时报错？

A: 确保安装了 `ffmpeg`：

```bash
# Windows (使用 Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

---

## 许可

该工具包为内部使用，请遵守项目许可协议。

---

## 联系方式

如有问题或建议，请联系项目维护者。

---

**最后更新：** 2026-02-02
