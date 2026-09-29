# Academic Figure Skills

两套用于学术示意图的 Codex skills：从参考图或方法描述生成可编辑 **Excalidraw**，并导出高清 **PNG、PDF、SVG**。

| Skill | 适用任务 | 布局偏好 |
|---|---|---|
| [motivation](skills/motivation/SKILL.md) | 动机、局限、设计理由与方法对比 | 紧凑对比，可纵向组织 |
| [method](skills/method/SKILL.md) | 方法架构、机制、数据流与训练流程 | 横向一体化、高信息密度，默认无明显步骤编号 |

## 使用

```bash
git clone https://github.com/Dhs2004/draw-skills-motivation_method.git
```

在 Codex 中提供参考图或方法描述，并指定 skill 的实际路径：

> 使用 /path/to/draw-skills-motivation_method/skills/method/SKILL.md，根据这张参考图生成横向、一体化、信息密度高的学术方法图，保存到指定目录，导出 Excalidraw、PNG 和 PDF。

绘制 motivation 图时改用 `skills/motivation/SKILL.md`。修改现有图时提供当前 `.excalidraw`，以保留手动调整。

## 视觉与内容规则

- 模块背景优先使用原生手绘斜线填充，浅色区分语义区域；保留黑灰框线、清楚的卡通字体和原色实体图标。
- 以 GRPO / Transformer 的信息密度为基准；通过分层调整字号、精简长句和收紧间距减少留白，避免堆叠数值表与重复说明。
- 根据实际问题调整布局或字号来减少空白，也可两者结合：重分配列宽与模块高度、收紧间距和画布，或适当放大文字；保持可读性与必要分组留白。
- 按实际语义寻找新图标，不局限于现有素材；矩阵、token、曲线和流程仍用原生工具。
- 公式逐条调整，只缩小明显偏大的具体公式；正常公式保持原尺寸，分式与上下标须可读。
- 保留科学含义；示意数据不是实验结果，不为填空白编造算法。
- 导出后查看整图与密集局部，检查字体、图文/连线遮挡和文件一致性。

## Motivation 示例

<table>
  <tr>
    <th width="50%">GRPO</th>
    <th width="50%">Transformer</th>
  </tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/grpo/motivation.png"><img src="skills/motivation/assets/grpo/motivation.png" alt="GRPO motivation" width="380"></a></td>
    <td align="center"><a href="skills/motivation/assets/transformer/motivation.png"><img src="skills/motivation/assets/transformer/motivation.png" alt="Transformer motivation" width="380"></a></td>
  </tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/grpo/motivation.excalidraw">可编辑源文件</a> · <a href="skills/motivation/assets/grpo/motivation.pdf">PDF</a></td>
    <td align="center"><a href="skills/motivation/assets/transformer/motivation.excalidraw">可编辑源文件</a> · <a href="skills/motivation/assets/transformer/motivation.pdf">PDF</a></td>
  </tr>
  <tr>
    <th>DAPO</th>
    <th>GiGPO</th>
  </tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/dapo/motivation.png"><img src="skills/motivation/assets/dapo/motivation.png" alt="DAPO motivation" width="380"></a></td>
    <td align="center"><a href="skills/motivation/assets/gigpo/motivation.png"><img src="skills/motivation/assets/gigpo/motivation.png" alt="GiGPO motivation" width="380"></a></td>
  </tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/dapo/motivation.excalidraw">可编辑源文件</a> · <a href="skills/motivation/assets/dapo/motivation.pdf">PDF</a></td>
    <td align="center"><a href="skills/motivation/assets/gigpo/motivation.excalidraw">可编辑源文件</a> · <a href="skills/motivation/assets/gigpo/motivation.pdf">PDF</a></td>
  </tr>
  <tr><th>PPO</th><th>PPO-Clip</th></tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/ppo/motivation.png"><img src="skills/motivation/assets/ppo/motivation.png" alt="PPO motivation" width="380"></a></td>
    <td>基于 <a href="https://arxiv.org/abs/1707.06347">PPO (2017)</a>：<ul><li>裁剪代理目标，限制过大变化的优化激励</li><li>同一批新数据执行多轮 mini-batch 更新</li><li>以一阶优化简化策略训练</li></ul>采用原始 actor–critic 场景，包含 GAE、价值拟合和可选熵奖励。<br><a href="skills/motivation/assets/ppo/README.md">示例说明与素材来源</a></td>
  </tr>
  <tr>
    <td align="center"><a href="skills/motivation/assets/ppo/motivation.excalidraw">可编辑源文件</a> · <a href="skills/motivation/assets/ppo/motivation.pdf">PDF</a></td><td></td>
  </tr>
</table>

## Method 示例

### GRPO

基于 [DeepSeekMath (2024)](https://arxiv.org/abs/2402.03300) 的结果奖励版 GRPO。

![GRPO method](skills/method/assets/grpo/method.png)

[可编辑源文件](skills/method/assets/grpo/method.excalidraw) · [PDF](skills/method/assets/grpo/method.pdf)

### Transformer

基于 [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) 的原始 encoder–decoder Transformer。

![Transformer method](skills/method/assets/transformer/method.png)

[可编辑源文件](skills/method/assets/transformer/method.excalidraw) · [PDF](skills/method/assets/transformer/method.pdf)

### DAPO

基于 [DAPO (2025)](https://arxiv.org/abs/2503.14476) 的横向一体化流程，包含动态筛选、组内优势、非对称裁剪、token 级损失和超长奖励塑形。

![DAPO method](skills/method/assets/dapo/method.png)

[可编辑源文件](skills/method/assets/dapo/method.excalidraw) · [PDF](skills/method/assets/dapo/method.pdf) · [公式源码](skills/method/assets/dapo/formulas) · [示例说明](skills/method/assets/dapo/README.md)

### GiGPO

基于 [Group-in-Group Policy Optimization (2025)](https://arxiv.org/abs/2505.10978)，展开多步环境交互、重复状态分组、两层优势与策略更新；以紧凑流程展示折扣回报与动作信用分配。

![GiGPO method](skills/method/assets/gigpo/method.png)

[可编辑源文件](skills/method/assets/gigpo/method.excalidraw) · [PDF](skills/method/assets/gigpo/method.pdf) · [公式源码](skills/method/assets/gigpo/formulas) · [示例说明](skills/method/assets/gigpo/README.md)

### PPO

基于 [Proximal Policy Optimization Algorithms (2017)](https://arxiv.org/abs/1707.06347) 的 PPO-Clip，展示 rollout、GAE、概率比率、多轮 mini-batch 更新，以及正负优势下的裁剪形状。

![PPO method](skills/method/assets/ppo/method.png)

[可编辑源文件](skills/method/assets/ppo/method.excalidraw) · [PDF](skills/method/assets/ppo/method.pdf) · [公式源码](skills/method/assets/ppo/formulas) · [示例说明](skills/method/assets/ppo/README.md)

示例均为公开论文的重新绘制，用于说明绘图风格。简化范围和素材来源见 [示例说明](skills/method/references/public-examples.md)。

## 运行与导出

需要 Node.js 18+、Chromium；新建 skeleton 时还需 Python 3。每套 skill 自带依赖清单及真实 Excalidraw 导出脚本。详细操作见 [渲染指南](skills/method/references/rendering.md)。

```bash
npm install --prefix skills/method/scripts/runtime
cd skills/method/scripts/runtime
npx playwright install chromium
```

在仓库根目录导出现有图：

```bash
node skills/method/scripts/export_scene.mjs \
  --input /path/to/figure.excalidraw \
  --out-prefix /path/to/output/figure
```

PNG 默认 3 倍像素尺寸并写入 300 dpi 元数据；PDF 为按画布尺寸生成的单页文件。复杂公式优先通过 LaTeX Live 渲染，保留 `.tex`；公式图片可移动缩放，字符修改后需重新渲染。

## 素材与授权

OpenMoji 素材保留 CC BY-SA 4.0 许可及来源记录。部分 Flaticon 素材的作者和具体出版/再分发许可尚未核实；本仓库不对第三方素材授予额外许可，正式发表或再分发须核实并按许可署名。详见各 skill 的素材说明与 `assets/icons`。
