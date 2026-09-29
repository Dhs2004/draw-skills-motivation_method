# 公开论文示例与素材来源

## 论文范围

- GRPO：Shao et al., DeepSeekMath (2024)，https://arxiv.org/abs/2402.03300 。示例采用结果奖励版：同一问题的多回答奖励归一化、回答内共享 token 优势、裁剪代理目标和独立参考 KL 惩罚。优势分母中 δ 是明确标注的数值稳定项。示意答案与奖励不是实验数据。
- Transformer：Vaswani et al., Attention Is All You Need (2017)，https://arxiv.org/abs/1706.03762 。示例为原始 encoder–decoder、post-norm base 模型；省略 dropout、embedding 缩放和部分训练细节。因果矩阵是可见性示意而非注意力测量值。少量 head 的图示代表并行 head 的省略画法。

- DAPO：Yu et al., DAPO (2025)，https://arxiv.org/abs/2503.14476 。展示四项核心机制；目标函数显式标出有效 token 的损失屏蔽，示意组大小不代表论文配置。详见 [DAPO 示例说明](../assets/dapo/README.md)。

- GiGPO：Feng et al., Group-in-Group Policy Optimization for LLM Agent Training (2025)，https://arxiv.org/abs/2505.10978 。复用同一批轨迹中的重复状态，结合 episode 与 step 两层优势；轨迹为示意，非实验测量；method 聚焦核心流程，数值例子保留在补充说明。详见 [GiGPO 示例说明](../assets/gigpo/README.md)。

- PPO：Schulman et al., Proximal Policy Optimization Algorithms (2017)，https://arxiv.org/abs/1707.06347 。采用原始 PPO-Clip actor–critic 流程，含 GAE 和可选熵奖励；曲线仅展示单样本 surrogate 的形状，不代表实际更新的硬边界。详见 [PPO 示例说明](../assets/ppo/README.md)。

各 skill 的 assets/grpo、assets/transformer、assets/dapo、assets/gigpo 与 assets/ppo 包含相应 PNG 预览、PDF 和可编辑源文件；复杂公式的 .tex 与 SVG 保存在对应 formulas 目录。公式由 LaTeX Live 渲染，原生框线、文字与机制小图仍可编辑。示例来自公开论文的重新绘制，不表示论文作者背书。

## 实体图标

OpenMoji contributors，CC BY-SA 4.0：https://openmoji.org/ ，官方素材来源及具体编号见 assets/icons 中的 JSON 记录。处理包括透明边距裁剪与栅格化；保留许可副本 OpenMoji-LICENSE.txt，并按许可保留署名及修改说明。

复用 Flaticon 的机器人、雪花、书本、奖杯、天平、锁等素材；作者和具体出版/再分发许可尚未完全核实。部分素材已有配色或描边适配。本仓库不授予这些第三方素材额外权利，正式发表或再分发须核实具体许可。公式图不属于第三方实体图标来源。
