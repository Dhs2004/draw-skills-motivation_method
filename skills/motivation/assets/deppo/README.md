# DEPPO 示例说明

依据 **DEPPO: Dual Experience Pool Policy Optimization for Long-Horizon Reinforcement Learning**（已接收，作者提供的论文版本）。展示 task-conditioned 双经验池、门控优势重加权与不对称经验更新。

## 科学含义与简化

DEPPO 的基础优势来自论文指定的 **GiGPO state-aware group-based optimization**；不是 PPO actor–critic GAE，也没有额外引入 critic、PRM 或参考策略 KL 项。主图只展示论文 Eq. (9) 的训练目标。

双池 D+ / D− 存储 **task → state → action statistics**。任务索引 u 必须保留；相同状态在不同任务下不会混为一项。P± 是加性平滑后的经验概率，不是两个额外的神经网络。共享动作集合是两个池在当前任务—状态下已出现动作的并集，再加入当前动作。N± 是对应动作计数之和。

门控 g_t 同时要求：总支持数不少于 S_min、两个池各自的支持数不少于 S_min_each，以及 |Δ_t| 不小于 τ_Δ。门控关闭时权重为 1，保留基础优势，不丢弃当前样本。Δ_t = log[(P+ + ε)/(P− + ε)] 是关联证据，不是因果贡献或正确性的保证。

成功轨迹 y_i=+1，失败轨迹 y_i=−1。权重为 clip(exp(β y_i Δ_t), w_min, w_max) 的 g_t 次方，乘到基础优势 A_i,t 上。正权重改变优势幅度而不改变符号。不能将“成功关联”简单画成对所有轨迹一律放大：对于失败轨迹，成功关联动作的权重反而减小。具体梯度方向还取决于原始优势的符号。Motivation 中 +R/−R 是论文所讨论的终局回报广播示意，不表示 GiGPO 的每一步优势都相同。

**严格时序：查询历史池 → 优势重加权 → 策略优化 → 当前批次写入 → 后续批次查询。** 避免当前轨迹先写入后查询自身。实线表示当前批次的数据／优化流程，虚线表示历史经验反馈。

成功池偏向尚未充分表示的成功动作，写入权重由 P+ 与 freshness threshold η 决定。失败池加权强调重复失败、无效动作和靠近失败终点的动作。主图用短说明替代 Eq. (10)–(13) 的完整展开，不新增手工标注环节。周期性指数衰减后，删除低计数动作和低总计数状态；限制每个状态动作数与每个任务状态数，超限时优先移除低支持且陈旧的状态。详见论文 Eq. (14)–(16)。

不展示未经复核的实验数值。轨迹、符号和机制均为说明性示意，不是测量结果。

## 英文图注

**Motivation.** Broadcasting terminal outcomes can over-reinforce redundant actions in successful trajectories and penalize useful actions in failed ones. DEPPO contrasts historical success and failure statistics under the same task–state context, applying outcome-aware advantage rescaling only when sufficient evidence is available.

**Method.** DEPPO queries task-conditioned dual experience pools to compute smoothed action likelihoods and a success–failure log preference. A support-aware gate controls outcome-aware rescaling of the GiGPO base advantage, which is used in a PPO-style clipped objective. After policy optimization, the current batch updates the pools asymmetrically through freshness-aware success insertion and risk-aware failure insertion. Decay and pruning keep the memory bounded and adaptive.

## 素材与编辑

新增 OpenMoji 图标的来源、作者、CC BY-SA 4.0 许可及修改记录见 [icon-sources.json](icon-sources.json) 与 [许可副本](OpenMoji-LICENSE.txt)。复用图标来源见相邻 `../icons/` 目录。Flaticon 素材的具体出版许可状态沿用仓库素材说明。

原生文字、框线、箭头和斜线填充可编辑；复杂公式为 LaTeX Live 渲染的 SVG，源码位于 method 示例的 `formulas/` 目录。PNG 为 3 倍像素、300 dpi，PDF 为单页。
