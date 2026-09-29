# 归一化三维柱状图：九种清晰视角

使用同一份 4×4 模拟分数，固定参数设置顺序和指标顺序，比较九种排距、柱体比例、配色与观察方向。README 中统一为一类图，按三行三列展示；不是九组实验。

[九图总览](../assets/examples/normalized_3d_bar_gallery_overview.png) · [原值与规则](../assets/examples/normalized_3d_bar_data.json) · [CSV](../assets/examples/normalized_3d_bar_data.csv)

| 文件后缀 | 名称 | 视觉特点 |
|---|---|---|
| balanced_isometric | 均衡轴测 | 中等斜角与舒展的层间距，四排关系清楚 |
| frontal_oblique | 正面斜投影 | 横轴水平，数值比较更直观 |
| elevated_grid | 高位网格 | 较高俯视感与紧凑柱高，展示分组平面 |
| architectural | 建筑式层列 | 较小横向偏斜，行列组织规整 |
| wide_isometric | 宽幅轴测 | 横向展开，纵深方向更明显 |
| terraced_rows | 阶梯分层 | 各排接近水平，便于逐行阅读 |
| compact_parallel | 紧凑平行投影 | 保留纵深，同时压缩整体占用 |
| porcelain_perspective | 青瓷轴测 | 浅色柱体与弱底面，线条轻、层次清楚 |
| slate_copper | 石板铜色 | 冷灰蓝与暖铜色组合，保持低饱和度 |

## 几何与数据含义

- 新样例使用**轴测／斜平行投影**，不是近大远小的中心透视。每个 3D 点以 `p = x*bx + y*by + z*bz` 投影。位置改变不会缩放同样数值的柱体，同图所有柱子的垂直单位长度一致。
- 柱高为 `raw_score / max(raw_score over settings for this metric)`；柱顶标签显示原始分数。四个指标分别归一化，不能把同样柱高解释为同样原始分数。保留明确说明及 CSV 中的 normalized_height。
- 每种设计可以调整三维基向量及地面间距，但数据顺序、归一化分母、单图共同 z 比例均不改变。前后柱体保持相同底面尺寸，不用透视大小强化某种方法。
- 宽而适度矮的柱体比细高柱更容易看清。先根据最大归一化高度设定排距，避免前排柱体覆盖后排柱顶；不能只靠把数值标签强制浮到前景掩盖遮挡问题。
- 从远排向近排绘制可见面，正面、侧面、顶面用同一指标色的明暗层次；深浅表示面朝向，不表示额外数据。
- 每排使用弱底色条和零基线，替代厚重的封闭三维网格。指标名置于该排末端，横轴标题放在所有参数刻度之下，不能按轴中点投影后直接压到最右侧刻度。
- 标签贴近柱顶，保留白底与安全距离；共同归一化刻度位于前方，图内明确注明“高度为归一化值、标签为原值”。
- 需要精确读数时交付 CSV；3D 不能取代合理的统计定义。真实数据包含负值或零分母时，应重新设计轴与归一化，不能套用本正值示范脚本。

## 生成与检查

```bash
python /path/to/figure/scripts/render_3d_bar_gallery.py \
  --data /path/to/figure/assets/examples/normalized_3d_bar_data.json \
  --out /path/to/3d-bar-gallery
```

依赖 NumPy、Matplotlib、Pillow。输入带 `synthetic: true` 和 `sensitivity` 正值 4×4 数组。输出 360 dpi PNG、单页矢量 PDF、SVG、预览、总览、JSON 与 CSV。保存前检查文本矩形是否相交，再看整体与 PDF，重点检查最远排标注、横轴末端和归一化轴。
