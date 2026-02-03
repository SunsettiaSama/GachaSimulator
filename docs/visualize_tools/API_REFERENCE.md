# Visualize Tools API 速查表

## 目录

- [PlotLib 类](#plotlib-类)
  - [基础绘图](#基础绘图)
  - [高级绘图](#高级绘图)
  - [动画与展示](#动画与展示)
- [ChartApp 类](#chartapp-类)
- [_Propose_Data_GUI 类](#_propose_data_gui-类)

---

## PlotLib 类

### 基础绘图

#### `plot()` - 线图

```python
plot_lib.plot(y, x=None, title=None, xlabel=None, ylabel=None, 
              color=None, legend=None, xlim=None, ylim=None, 
              dpi=None, fig=None, style=None, alpha=None, 
              ax=None, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `y` | array-like | **必需** | Y 轴数据 |
| `x` | array-like | `None` | X 轴数据（默认索引） |
| `title` | str | `None` | 图表标题 |
| `xlabel` | str | `None` | X 轴标签 |
| `ylabel` | str | `None` | Y 轴标签 |
| `color` | str | `'skyblue'` | 线条颜色 |
| `legend` | str | `None` | 图例标签 |
| `xlim` | tuple | `None` | X 轴范围 (min, max) |
| `ylim` | tuple | `None` | Y 轴范围 (min, max) |
| `dpi` | int | `None` | 图像分辨率 |
| `fig` | Figure | `None` | matplotlib Figure 对象 |
| `style` | str | `None` | 线型 ('-', '--', '-.', ':') |
| `alpha` | float | `0.8` | 透明度 (0-1) |
| `ax` | Axes | `None` | matplotlib Axes 对象 |
| `add_fig` | bool | `True` | 是否添加到图表列表 |

**返回值：** `(fig, ax)` - Figure 和 Axes 对象

---

#### `plots()` - 多子图线图

```python
plot_lib.plots(data_lis, color=None, alpha=0.7, titles=None, 
               labels=None, xlims=None, ylims=None, 
               coordinate_systems=None, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data_lis` | list of tuples | **必需** | `[(x1, y1), (x2, y2), ...]` |
| `color` | str | `'skyblue'` | 线条颜色 |
| `alpha` | float | `0.7` | 透明度 |
| `titles` | list of str | `None` | 各子图标题 |
| `labels` | list of tuples | `None` | `[(xlabel1, ylabel1), ...]` |
| `xlims` | list of tuples | `None` | X 轴范围列表 |
| `ylims` | list of tuples | `None` | Y 轴范围列表 |
| `coordinate_systems` | list of str | `None` | `['linear', 'loglog', 'semilogy']` |
| `add_fig` | bool | `True` | 是否添加到图表列表 |

**返回值：** `(fig, axes)` - Figure 和 Axes 列表

---

#### `scatter()` - 散点图

```python
plot_lib.scatter(x, y, title=None, xlabel=None, ylabel=None, 
                 xlim=None, ylim=None, dpi=None, fig=None, 
                 ax=None, marker=None, color=None, legend=None, 
                 s=None, alpha=0.8, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `x` | array-like | **必需** | X 坐标数据 |
| `y` | array-like | **必需** | Y 坐标数据 |
| `s` | float | `1` | 点大小 |
| `marker` | str | `'o'` | 标记样式 ('o', 's', '^', 'x', ...) |
| `color` | str | `'skyblue'` | 点颜色 |
| `legend` | str | `None` | 图例标签 |
| `alpha` | float | `0.8` | 透明度 |
| 其他参数 | - | - | 同 `plot()` |

**返回值：** `(fig, ax)`

---

#### `scatters()` - 多子图散点图

```python
plot_lib.scatters(data_lis, color=None, alpha=0.7, titles=None, 
                  labels=None, xlims=None, ylims=None, 
                  add_fig=True, s=0.8)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data_lis` | list of tuples | **必需** | `[(x1, y1), (x2, y2), ...]` |
| `s` | float | `0.8` | 点大小 |
| 其他参数 | - | - | 同 `plots()` |

**返回值：** `(fig, axes)`

---

#### `hist()` - 直方图

```python
plot_lib.hist(x, bins=50, density=True, title=None, xlabel=None, 
              ylabel=None, dpi=None, fig=None, ax=None, 
              color=None, legend=None, alpha=0.7, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `x` | array-like | **必需** | 数据 |
| `bins` | int | `50` | 直方图箱数 |
| `density` | bool | `True` | 是否归一化 |
| `color` | str | `'skyblue'` | 柱形颜色 |
| `alpha` | float | `0.7` | 透明度 |
| 其他参数 | - | - | 同 `plot()` |

**返回值：** `(fig, ax)`

---

### 高级绘图

#### `rose_hist()` - 极坐标直方图

```python
plot_lib.rose_hist(x, y_datas=None, title='Wind Direction Distribution', 
                   separate_bins=20, density=True, color=None, 
                   fig=None, ax=None, y_label="Percent Frequency (%)", 
                   geographic_orientation=False, bridge_axis=True, 
                   dpi=None, add_fig=True, log_y=False, 
                   top_n_density=3, highlight_max_speed=False)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `x` | array-like | **必需** | 角度数据（度） |
| `y_datas` | array-like | `None` | 对应数值（如风速） |
| `separate_bins` | int | `20` | 扇形区间数 |
| `density` | bool | `True` | 是否归一化 |
| `geographic_orientation` | bool | `False` | 使用地理方向标签 (N, NE, ...) |
| `bridge_axis` | bool | `True` | 显示桥梁轴线 |
| `log_y` | bool | `False` | Y 轴对数坐标 |
| `top_n_density` | int | `3` | 标注 N 个最高密度区间 |
| `highlight_max_speed` | bool | `False` | 高亮最高平均风速区间 |

**返回值：** `(fig, ax)`

---

#### `rose_scatter()` - 极坐标散点图

```python
plot_lib.rose_scatter(theta, rho, title=None, xlabel=None, ylabel=None, 
                      xlim=None, ylim=None, dpi=None, fig=None, ax=None, 
                      s=None, marker=None, legend=None, color=None, 
                      colorbar=None, cmap=None, c_data=None, 
                      color_label=None, geographic_orientation=True, 
                      bridge_axis=True, norm=None, alpha=0.8, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `theta` | array-like | **必需** | 角度（弧度） |
| `rho` | array-like | **必需** | 半径 |
| `cmap` | str | `None` | 颜色映射 ('viridis', 'plasma', 'jet', ...) |
| `c_data` | array-like | `None` | 颜色数据 |
| `colorbar` | bool | `None` | 是否显示颜色条 |
| `color_label` | str | `None` | 颜色条标签 |
| `norm` | Normalize | `None` | matplotlib 颜色归一化对象 |
| `geographic_orientation` | bool | `True` | 使用地理方向标签 |
| `bridge_axis` | bool | `True` | 显示桥梁轴线 |
| 其他参数 | - | - | 同 `scatter()` |

**返回值：** `(fig, ax)`

---

#### `scatter_3d()` - 3D 散点图（柱坐标）

```python
plot_lib.scatter_3d(theta, rho, z, title=None, xlabel=None, ylabel=None, 
                    zlabel=None, xlim=None, ylim=None, dpi=None, 
                    fig=None, ax=None, marker=None, color=None, 
                    edgecolor=None, legend=None, s=None, 
                    alpha=0.5, add_fig=True)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `theta` | array-like | **必需** | 角度（弧度） |
| `rho` | array-like | **必需** | 半径 |
| `z` | array-like | **必需** | 高度 |
| `zlabel` | str | `None` | Z 轴标签 |
| `edgecolor` | str | `'none'` | 点边缘颜色 |
| 其他参数 | - | - | 同 `scatter()` |

**特殊功能：**
- 自动添加地理方向标签（N, NE, E, ...）
- 自动绘制柱坐标网格
- 自定义 Z 轴刻度

**返回值：** `(fig, ax)`

---

### 动画与展示

#### `animate()` - 生成动画

```python
plot_lib.animate(data_lis, color=None, alpha=0.7, title=None, 
                 labels=None, xlims=None, ylims=None, fps=None, 
                 save_path=None, dynamic_adjust=[(True, False), (False, False)])
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data_lis` | list of tuples | **必需** | `[(x_frames, y_frames), ...]` |
| - | - | - | `x_frames`, `y_frames` 形状: `(num_frames, num_points)` |
| `fps` | int | `None` | 帧率 |
| `save_path` | str | `None` | 保存路径 (`.gif` 或 `.mp4`) |
| `dynamic_adjust` | list of tuples | `[(True, False), ...]` | 动态调整坐标轴 `[(x_adjust, y_adjust), ...]` |
| `title` | list of str | `None` | 各子图标题 |
| `labels` | list of tuples | `None` | 坐标轴标签 |

**返回值：** `ani` - matplotlib Animation 对象

**注意：** 保存为 MP4 需要安装 `ffmpeg`

---

#### `show_sample()` - 信号时频分析

```python
plot_lib.show_sample(data, fs=50, nperseg=256, add_fig=True, scatter=False)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `data` | array-like | **必需** | 时域信号 |
| `fs` | float | `50` | 采样频率（Hz） |
| `nperseg` | int | `256` | Welch 方法窗口长度 |
| `scatter` | bool | `False` | 是否使用散点图 |
| `add_fig` | bool | `True` | 是否添加到图表列表 |

**功能：** 显示时域波形和功率谱密度（PSD）

**返回值：** `(fig, axes)`

---

#### `show()` - 显示所有图表

```python
plot_lib.show()
```

**功能：** 启动 `ChartApp` GUI，显示所有已创建的图表

**返回值：** 无

---

## ChartApp 类

### 构造函数

```python
ChartApp(root, figs)
```

| 参数 | 类型 | 描述 |
|------|------|------|
| `root` | Tkinter.Tk | Tkinter 根窗口 |
| `figs` | list | matplotlib Figure 对象列表 |

---

### 方法

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `show_previous()` | 无 | 无 | 显示上一张图表 |
| `show_next()` | 无 | 无 | 显示下一张图表 |
| `save_current_chart()` | 无 | 无 | 保存当前图表为 PNG |
| `update_chart()` | 无 | 无 | 更新显示的图表 |

---

## _Propose_Data_GUI 类

### 构造函数

```python
_Propose_Data_GUI(root, save_excel_root, default_img_root=None, image_list=[])
```

| 参数 | 类型 | 描述 |
|------|------|------|
| `root` | Tkinter.Tk | Tkinter 根窗口 |
| `save_excel_root` | str | Excel 保存路径 |
| `default_img_root` | str | 默认图像文件夹路径 |
| `image_list` | list | 图像路径列表（留空则弹出选择对话框） |

---

### 方法

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `next_image()` | `event=None` | 无 | 下一张图像 |
| `prev_image()` | `event=None` | 无 | 上一张图像 |
| `save_to_excel()` | 无 | 无 | 保存标注到 Excel |
| `load_existing_data()` | 无 | 无 | 加载已有标注数据 |
| `collect_images(folder_path)` | `folder_path: str` | 无 | 收集文件夹中的图像 |

---

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 下一张 |
| `Left Arrow` | 上一张 |
| `Ctrl+S` | 保存到 Excel |

---

## 全局配置

```python
GLOBAL_FONT_SIZE = 10  # 全局字体大小
plt.style.use('default')
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.size'] = GLOBAL_FONT_SIZE
```

---

## 常用颜色

| 颜色名称 | 示例 |
|----------|------|
| `'skyblue'` | 天蓝色 |
| `'coral'` | 珊瑚色 |
| `'steelblue'` | 钢蓝色 |
| `'darkblue'` | 深蓝色 |
| `'green'` | 绿色 |
| `'red'` | 红色 |
| `'pink'` | 粉色 |
| `'orange'` | 橙色 |
| `'purple'` | 紫色 |
| `'brown'` | 棕色 |

---

## 常用标记样式

| 标记符号 | 样式 |
|----------|------|
| `'o'` | 圆圈 |
| `'s'` | 正方形 |
| `'^'` | 三角形（上） |
| `'v'` | 三角形（下） |
| `'<'` | 三角形（左） |
| `'>'` | 三角形（右） |
| `'x'` | 叉号 |
| `'+'` | 加号 |
| `'*'` | 星号 |
| `'D'` | 菱形 |

---

## 常用线型

| 线型符号 | 样式 |
|----------|------|
| `'-'` | 实线 |
| `'--'` | 虚线 |
| `'-.'` | 点划线 |
| `':'` | 点线 |

---

## 常用颜色映射（cmap）

| 名称 | 描述 |
|------|------|
| `'viridis'` | 黄绿蓝渐变 |
| `'plasma'` | 紫红黄渐变 |
| `'inferno'` | 黑红黄渐变 |
| `'magma'` | 黑紫白渐变 |
| `'jet'` | 蓝青黄红渐变（经典） |
| `'coolwarm'` | 蓝白红渐变 |
| `'RdYlBu'` | 红黄蓝渐变 |

---

## 坐标系类型（coordinate_systems）

| 类型 | 描述 |
|------|------|
| `'linear'` | 线性坐标（默认） |
| `'loglog'` | 双对数坐标 |
| `'semilogy'` | Y 轴对数坐标 |

---

## 快速参考

### 最常用的 5 个方法

1. **`plot()`** - 绘制线图
2. **`scatter()`** - 绘制散点图
3. **`hist()`** - 绘制直方图
4. **`plots()`** - 绘制多子图
5. **`show()`** - 显示所有图表

---

### 典型工作流程

```python
from visualize_tools.utils import PlotLib
import numpy as np

# 1. 创建绘图对象
plot_lib = PlotLib()

# 2. 绘制图表
x = np.linspace(0, 10, 100)
plot_lib.plot(np.sin(x), x=x, title='Sine Wave')
plot_lib.scatter(x, np.random.randn(100), title='Random Scatter')

# 3. 显示
plot_lib.show()

# 4. (可选) 保存
for i, fig in enumerate(plot_lib.figs):
    fig.savefig(f'chart_{i}.png', dpi=300)
```

---

**查看更多示例：** [快速入门指南](QUICKSTART.md) | [完整文档](README.md)
