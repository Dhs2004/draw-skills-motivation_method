# DEPPO 实验图风格复绘

本目录对应 DEPPO 论文的 **Figure 3–14，共 12 张实验图**。全部使用随机种子 `20260930` 生成的模拟数据，未复用论文数值，不能作为实验结果。

文件名包含原论文图号和风格类型。每张提供 PNG（300 dpi）、单页矢量 PDF、SVG 和 `_preview.png`。`synthetic_data.json` 保存全部数据，`synthetic_values.csv` 为长表，索引从零开始。绘图脚本位于 `../../../scripts/render_deppo_examples.py`，可独立运行（NumPy、Matplotlib）。

```bash
python ../../../scripts/render_deppo_examples.py --out reproduced --data synthetic_data.json
```

雷达图采用统一 0–100 量程，外环颜色仅区分任务。3D 柱状图按每个指标的最大值归一化高度，柱顶显示原始模拟值；不声称复原原论文未明确的数据处理。3D 曲线立面与双曲线的填充均连接到零平面，不是误差带。训练曲线中的局部噪声来自合成过程，不代表实际种子间方差。

图表是可复用风格示例，配套的 figure skill 说明各类图的布局、配色、坐标轴、归一化和标注规则。
