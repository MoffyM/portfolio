# Design QA — Project 02 用户召回策略

**Source visual truth**

- `docs/qa/project-05/02-project05-desktop.png` — 已验收的 Project 04/05 暖色报刊杂志视觉方向。
- 新 PPT 的 10 页信息结构、文字、数据及表格作为内容真相来源；源文件未包含独立图片媒体，因此本页无需图片轮播。

**Implementation evidence**

- `docs/qa/project-02/01-project02-desktop.png` — 1440 × 900 全页桌面验收图。
- `docs/qa/project-02/02-project02-mobile-top.png` — 390 × 844 手机首屏。
- `docs/qa/project-02/03-project02-experiment.png` — 页内导航后的实验表格重点状态。

**State and interactions checked**

- 10 个 PPT 对应内容段、返回作品集、章节锚点导航。
- 三张数据表均使用原生 HTML 表格；390px 下由表格容器局部横向滚动。
- 桌面与手机端页面均无横向溢出；手机端导航可横向轻扫。
- `prefers-reduced-motion` 下关闭进入动画，保留完整内容可见性。

**Required fidelity surfaces**

- Fonts and typography: 大号中文衬线标题、等宽元数据、陶土红手写式判断语；正文不低于 16px，章节标记 14px。
- Spacing and layout rhythm: 12 栏编辑网格、细分隔线和大面积留白；移动端改为单栏叙事。
- Colors and tokens: 米沙纸色、深炭黑、主站深蓝、陶土红和淡黄高亮与现有 04/05 页面协调。
- Tables: 流失主因校准、召回策略映射、A/B 实验三处均保留行列结构与重点行高亮。
- Copy and content: 保留 24 次访谈、2,731 份问卷、18.6 万行为样本、42.4%、66.7%、四层召回、滴滴 567、7.8%、+4.7pp、+5.4% 和 ROI 1.89 等 PPT 原始信息；未引入外部数据。

**Findings**

- P2: 首次自动化全页截图中，滚动进入动画使未进入视口的内容显示为空白；实际滚动浏览正常。补充页内导航到实验段的可视验收图，并确认目标段可见。
- P2: 手机端宽表可能撑宽页面。Fix: 三张表置于 `overflow-x:auto` 容器；实测页面 scrollWidth 390 等于 viewport 390，表格容器宽 390、内部宽 820。
- P3: 共用 `assets/js/vendor.js` 仍产生 Tailwind CDN 的既有警告；该文件属于全站公共运行时，不在本次单页修改范围。
- Final comparison: 无未解决的 P0/P1/P2；视觉语言延续 04/05，页面重点转向用户洞察、分层策略和实验结果。

final result: passed
