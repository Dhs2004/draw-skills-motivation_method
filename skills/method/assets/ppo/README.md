# PPO 示例说明

依据 Schulman et al., [Proximal Policy Optimization Algorithms (2017)](https://arxiv.org/abs/1707.06347)。本例采用 PPO-Clip actor–critic 流程；原生文字与框线可编辑，公式由 LaTeX Live 渲染并保留源码。

## 科学范围

论文 Sections 3、5、Figure 1、Algorithm 1 和 Eq. 7、9、11–12 是主要依据。主流程用旧策略采集新一批环境交互数据，固定旧 log-probabilities 和 rollout 时计算的优势/目标，在该批数据上执行 K 轮 shuffled mini-batch 优化，然后刷新旧策略并重新采样。PPO 的短期批内重用不同于无限期重放陈旧数据。

图中 GAE 使用 t=0,…,T−1 的明确索引：δ_t=r_t+γV(s_(t+1))−V(s_t)，Â_t=Σ_(l=0)^(T−1−t)(γλ)^l δ_(t+l)。此处 V 是采样阶段用于估计优势的 value baseline；真终止状态的后继 bootstrap 为零，时间截断是否 bootstrap 取决于终止语义。图中为紧凑起见没有展开 done/truncation masks。优势和 return targets 在各轮更新中视为固定。

概率比率记为 ρ_t，避免与奖励 r_t 混淆。裁剪目标取未裁剪项和裁剪项的较小者。正优势在高概率比率一侧出现平台，负优势在低概率比率一侧出现平台；这些是单样本 surrogate 的示意形状。它们不构成实际策略更新、概率比率或 KL 的硬边界，不保证单调性能提升。

联合目标以 J=L_CLIP−c_V E[(V_φ−R̂)^2]+c_H E[H(π_θ)] 表示最大化方向。策略与 value 参数可独立或共享；图中下标只用于区分角色，不规定网络共享方式。熵奖励是可选项；不同实验配置的系数可能为零。Return target 的具体构造可依据实现使用 bootstrapped/λ-return 等，不在主图中强行固定。

Motivation 对比的是普通 policy gradient 的更新风险、每批单次更新的低样本利用，以及 TRPO 约束求解的复杂度；不表示所有 policy-gradient 变体都只能单次更新，也不声称 PPO-Clip 拥有 TRPO 的完整理论保证。图中轨迹、曲线和 epoch 标签均为机制示意，不是实验测量。

## 建议英文图注

**Motivation.** PPO-Clip balances practical first-order optimization and repeated use of fresh interaction data by modifying the policy surrogate. Clipping reduces incentives for excessively large changes without imposing a hard bound on the realized policy update.

**Method.** An old-policy snapshot collects environment transitions. Rollout-time value estimates yield fixed GAE advantages and value targets. The actor and critic are optimized over several mini-batch epochs using a clipped surrogate, value fitting, and an optional entropy bonus; the old policy is then refreshed. The curves illustrate the single-sample surrogate for positive and negative advantages.

## 图标来源

使用现有 skill 的原色卡通图标，未做灰度化。OpenMoji contributors，CC BY-SA 4.0：https://openmoji.org/ 。具体下载来源、栅格化与裁剪说明及许可副本见 相邻的 `../icons/` 目录。

Flaticon 复用素材包括机器人 4712109、雪花 642000、书本 3534033、清单 2098402、天平 924954 等；CDN 模式为 `https://cdn-icons-png.flaticon.com/512/{floor(id/1000)}/{id}.png`。这些旧素材的作者和具体出版/再分发许可尚未完全核实；正式发表前应核实相关许可并署名。数学公式不属于第三方实体图标。

