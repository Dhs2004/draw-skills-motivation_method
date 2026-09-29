# DEPPO 实验图风格

用于复用用户提供的 DEPPO 论文 Figure 3–14 的实验图风格。以下参考预览是重新生成的模拟数据图，不是论文结果，也不涉及机器人、奖杯等实体小图标。原始论文中的实验结论不能从这些示例推出。

| 论文图号 | 风格与布局 | 模拟参考图 |
|---|---|---|
| 3 | 六维雷达图；彩色外环划分任务；红色主线、低饱和基线、轻填充；下方共享图例 | [雷达图](../assets/examples/deppo/deppo_fig03_annular_pastel_radar_preview.png) |
| 4 | 两面板灰度／米色柱状图；每根柱子不同纹理；顶部数值；左上任务标签 | [任务比较](../assets/examples/deppo/deppo_fig04_paired_grayscale_hatched_bars_preview.png) |
| 5 | 与任务比较相同视觉语言；两个面板对应不同模型骨干；首柱为基础模型 | [骨干比较](../assets/examples/deppo/deppo_fig05_paired_backbone_hatched_bars_preview.png) |
| 6 | 3D 分组柱；指标对应低饱和颜色；透视角度清楚；柱顶显示原值；高度经过明确归一化 | [参数敏感性](../assets/examples/deppo/deppo_fig06_perspective_normalized_3d_bars_preview.png) |
| 7 | 三条训练曲线沿类别轴分层；曲线下透明带回落至零平面；弱三维网格 | [3D 动态](../assets/examples/deppo/deppo_fig07_perspective_3d_ribbon_dynamics_preview.png) |
| 8 | 红蓝双曲线、透明零基线填充、允许负值、虚线零参考线 | [偏好与权重动态](../assets/examples/deppo/deppo_fig08_dual_line_translucent_area_preview.png) |
| 9 | 红蓝颜色区分模型规模，实虚线区分成功／失败池；顶部两列图例 | [任务计数](../assets/examples/deppo/deppo_fig09_dual_pool_task_count_lines_preview.png) |
| 10 | 与任务计数同一颜色和线型编码；计数轴可用 k 缩写 | [状态计数](../assets/examples/deppo/deppo_fig10_dual_pool_state_count_lines_preview.png) |
| 11 | 紧凑 2×3 任务分面；共享轴范围和图例；蓝橙红细曲线；任务名在轴内左上 | [多任务收敛](../assets/examples/deppo/deppo_fig11_six_panel_shared_legend_learning_preview.png) |
| 12 | 1×2 训练诊断；响应长度与熵损失分轴显示；方法配色一致、顶部共享图例 | [长度与熵](../assets/examples/deppo/deppo_fig12_paired_response_entropy_lines_preview.png) |
| 13 | 红蓝过滤消融曲线；成功率使用统一 0–1 范围；图例独立置顶 | [消融比较](../assets/examples/deppo/deppo_fig13_filtering_ablation_lines_preview.png) |
| 14 | 2×2 训练内部统计；统一横轴，各面板保留实际纵轴量纲；顶部共享图例 | [塑形诊断](../assets/examples/deppo/deppo_fig14_four_panel_shaping_diagnostics_preview.png) |

## 复用时保留的关键关系

- Figure 3：各辐条需要同向指标和可比尺度。示例使用 0–100；真实量纲不同必须明确规范化规则，不能直接混用。外环仅标识任务，不编码额外数值。
- Figure 4–5：柱形从零开始；纹理与数值标签提高灰度打印辨识度。避免旋转标签与论文图注互相挤压。
- Figure 6：本示例按**每个指标在各参数设置下的最大值**归一化柱高，柱顶文字显示原始合成分数。此规则用于清楚演示透视与归一化，不声称复原原图内部归一化方式。真实数据需根据实验定义确定分母，注明后再画。视角、绘制顺序与柱宽应避免遮挡；读精确差值时可以额外给出 2D 图。
- Figure 7：透明立面是曲线到零平面的填充，不是误差区间。类别轴名称应能完整阅读，避免文字和 step 标签在 3D 投影后重叠。
- Figure 8：零基线填充不是不确定性，负值不得静默裁为零。本文示例两条曲线是独立生成的信号，只展示样式。
- Figure 9–10：颜色表示模型规模，实线／虚线表示池类型，图例必须表达这两个独立因素。示例生成了单调计数作为演示；真实包含衰减或剪枝的数据不应强制单调化。
- Figure 11–14：共享图例减少重复；同一方法在各图保留一致颜色。各面板单位不同则不强行统一纵轴。原始锯齿、平滑曲线与统计置信带应明确区分；本示例只对生成噪声作局部平均，不代表真实训练平滑策略。

## 本地生成

```bash
python /path/to/figure/scripts/render_deppo_examples.py --out /path/to/retry/deppo --seed 20260930
python /path/to/figure/scripts/render_deppo_examples.py --out /path/to/replay --data /path/to/retry/deppo/synthetic_data.json
```

脚本生成 12 张图的 PNG（300 dpi）、单页 PDF、SVG、预览，以及 JSON 与长表 CSV。CSV 使用数组名和从零开始的层级索引，可精确追溯每个绘制数值。数据全部来自固定随机种子的合成过程；真实实验任务需要替换数据读取逻辑与来源说明，不能只删掉 `SYNTHETIC DATA` 标签。
