# Visualize Tools 快速入门指南

## 🚀 5 分钟快速上手

### 安装依赖

```bash
pip install matplotlib numpy pandas scipy pillow
```

---

## 基础用法

### 1. 最简单的线图

```python
from visualize_tools.utils import PlotLib
import numpy as np

# 创建绘图对象
plot_lib = PlotLib()

# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘制并显示
plot_lib.plot(y, x=x, title='My First Plot')
plot_lib.show()
```

**输出：** 弹出交互式窗口，显示正弦曲线

---

### 2. 多个图表一起看

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 创建多个图表
x = np.linspace(0, 10, 100)

plot_lib.plot(np.sin(x), x=x, title='Sine')
plot_lib.plot(np.cos(x), x=x, title='Cosine', color='red')
plot_lib.plot(np.tan(x), x=x, title='Tangent', color='green')

# 一次性显示所有图表（可以用 Next/Previous 切换）
plot_lib.show()
```

---

### 3. 子图排列

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()
x = np.linspace(0, 10, 100)

# 准备多个数据集
data_lis = [
    (x, np.sin(x)),
    (x, np.cos(x)),
    (x, np.exp(-x/10))
]

# 一次性绘制多个子图
plot_lib.plots(
    data_lis,
    titles=['Sine', 'Cosine', 'Exponential'],
    labels=[('Time', 'Amplitude'), ('Time', 'Amplitude'), ('Time', 'Value')],
    color='skyblue'
)

plot_lib.show()
```

---

### 4. 散点图

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 生成随机数据
x = np.random.randn(200)
y = 2*x + np.random.randn(200)  # 有线性关系

plot_lib.scatter(
    x, y, 
    title='Correlation Plot',
    xlabel='X Variable',
    ylabel='Y Variable',
    s=20,  # 点大小
    alpha=0.6,  # 透明度
    color='coral'
)

plot_lib.show()
```

---

### 5. 直方图（分布可视化）

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 生成正态分布数据
data = np.random.normal(loc=0, scale=1, size=1000)

plot_lib.hist(
    data,
    bins=30,
    title='Normal Distribution',
    xlabel='Value',
    ylabel='Frequency',
    density=True,
    color='steelblue'
)

plot_lib.show()
```

---

## 进阶用法

### 6. 风玫瑰图（极坐标直方图）

适用于风向、方位角等圆周数据的分布可视化。

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 模拟风向数据（0-360度）
wind_directions = np.random.uniform(0, 360, 2000)
wind_speeds = np.random.lognormal(2, 0.5, 2000)  # 对数正态分布的风速

plot_lib.rose_hist(
    wind_directions,
    y_datas=wind_speeds,  # 可选：显示平均风速
    title='Wind Direction Distribution',
    separate_bins=16,  # 16个方向扇区
    geographic_orientation=True,  # 使用地理方向标签（N, NE, E, ...）
    top_n_density=3,  # 标注前3个最密集的区间
    highlight_max_speed=True  # 高亮最高风速区间
)

plot_lib.show()
```

---

### 7. 3D 散点图（柱坐标）

适用于风工程、天文等需要柱坐标系的场景。

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 生成柱坐标数据
n = 500
theta = np.random.uniform(0, 2*np.pi, n)  # 角度（弧度）
rho = np.random.uniform(5, 30, n)         # 半径
z = np.random.uniform(0, 50, n)           # 高度

plot_lib.scatter_3d(
    theta, rho, z,
    title='3D Wind Field Data',
    s=10,
    color='skyblue',
    alpha=0.5,
    edgecolor='none'
)

plot_lib.show()
```

**特点：** 自动添加地理方向标签、柱坐标网格、高度刻度

---

### 8. 信号分析（时频域）

快速查看时域信号和功率谱密度（PSD）。

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 生成混合信号
fs = 1000  # 采样频率 1000 Hz
t = np.linspace(0, 1, fs)
signal = (np.sin(2*np.pi*50*t) +      # 50 Hz 分量
          0.5*np.sin(2*np.pi*120*t) +  # 120 Hz 分量
          np.random.normal(0, 0.2, fs))  # 噪声

plot_lib.show_sample(
    signal,
    fs=fs,
    nperseg=256  # Welch 方法的窗口长度
)

plot_lib.show()
```

**输出：** 两个子图，上方为时域波形，下方为功率谱密度

---

### 9. 动画生成

生成动态曲线动画，导出为 GIF 或 MP4。

```python
from visualize_tools.utils import PlotLib
import numpy as np

plot_lib = PlotLib()

# 生成动画数据（50帧）
num_frames = 50
num_points = 100
x_frames = np.zeros((num_frames, num_points))
y_frames = np.zeros((num_frames, num_points))

for i in range(num_frames):
    x_frames[i, :] = np.linspace(0, 10, num_points)
    y_frames[i, :] = np.sin(x_frames[i, :] + i * 0.2)  # 移动的正弦波

data_lis = [(x_frames, y_frames)]

# 生成并保存动画
ani = plot_lib.animate(
    data_lis,
    title=['Moving Sine Wave'],
    labels=[('X', 'Y')],
    fps=10,
    save_path='moving_wave.gif'
)

print("动画已保存为 moving_wave.gif")
```

**注意：** 保存为 MP4 需要安装 `ffmpeg`

---

## 图表查看器（ChartApp）

如果你已经有现成的 matplotlib 图表，可以用 `ChartApp` 快速浏览。

```python
import tkinter as tk
import matplotlib.pyplot as plt
from visualize_tools.utils import ChartApp

# 创建图表列表
figs = []

# 图表 1
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax1.set_title("Quadratic Function")
figs.append(fig1)

# 图表 2
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter([1, 2, 3, 4], [2, 5, 8, 11])
ax2.set_title("Linear Scatter")
figs.append(fig2)

# 启动查看器
root = tk.Tk()
root.title("My Charts")
app = ChartApp(root, figs)
root.mainloop()
```

**操作：**
- **Previous** 按钮：上一张图
- **Next** 按钮：下一张图
- **Save** 按钮：保存当前图为 PNG

---

## 数据标注工具

批量标注图像数据并导出为 Excel。

```python
from tkinter import Tk
from visualize_tools.utils import _Propose_Data_GUI

root = Tk()
app = _Propose_Data_GUI(
    root,
    save_excel_root='annotations.xlsx',
    default_img_root=r'C:\MyImages'  # 默认图像文件夹
)
root.mainloop()
```

**操作流程：**
1. 启动后选择包含图像的文件夹
2. 在输入框中输入标注值（例如：类别、数值等）
3. 按 `Enter` 或点击 **Next** 进入下一张
4. 按 `Ctrl+S` 或点击 **Save** 保存到 Excel

**快捷键：**
- `Enter` - 下一张
- `Left Arrow` - 上一张
- `Ctrl+S` - 保存

---

## 常用技巧

### 1. 保存单个图表

```python
plot_lib = PlotLib()
fig, ax = plot_lib.plot([1, 2, 3], [4, 5, 6], title='My Chart')

# 保存为高分辨率 PNG
fig.savefig('my_chart.png', dpi=300, bbox_inches='tight')
```

---

### 2. 批量保存所有图表

```python
plot_lib = PlotLib()

# 创建多个图表
plot_lib.plot([1, 2, 3], [4, 5, 6], title='Chart 1')
plot_lib.plot([1, 2, 3], [6, 5, 4], title='Chart 2')

# 批量保存
for i, fig in enumerate(plot_lib.figs):
    fig.savefig(f'chart_{i+1}.png', dpi=300, bbox_inches='tight')
    print(f'Saved chart_{i+1}.png')
```

---

### 3. 自定义颜色和样式

```python
plot_lib = PlotLib()

# 自定义线型和颜色
plot_lib.plot(
    [1, 2, 3, 4], [1, 4, 9, 16],
    title='Styled Plot',
    color='darkblue',
    style='--',  # 虚线
    alpha=0.8,
    legend='Quadratic'
)

plot_lib.show()
```

**可用线型：**
- `'-'` 实线
- `'--'` 虚线
- `'-.'` 点划线
- `':'` 点线

---

### 4. 设置坐标轴范围

```python
plot_lib = PlotLib()

x = np.linspace(0, 10, 100)
y = np.sin(x)

plot_lib.plot(
    y, x=x,
    title='Sine with Custom Limits',
    xlim=(2, 8),  # X轴范围
    ylim=(-0.5, 0.5)  # Y轴范围
)

plot_lib.show()
```

---

### 5. 在同一图上绘制多条曲线

```python
import matplotlib.pyplot as plt
from visualize_tools.utils import PlotLib

plot_lib = PlotLib()
x = np.linspace(0, 10, 100)

# 创建图表对象
fig, ax = plt.subplots()

# 绘制多条曲线（使用同一个 ax）
plot_lib.plot(np.sin(x), x=x, fig=fig, ax=ax, color='blue', legend='sin(x)', add_fig=False)
plot_lib.plot(np.cos(x), x=x, fig=fig, ax=ax, color='red', legend='cos(x)', add_fig=False)

# 添加图例
ax.legend()
ax.set_title('Multiple Curves')

# 手动添加到图表列表
plot_lib.figs.append(fig)

plot_lib.show()
```

---

## 下一步

- 查看 [完整 API 文档](README.md#api-参考)
- 查看 [使用示例](README.md#使用示例)
- 探索更多绘图方法

---

**祝你绘图愉快！** 🎨
