# Design QA — Homepage refresh

**Source visual truth**

- `docs/qa/homepage/comparison-input/01-reference.png` — 用户提供的 MY STORY 时间线参考图。
- 现有主页的米沙纸色、深蓝、陶土橙、细网格与编辑式排版为站点视觉基线。

**Implementation evidence**

- `docs/qa/homepage/desktop-full.png` — 1440 × 900 CSS viewport，density 1，桌面完整页。
- `docs/qa/homepage/mobile-full.png` — 390 × 844 CSS viewport，density 1，手机完整页。
- `docs/qa/homepage/desktop-timeline-panel.png` 与 `mobile-timeline-panel.png` — 时间线聚焦区域。
- `docs/qa/homepage/timeline-comparison.png` — 参考图与实现图的并排对照。

**States and interactions checked**

- 首屏欢迎语、能力卡与新增引导语。
- ABOUT ME 档案、五段 MY STORY 时间线、成长轨迹印章。
- 项目详情引导、末页联系方式、微信二维码和诗歌组件。
- 桌面 1440px 与手机 390px 均无横向溢出；二维码可见且保持正方形比例。

**Required fidelity surfaces**

- Fonts and typography: 中文采用思源宋体优先的系统字体栈，英文采用 Anthropic Serif 优先的衬线回退栈；正文与时间线说明最低 16px，标题保持原站粗体层级。
- Spacing and layout rhythm: 桌面双栏、手机单栏；时间线图标与文字分列，修复了手机首轮图标与标题相碰的问题。
- Colors and tokens: 沿用主页米沙底、深蓝黑与陶土橙；年份、关键指标与岭南大学信息按要求使用橙色。
- Image quality and asset fidelity: 微信二维码直接使用用户原图，80 × 80 CSS px 展示，无拉伸；参考图只用于对照，不进入成品页面。
- Copy and content: 指定旧文案均移除；Agent 档案、五段经历、项目引导、联系方式与诗歌按钮文字逐项核对。

**Findings and comparison history**

- First responsive pass — P2: 手机时间线第二至第五项使用 48px 左内边距，圆形图标与长标题发生接触。Fix: 全部时间线条目统一为 64px 左内边距。Post-fix evidence: `mobile-timeline-panel.png`。
- Second reference pass — P2: 纵向指引线过淡，手机印章压近最后一项内容。Fix: 使用 38% 深蓝实线贯穿五个节点，最后一项增加右侧安全空间，并把印章定位到统一底线上方。Post-fix evidence: 最新 `desktop-timeline-panel.png` 与 `mobile-timeline-panel.png`。
- Full-view comparison: 实现保留参考图的纵向节点、圆形线性图标、橙色年份/指标和右下印章，同时延续现有主页网格体系，属于有意的品牌适配。
- Focused comparison: 时间线与联系方式分别单独截图检查；长标题可换行，二维码清晰，手机端没有横向滚动。
- P3: 指定商业字体文件未随项目提供，当前以同类系统衬线字体回退；未来若提供合法字体文件可进一步锁定跨设备一致性。
- Final comparison: 无未解决的 P0/P1/P2。

final result: passed
