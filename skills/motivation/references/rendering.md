# 实际生成和导出

## 运行环境

需要 Node.js 18+、Python 3（仅创建 skeleton 时）、Chromium。一次安装：

```bash
npm install --prefix "<skill>/scripts/runtime"
cd "<skill>/scripts/runtime"
npx playwright install chromium
```

也可复用已有依赖目录：`--runtime <包含 node_modules 的目录>`。该目录需有 package.json 和 Excalidraw、React、React DOM、esbuild、Playwright。不依赖固定的 /tmp 服务或其他项目路径。Playwright 浏览器可通过标准环境变量 PLAYWRIGHT_BROWSERS_PATH 或脚本参数 `--browser /path/to/chromium` 指定。缺少依赖时报告具体原因，不声称已经导出。

## 新建图

将 skill 的 scripts 目录加入 Python 导入路径，在本次工作目录编写构图脚本。一个最小示例：

```python
from scene_builder import Scene
s = Scene(480, 260)
s.text(24, 12, 'A compact academic figure', 26, width=432)
s.box(24, 62, 432, 174, stroke_width=2.2)
s.icon('/path/to/skill/assets/icons/robot.png', 42, 85, 64)
s.text(124, 82, 'Student', 24, width=300)
s.text(124, 124, 'Reward-aligned learning\nwith reliable guidance', 17, width=300)
s.line(124, 194, [[0, 0], [260, 0]], arrow=True)
s.save('/output/figure-scene.json')
```

```bash
PYTHONPATH="<skill>/scripts" python3 /output/build_figure.py
node "<skill>/scripts/export_scene.mjs" \
  --input /output/figure-scene.json --out-prefix /output/figure
```

Skeleton 测量使用实际 Comic Shanns 字体；文本超过 layoutWidth 时故意报错，必须合理断行/加宽，而不是静默缩成不可读的小字。字体先由 Excalidraw 按实际文本选择并嵌入子集，再加载至浏览器进行测量。中文可指定 font=5（Excalifont 会使用 Xiaolai 中文回退字体；英文正文仍默认 font=8）；导出后仍须检查字形覆盖，不能用英文测量器猜测中文宽度。

## 已有图 / 用户改过源文件

```bash
node "<skill>/scripts/export_scene.mjs" \
  --input /output/figure.excalidraw --out-prefix /output/figure
```

这一路径保留整个源文件，包括 appState、文本尺寸、用户改动和未删除元素；导出只显示未删除元素。不再运行旧 build_figure.py。脚本对输入做 SHA-256 记录并检查导出期间源文件没有变化，同路径不重写源文件。输出到不同 prefix 时，复制原始源文件字节。

用户要求调整图时先备份原始 `.excalidraw`，按组调整元素；更新内容时同时维护 text/originalText 和真实文本尺寸，不能只改 text 字符串。遇到绑定文本/箭头，检查 containerId、boundElements、startBinding/endBinding 关系，不套用只针对未绑定元素的坐标平移。不要随意更换元素 ID。

## 公式：LaTeX Live 渲染图片

用户已明确允许公式使用 https://www.latexlive.com/ 生成渲染图，替换分段原生文字公式。含分式、上下标、期望、集合和花体的复杂公式优先使用此方式；普通文字和简单标签仍使用原生文本。

1. 先忠实转录参考图中的 LaTeX，逐项检查大小写、索引、条件、括号和求和/最大化范围，不修正未经确认的科学记法。
2. 在浏览器进入网站公式编辑器，输入公式。当前源码输入框为 `#txta_input`，预览为 `mjx-container svg`；页面结构变化时重新检查，不能盲用选择器。
3. 等待本次输入实际渲染完成并确认没有 MathJax 错误，再使用网站导出或取得预览 SVG。取得预览 SVG 前检查它对应当前公式，而非上一次输入。不要通过“分享”发布内容。
4. 优先 SVG（路径字体、透明背景），保留完整 defs/路径及局部引用。规范 width/height 为像素、保留 viewBox、设置显式文字颜色，确保不依赖页面 CSS、外链字体或全局 glyph 缓存。需要 PNG 时另生成足够像素的透明图。
5. 每条公式同时保存 `.tex` 和 `.svg`，在图中按真实边界居中放置并留安全间距。作为 `mimeType: image/svg+xml` 的 data URL 写入 Excalidraw files，用 image 元素引用；原字符级公式元素先备份再替换，避免双重显示。可以在 image 的 customData 记录 LaTeX 和来源。
6. 检查导出后的分式、花体、上下标和小字号清晰度。公式是可移动/缩放的图片，字符编辑依靠保存的 `.tex` 重新渲染；交付时不能再声称每个公式字符均可直接编辑。

网站无法访问或渲染失败时可使用本地 TeX/MathJax 生成同等 SVG，并明确说明实际渲染来源，不伪称已使用 LaTeX Live。不要将 MathJax 输出图片和第三方实体图标混为同一授权来源。

## 导出产物

- `.excalidraw`：内嵌图标，原生文本/框线/箭头保持可编辑。
- `.svg`：实际 Excalidraw 导出，字体由库处理嵌入。
- `.pdf`：同一 SVG 在浏览器打印，页面按 SVG 实际尺寸，不套 A4；默认 8 px 外留白。
- `.png`：默认 3 倍尺寸，写入真实 pHYs 300 dpi 元数据；`--scale` 可改，不能用 dpi 声称分辨率提高。
- `_preview.png`：1 倍整体预览。
- `_report.json`：导出尺寸、元素/图标数量、源文件 hash、文字过小及图文相交警报。

每次改动后检查预览，密集区域放大看。PDF 要确认单页、无裁切，必要时用可用的 PDF 工具渲染验证。报告的相交警报需要人工视觉判断，旋转、透明边界和嵌套关系可能产生误报；没有警报也不意味着所有线条间距正确。

## 渲染踩坑

- 使用真正的 Excalidraw 库，不用自制 SVG 冒充 Excalidraw 手绘效果。
- 新建 skeleton 转換会再次居中文本，渲染器在转换后还原已量好的文本坐标；已有 canonical 文件绝不能再次转换。
- 原生 hachure 使用 `roughness=1, strokeWidth=1`；此前非整数参数组合曾导致斜线填充异常。未要求修改样式的现有文件不自动修正这些值。
- 高清 PNG 用 exportToBlob 的 `getDimensions` 同时返回放大后的 width、height 和 scale；单设 exportScale 曾未达到期望像素。
- SVG/PDF 尺寸来自导出结果，不是旧 viewport 常量。画布常使用锁定的白底矩形控制边界；多余的远处元素仍会扩大边界，需要在源文件中处理。
- 图标必须存在于 files 数据中，字体文件要能加载。不能靠本地缺失字体的浏览器 fallback 交付。
