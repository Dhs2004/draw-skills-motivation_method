# 三种可复用风格

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

参考 DEPPO 的雷达图、3D 图或训练／消融曲线时，转到 [DEPPO 实验图风格](deppo-experiments.md)。
