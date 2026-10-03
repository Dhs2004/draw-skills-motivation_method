# Academic Figure Skills

**Create editable research diagrams and reproducible scientific plots with three Codex skills.**

[简体中文与完整示例](README.zh-CN.md) · [Quick start](#quick-start) · [Editable examples](#editable-examples) · [Export setup](#export-setup)

Turn a method description or a reference layout into an Excalidraw diagram, or turn supplied experiment data into a scientific plot. Keep the diagram source or plotting code so you can revise the figure after feedback.

![Editable GRPO method diagram](skills/method/assets/grpo/method.png)

[Open the editable Excalidraw source](skills/method/assets/grpo/method.excalidraw) · [View the PDF](skills/method/assets/grpo/method.pdf)

## Choose a skill

| You need | Skill | Editable output |
|---|---|---|
| Explain a research problem, limitation, or design motivation | [motivation](skills/motivation/SKILL.md) | Excalidraw scene, with PNG/PDF/SVG exports |
| Explain an architecture, mechanism, data flow, or training procedure | [method](skills/method/SKILL.md) | Excalidraw scene, with PNG/PDF/SVG exports |
| Plot experiment results or reproduce a reference chart's visual style | [figure](skills/figure/SKILL.md) | Plotting code and data, with PNG/PDF/SVG exports |

The diagram skills favor compact layouts and editable components. The plotting skill uses scientific plotting libraries and keeps data separate from styling. These are skill instructions and helper scripts for Codex, rather than a standalone drawing application.

## Quick start

### 1. Get the repository

```bash
git clone https://github.com/Dhs2004/draw-skills-motivation_method.git
cd draw-skills-motivation_method
```

### 2. Give Codex a skill path and your input

Replace `/absolute/path/to` with your local checkout location. Supply a method description, reference image, or data file alongside the prompt.

**Method diagram**

> Use /absolute/path/to/draw-skills-motivation_method/skills/method/SKILL.md. Draw a horizontal method diagram from the description I provide. Preserve the scientific meaning and use clearly labeled data flows. Save the editable Excalidraw scene and export PNG and PDF to ./outputs/method.

**Motivation diagram**

> Use /absolute/path/to/draw-skills-motivation_method/skills/motivation/SKILL.md. Make a compact comparison showing the limitation of the baseline and how my proposed approach addresses it. Use only the claims in my description. Save Excalidraw, PNG, and PDF to ./outputs/motivation.

**Experiment plot**

> Use /absolute/path/to/draw-skills-motivation_method/skills/figure/SKILL.md. Plot the experiment data I attach using the reference image's layout and visual style. Do not invent missing measurements. Export PNG, PDF, and SVG and retain the plotting code and data in ./outputs/figure.

For revisions, supply the existing `.excalidraw` file so manual edits can be preserved. Inspect the final export, including equations, labels, and arrow connections, before using it in a paper.

### 3. Try a plotting example without an agent

Requires Python 3. The command below replays bundled **synthetic example data**, not real benchmark results.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib
python skills/figure/scripts/render_examples.py \
  --out ./figure-output \
  --data skills/figure/assets/examples/synthetic_data.json
```

The `--data` option here expects this example script's JSON schema; it is not a general CSV importer. For your own dataset, use the figure skill with your data and describe the intended axes and metrics.

## Editable examples

The repository includes motivation and method diagrams for GRPO, Transformer, DAPO, GiGPO, PPO, and DEPPO. They are redrawings that illustrate the drawing workflow; see the example notes for simplifications and sources.

| Example | Motivation source | Method source | Method preview |
|---|---|---|---|
| GRPO | [Excalidraw](skills/motivation/assets/grpo/motivation.excalidraw) | [Excalidraw](skills/method/assets/grpo/method.excalidraw) | [PDF](skills/method/assets/grpo/method.pdf) |
| Transformer | [Excalidraw](skills/motivation/assets/transformer/motivation.excalidraw) | [Excalidraw](skills/method/assets/transformer/method.excalidraw) | [PDF](skills/method/assets/transformer/method.pdf) |
| DAPO | [Excalidraw](skills/motivation/assets/dapo/motivation.excalidraw) | [Excalidraw](skills/method/assets/dapo/method.excalidraw) | [PDF](skills/method/assets/dapo/method.pdf) |
| GiGPO | [Excalidraw](skills/motivation/assets/gigpo/motivation.excalidraw) | [Excalidraw](skills/method/assets/gigpo/method.excalidraw) | [PDF](skills/method/assets/gigpo/method.pdf) |
| PPO | [Excalidraw](skills/motivation/assets/ppo/motivation.excalidraw) | [Excalidraw](skills/method/assets/ppo/method.excalidraw) | [PDF](skills/method/assets/ppo/method.pdf) |
| DEPPO | [Excalidraw](skills/motivation/assets/deppo/motivation.excalidraw) | [Excalidraw](skills/method/assets/deppo/method.excalidraw) | [PDF](skills/method/assets/deppo/method.pdf) |

### Scientific plots

![Scientific plotting example using synthetic data](skills/figure/assets/examples/grouped_bar_blue_palette_hatched_baseline_preview.png)

[PNG](skills/figure/assets/examples/grouped_bar_blue_palette_hatched_baseline_synthetic.png) · [PDF](skills/figure/assets/examples/grouped_bar_blue_palette_hatched_baseline_synthetic.pdf) · [SVG](skills/figure/assets/examples/grouped_bar_blue_palette_hatched_baseline_synthetic.svg) · [Plotting code](skills/figure/scripts/render_examples.py)

Additional styles include multi-panel curves, dual-axis plots, radar charts, patterned bars, and 3D plots. The full [visual gallery](README.zh-CN.md#figure-数据图示例) includes downloadable outputs. Gallery experiment values are synthetic and must not be presented as measured research results.

## Export setup

For Excalidraw exports, the repository documents Node.js 18+, Chromium, and Python 3 for creating skeleton scenes. From the repository root:

```bash
npm install --prefix skills/method/scripts/runtime
(cd skills/method/scripts/runtime && npx playwright install chromium)
node skills/method/scripts/export_scene.mjs \
  --input skills/method/assets/grpo/method.excalidraw \
  --out-prefix ./figure-output/grpo-method
```

The subshell keeps your terminal at the repository root for the export command. See the [rendering guide](skills/method/references/rendering.md) for the complete workflow. The motivation skill also has its own runtime directory.

PNG exports default to 3× pixel dimensions with 300 dpi metadata; PDF exports use the scene's canvas size. Complex equations may be embedded as rendered images: they can be moved and resized, but editing their symbols requires changing the retained LaTeX source and rendering again.

## Scientific fidelity and asset permissions

- Provide actual measurements for experiment plots. Explicitly label synthetic data when using illustrative values.
- Review simplified diagrams against the source paper; drawing style does not establish scientific correctness.
- OpenMoji assets retain their CC BY-SA 4.0 terms and attribution records.
- Some Flaticon assets have not had their author and publication/redistribution permissions verified. Check the relevant asset records before publication or redistribution. This repository does not grant additional rights to third-party assets.
- The repository currently has no top-level license. Public availability alone does not establish a blanket reuse license; consult the maintainer for terms governing original code and instructions.

## Feedback

If a workflow fails, [open an issue](https://github.com/Dhs2004/draw-skills-motivation_method/issues) with the skill name, expected output, software versions, and a minimal non-confidential example. Suggestions for new diagram types and chart styles are welcome.

If these skills are useful in your research workflow, consider starring the repository so you can find it again.
