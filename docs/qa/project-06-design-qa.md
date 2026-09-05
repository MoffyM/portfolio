# Design QA — Project 06 汉字数字化创作

**Source visual truth**

- `docs/qa/project-05/02-project05-desktop.png` — 已确认的暖色编辑风首屏，作为同站视觉体系参照。
- 用户提供的明信片、演讲、证书、社媒截图、MP4 与 13 页原始 PPT 为作品内容真相来源。

**Implementation evidence**

- `docs/qa/project-06/01-project06-desktop.png` — 桌面首屏，1426 × 891 px；CSS viewport 1440 × 900，density 1。
- `docs/qa/project-06/02-project06-mobile.png` — 手机首屏，375 × 844 px；CSS viewport 390 × 844，density 1。
- `docs/qa/project-06/03-project06-deck.png` — 手机端 PPT 第 3/13 页及轮播控件状态。
- `docs/qa/project-06/04-comparison.png` — Project 05 与 Project 06 同视口首屏并排对照。

**States and interactions checked**

- 六个视觉章节、返回作品集及六个章节锚点。
- 原生 MP4 元数据成功加载，视频源为 `assets/video/project-06-animation.mp4`。
- 四组轮播：明信片、演讲、社媒、13 页 PPT；按钮、点击图片和左右方向键均可切换。
- PPT 轮播实测 `01 — 13 → 02 — 13 → 03 — 13`，放大弹层正常开启与关闭。
- 390px 手机端无整页横向溢出；轮播按钮和页尾均适配窄屏。
- 控制台无页面脚本错误；仅有共用 `assets/js/vendor.js` 的既有 Tailwind CDN 警告。

**Required fidelity surfaces**

- Fonts and typography: 延续中文衬线展示字体与等宽元数据；桌面返回/导航约 19.45px，手机 16px，正文基准 16px，章节标记 14px。
- Spacing and layout rhythm: 延续 12 栏编辑网格、细分隔线和大面积留白；作品图像获得高于文字的视觉权重。
- Colors and tokens: 保留米沙纸色、深炭黑与主站深蓝，并从作品提取松绿色和嫩绿色作为项目专属强调色。
- Image quality and asset fidelity: 所有照片、证书和社媒截图均为用户原始文件；PPT 13 页以 1600 × 900 PNG 原样导出；动画保留原始 MP4，未转换为有损 GIF。
- Copy and content: 六段内涵盖独立 Blender 创作、英文演讲、优秀创作者认可、项目宣发与作品送展台湾；文字保持简洁，不新增外部数据。

**Findings and comparison history**

- First responsive pass — P2: 手机端页尾项目编号与英文说明距离过近。Fix: 页尾允许换行并设置 12px 间距、18px 上下内边距与 250px 文本宽度。Post-fix evidence: `03-project06-deck.png`，页尾高度 85px，页面 scrollWidth 375。
- Full-view comparison: Project 06 与已确认 Project 05 保持相同导航尺度、编辑网格和纸张底色；项目专属绿色来自作品本身，属于有意内容映射。
- Focused comparison: `03-project06-deck.png` 单独检查 PPT 原图比例、页码、按钮和深色展陈区域，内容清晰且无裁切。
- P3: 浏览器公共运行时仍报告 Tailwind CDN 既有警告，不属于本次单页范围。
- Final comparison: 无未解决的 P0/P1/P2。

final result: passed
