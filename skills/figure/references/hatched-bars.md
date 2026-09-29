# 灰度纹理多指标柱状图

此类图统一展示六张样例，在 README 中按两行三列排列，不另分“原版”和“变体”。支持多个指标、多任务、多方法对比。所有示例使用同一份模拟数据，四种方法、三个任务、四个指标（成功率、F1、延迟、成本）。

| 文件后缀 | 名称 | 用途 |
|---|---|---|
| paired_metrics | 双指标紧密对比 | 两个指标各占一面板；展示跨任务均值 |
| grouped_tasks | 多任务分组对比 | 每个任务是一组，组内方法柱相接，组间保留小间距 |
| four_metric_facets | 多指标分面对比 | 四指标分面，单位与优化方向分别标注 |
| continuous_blocks | 全连续纹理柱群 | 柱间、组间均无空隙，用细分隔线和任务标签划组 |
| horizontal_metrics | 横向多指标对比 | 柱条纵向紧密相接，长指标名放横轴 |
| normalized_metrics | 归一化指标对比 | 各指标分别除以 Base 的跨任务均值并乘 100，再分组对比 |

[总览](../assets/examples/hatched_bar_gallery_overview.png) · [数据](../assets/examples/hatched_bar_data.json) · [CSV](../assets/examples/hatched_bar_data.csv)

## 柱间零间距

- 竖柱中心步长等于柱宽，例如中心为 `0, 1, 2, 3`，`width=1`；横柱用相同关系约束 y 中心与 `height`。不以白色粗边框模拟间距。
- 同组柱子以细深灰边界和不同纹理区分；推荐线宽 0.5–0.7，hatch 不宜过密。纹理和灰度在各面板内保持一致。
- 用户要求所有柱子无空隙时，把任务组之间的偏移也设为零，用组边界线与刻度标签标识；“组内零间距”与“整条柱群零间距”须明确区别。
- 避免相接柱体掩盖类别身份。共享图例必须与顺序、灰度及纹理一致；空白不得靠错误拼接不相关指标消除。

## 多指标表达

- 同单位也不自动相加；成功率、F1、延迟、成本不能堆叠为一个总量。
- 默认各指标分面且从零起始，分别注明单位与 ↑／↓。多指标可以共用方法图例，但不得共用不兼容的纵轴范围。
- 需要放在同一数值尺度时，说明归一化分母、聚合顺序和优化方向。本例先对任务等权取均值，再按该指标 Base 的均值归一化；延迟与成本仍然越低越好，不因归一化就变成高者优。
- 柱顶数值精度统一。密集分组可以不显示逐柱数字，完整数值保留 CSV；不缩小到不可读，也不伪造误差线。
- 当前脚本是四指标布局示范，可按实际指标数调整分面和选择索引；不把此示例的指标数量写成通用绘图限制。真实数据应替换数据读取与来源标注，不能只移除模拟标签。

## 生成

```bash
python /path/to/figure/scripts/render_hatched_bars.py --out /path/to/bar-gallery --seed 20261001
python /path/to/figure/scripts/render_hatched_bars.py --out /path/to/replay --data /path/to/figure/assets/examples/hatched_bar_data.json
```

依赖 NumPy、Matplotlib 和 Pillow。输出 360 dpi PNG、单页矢量 PDF、SVG、预览、JSON 与长表 CSV。数据 schema 为 `tasks × methods × metrics`，指标元数据包括名称、单位和方向。示例保留灰／米色纹理风格；真实任务可在用户要求下扩展配色，但不能把灰度样式自动改成高饱和配色。
