# Design QA — Project 05 毕业项目网站成果

**Source visual truth**

- `docs/qa/project-05/01-project04-visual-reference.png` — 已验收的 Project 04 页面视觉方向，1440 × 900。
- 新 PPT 的 6 页信息结构、文字与 12 张原始证据图作为内容真相来源。

**Implementation evidence**

- `docs/qa/project-05/02-project05-desktop.png` — 1440 × 900，CSS viewport 1440 × 900，device density 1。
- `docs/qa/project-05/03-project05-mobile-390.png` — 390 × 844，CSS viewport 390 × 844，device density 1。
- `docs/qa/project-05/04-carousel-mobile.png` — 手机端轮播控件重点状态。
- `docs/qa/project-05/05-comparison.png` — Project 04 与 Project 05 同视口首屏并排对照。

**State and interactions checked**

- 首屏默认状态、章节锚点导航、返回作品集链接。
- 3 组原位图片轮播：上一张、下一张、点击图片、左右方向键。
- 当前图片计数通过 `aria-live="polite"` 更新。
- 当前图片可放大，Escape 关闭后焦点返回触发按钮。
- 390px 手机端无横向溢出，轮播控件重排为触控友好布局。

**Required fidelity surfaces**

- Fonts and typography: 延续 04 的大号中文衬线标题、等宽元数据和手写批注；层级、字重、换行均清晰。
- Spacing and layout rhythm: 延续 12 栏编辑网格、细分隔线和大面积留白；桌面与手机端比例稳定。
- Colors and tokens: 米沙纸色、深炭黑、主站深蓝、陶土红与淡黄高亮映射一致。
- Image quality and asset fidelity: 12 张图片均直接取自 PPT 原始媒体，不使用占位图或代码绘图；证据图保持原比例与可放大阅读。
- Copy and content: 6 个章节对应 PPT 6 页叙事，保留 5 类口音、15 个样本、10 次部署及用户反馈等原始事实；未引入外部数据。

**Findings and comparison history**

- First pass — P2: 轮播计数使用 `01 / 04`，会与站点页码测试产生歧义。Fix: 改为 `01 — 04`，保留清晰状态表达。Post-fix evidence: 自动化测试通过，轮播状态正确更新。
- First pass — P2: 手机端章节结构较长，需要确认轮播按钮不会溢出。Fix: 390px 下改为两列控制按钮、状态与放大按钮独占整行。Post-fix evidence: `04-carousel-mobile.png`，页面 scrollWidth 375 小于 viewport 390。
- Final comparison: 无未解决的 P0/P1/P2。Project 05 在保持 04 视觉系统的同时，用 0→1、二维码和学习产品数据形成自己的信息重点。
- P3: 共用 `assets/js/vendor.js` 仍产生 Tailwind CDN 的既有警告；该文件属于全站公共运行时，不在本次单页修改范围。

**Focused comparison**

轮播控件与证据图是本页新增的关键交互，已用 `04-carousel-mobile.png` 单独检查。桌面首屏的字体、网格、色彩与 04 通过 `05-comparison.png` 对照。

final result: passed
