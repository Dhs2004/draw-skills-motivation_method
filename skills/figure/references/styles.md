# 学术数据图风格

本页描述视觉规则。所附示例全部使用模拟数据，不代表任何真实方法的性能。

| 风格名称 | 核心特征 | 样例 |
|---|---|---|
| `triptych_cyan_orange_learning_efficiency` | 约 4–5:1 横向三联；青蓝／橙红对比；小圆／方标记；细虚线网格；透明误差带；中间面板可用曲线 + 淡色概率柱双轴 | [预览](../assets/examples/triptych_cyan_orange_learning_efficiency_preview.png) |
| `six_panel_serif_multimetric_dual_axis` | 2×3 面板；粗衬线标题；灰色六角／绿色菱形／红色三角；同列指标对齐；性能列用蓝方块与橙圆双轴；子图说明位于下缘 | [预览](../assets/examples/six_panel_serif_multimetric_dual_axis_preview.png) |
| `grouped_bar_blue_palette_hatched_baseline` | 约 2.5–3:1；四系列分组柱；蓝色深浅层次；基线细白斜纹；柱顶数值；横排上方图例；弱横网格；去除上／右边框 | [预览](../assets/examples/grouped_bar_blue_palette_hatched_baseline_preview.png) |

三联图的透明带在样例中表示 8 次模拟轨迹的均值 ± 1 SD。中间曲线是生成的响应率；柱子是独立生成 token 长度样本的概率质量，二者不是彼此的累积分布。两者应各自说明纵轴。

六宫格样例中的 share、concentration、margin、accuracy 是用于测试视觉布局的独立合成指标。上排长训练区间，下排短训练区间；不暗示训练预算一致或结果可公平比较。虚线阈值是示意设置，蓝线属于 margin 轴，橙线属于 accuracy 轴。

柱状图先将各任务基线定义为 100%，再生成其他系列的相对值；不是绝对交互次数。缺少原始实验基线时不可用这种样例数据代替真实归一化。

推荐从对应绘图函数修改：`plot_trip`、`plot_multi`、`plot_bars`。保留输入—处理—绘图之间的分离；新增风格时按参考调整函数，不强改不相关样例。

## 彩色外环雷达图

[预览](../assets/examples/annular_pastel_radar_preview.png) · [PNG](../assets/examples/annular_pastel_radar_synthetic.png) · [PDF](../assets/examples/annular_pastel_radar_synthetic.pdf) · [SVG](../assets/examples/annular_pastel_radar_synthetic.svg)

另有六种同级风格见 [雷达图设计变体](radar-design.md)，包括柔彩花环、宝石色弧环、青瓷双层环、极光渐变环、棱面彩环和极简彩带。

六维雷达图使用同向、可比较的指标；浅色外环只标识任务。红色主线与低饱和基线配合，透明填充保持克制，图例放于下方。

## 灰度纹理双面板柱状图

此类图包含三张同级样例：多任务分组对比、归一化指标对比和全连续纹理柱群。采用组内相接柱体，另有所有柱体连续无空隙的布局。见 [设计与生成说明](hatched-bars.md) 和 [三图总览](../assets/examples/hatched_bar_gallery_overview.png)。

## 透视归一化三维柱状图

[预览](../assets/examples/perspective_normalized_3d_bars_preview.png) · [PNG](../assets/examples/perspective_normalized_3d_bars_synthetic.png) · [PDF](../assets/examples/perspective_normalized_3d_bars_synthetic.pdf) · [SVG](../assets/examples/perspective_normalized_3d_bars_synthetic.svg)

三维分组柱以颜色区分指标，缩窄柱宽并提高观察仰角，避免遮住柱顶数值。本示例以各指标的最大值归一化柱高，柱顶显示原始分数；真实数据需明确归一化分母。标注绘制层级应保证完整可见。

## 分层半透明三维训练曲线

[预览](../assets/examples/perspective_3d_ribbon_dynamics_preview.png) · [PNG](../assets/examples/perspective_3d_ribbon_dynamics_synthetic.png) · [PDF](../assets/examples/perspective_3d_ribbon_dynamics_synthetic.pdf) · [SVG](../assets/examples/perspective_3d_ribbon_dynamics_synthetic.svg)

训练曲线沿类别轴分层，浅色透明立面落到零平面；它不是误差区间。缩短类别标签并调整投影间距，避免与训练步数末端刻度挤在一起。

## 四种几何风格的生成

上述四种风格参考 DEPPO 论文原 Figure 3、4、6、7 的视觉形式；示例全为合成数据，现按图表风格命名，不表示原论文结果。

[模拟数据](../assets/examples/geometric_styles_data.json) · [长表 CSV](../assets/examples/geometric_styles_values.csv)

```bash
python /path/to/figure/scripts/render_geometric_styles.py --out /path/to/output --data /path/to/figure/assets/examples/geometric_styles_data.json
```

固定随机种子为 20260930，输出四种风格的 PNG、PDF、SVG、预览与数据。运行不生成其他 DEPPO 实验图。
