# GiGPO 示例说明

依据 Feng et al., [Group-in-Group Policy Optimization for LLM Agent Training (2025)](https://arxiv.org/abs/2505.10978)。公式通过 LaTeX Live 渲染，原生图形与文字可编辑。

## 科学含义与简化范围

依据论文 Sections 4.1–4.3、Figure 3 和 Appendix D。图中使用主方法的相同环境状态匹配；没有将同一时间下标当成匹配条件，也没有引入新 rollout。论文还讨论了相似度匹配变体，本图没有展开该变体。

- 同一任务与初始环境状态下，收集 N 条轨迹。Episode return E_i 是奖励之和，episode advantage 在该轨迹组内中心化，并除以 F_E。
- 为每个重复状态 S 收集出现位置 I(S)={(i,t):s_t^(i)=S}，允许跨轨迹和同一轨迹不同时间出现。动作与观测结果来自已收集轨迹。
- Q_(i,t) 是从当前位置开始的折扣回报，即论文中的 R_t^(i)，不是即时奖励，也不是学习得到的 critic。Step advantage 在 I(S) 对应的回报集合内中心化和归一化。
- F 可取该组标准差或 1。单例组不提供局部对比；std 归一化的零方差情形需实现中的数值保护，不能直接除以零。
- 融合 A_(i,t)=A_i^E+ωA_(i,t)^S，并用于裁剪策略目标。旧策略定义重要性比率，独立参考策略定义 KL 锚点。这两个角色不同；GiGPO 不训练额外的价值 critic。
- 目标函数按论文的 action-level 表达；为节省空间省略了外层采样期望和 KL 的条件变量，保留相同 T 下的 1/(NT) 记法。本图没有替换为 DAPO 的非对称裁剪或 token 长度加权。

### 补充数值例子（精简版图中未展开）

这是为了可读性构造的示意例子，借鉴论文 Figure 3 的行为模式，不是实验测量，也不是论文实际奖励或超参数配置。

使用 N=2、T=3、γ=0.9、ω=1、F=1，仅在成功轨迹最后一步给奖励 1，失败轨迹给 0；失败轨迹的 end / — 是对终止后零奖励位置的示意。成功轨迹先在 S 选择 2nd item，返回 S 后选择 1st item；失败轨迹在 S 选择 next page。

S 组的三个折扣回报为 [0.81,1,0]，均值 1.81/3=0.603333…。Episode advantages 为 [+0.5,−0.5]；step advantages 为 [+0.206667,+0.396667,−0.603333]；combined advantages 为 [+0.706667,+0.896667,−1.103333]。详细数值示例显示两位小数，因此对已四舍五入的单元格求和可能出现 0.01 的舍入差。

该例特别保留“绕路动作仍可能有正优势”：GiGPO 提供相对排序，不保证每个不理想动作都被赋予负值。正文关于未来回报的表述不是因果识别保证。

实际 ALFWorld/WebShop 实验使用 N=8、γ=0.95、ω=1，成功奖励与无效动作罚分等设置见 Appendix E.1；图中没有混用这些实验数值。

## 建议英文图注

**Motivation.** Episode-level rewards blur the contributions of individual decisions in multi-turn agent tasks. GiGPO reuses recurring states within a shared trajectory group to obtain local action comparisons without additional per-state rollouts, combining these signals with episode-level credit.

**Method.** GiGPO collects trajectories under identical tasks and initial states, computes episode-relative advantages, and groups matching state occurrences across trajectories and time steps for discounted-return comparisons. Global and local advantages are fused for clipped policy optimization with a reference KL term. The two trajectories are schematic; the figure emphasizes the main grouping and optimization mechanisms.

## 图标来源

OpenMoji contributors，CC BY-SA 4.0，https://openmoji.org/ 。本次新增 anchor、cart、repeat、search；实际 URL 及裁剪/栅格化记录见 `icon-sources.json`，许可副本与复用素材记录在相邻的 `../icons/` 目录保留。未对新图标改色。

复用 skill 的 Flaticon 机器人 (4712109)、雪花 (642000)、清单 (2098402)、奖杯 (3112946)、天平 (924954) 等。CDN URL 模式为 `https://cdn-icons-png.flaticon.com/512/{floor(id/1000)}/{id}.png`。部分旧素材的作者、具体出版许可和修改来源尚未完全核实，不能据此宣称免署名或自由出版；正式发表应核实对应素材许可。图标授权不适用于本地生成的公式图片。


当前 method 已参考 GRPO / Transformer 的信息密度简化：省略逐项数值表、形式化状态集合与重复说明，保留轨迹、两层优势和带 KL 的策略目标。
