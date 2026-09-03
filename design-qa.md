# Design QA — Project 03 活动运营IP联动

**Source visual truth**

- `docs/qa/project-05/02-project05-desktop.png` — 已确认的暖色报刊杂志风首屏，作为同站视觉体系参照。
- `废柴猫用户活动运营联动项目.pptx` 的 11 页内容与 10 张原始图片作为本页内容真相来源。

**Implementation evidence**

- `docs/qa/project-03/01-project03-desktop.png` — 桌面首屏，1426 × 891 px；CSS viewport 1440 × 900，density 1。
- `docs/qa/project-03/02-project03-mobile.png` — 手机首屏，375 × 844 px；CSS viewport 390 × 844，density 1。
- `docs/qa/project-03/03-project03-community.png` — 手机端社群轮播第 3 张与控件重点状态。
- `docs/qa/project-03/04-comparison.png` — Project 05 与 Project 03 同视口首屏并排对照。

**States and interactions checked**

- 返回作品集、8 个章节锚点及 11 个 PPT 对应内容段。
- 两组原位图片轮播：上一张、下一张、点击图片、左右方向键。
- 轮播计数通过 `aria-live="polite"` 更新；实测 `01 — 04 → 02 — 04 → 03 — 04`。
- 4 组证据图均可放大；Escape/关闭按钮关闭后恢复焦点。
- 390px 手机端页面无横向溢出，轮播控制重排为触控友好布局。
- 控制台无页面脚本错误；仅有共用 `assets/js/vendor.js` 的既有 Tailwind CDN 警告。

**Required fidelity surfaces**

- Fonts and typography: 延续大号中文衬线标题、等宽元数据和陶土红批注；桌面返回/导航约 19.45px，手机 16px，正文基准 16px，章节标记 14px。
- Spacing and layout rhythm: 12 栏编辑网格、细分隔线、大面积留白；桌面图文并置，移动端自然堆叠。
- Colors and tokens: 米沙纸色、深炭黑、主站深蓝、陶土红、淡黄高亮与 02/04/05 页面一致。
- Image quality and asset fidelity: 10 张图片全部来自 PPT 原始媒体，未使用占位图、CSS 绘图或生成图片；保持原比例并支持放大。
- Copy and content: 保留 42 万元、25.2 万元、16.8 万元、约 5 倍、18 天周期、四类用户路径和复盘不足；未引入外部数据。

**Findings and comparison history**

- First pass — P2: `data-carousel` 是空值布尔属性，初版脚本用 `dataset.carousel` 判断，导致轮播按钮不更新。Fix: 改为 `hasAttribute('data-carousel')`，并新增静态回归断言。Post-fix evidence: 按钮实测从 `01 — 04` 更新到 `02 — 04`，键盘右方向键更新至 `03 — 04`，放大弹层正常打开。
- Responsive pass — 无页面横向溢出；390px 下 document scrollWidth 375，小于 viewport 390。
- Full-view comparison — Project 03 与已确认 Project 05 使用相同的字体层级、米沙底色、深蓝/陶土红/淡黄令牌、细线网格和数据栏节奏；Project 03 的右侧原始活动图为内容差异。
- Focused comparison — 社群轮播控件及原始海报在 `03-project03-community.png` 中单独检查，按钮、计数和图片比例清晰。
- P3: 共用 `assets/js/vendor.js` 仍产生 Tailwind CDN 既有警告；不属于本次单页修改范围。
- Final comparison: 无未解决的 P0/P1/P2。

final result: passed
