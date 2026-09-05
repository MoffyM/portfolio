# 跨境项目管理案例页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Project 04 的 PPT 占位页重构为面向面试官、响应式且可本地浏览的跨境项目管理完整案例页。

**Architecture:** 保持现有静态 HTML、预编译 Tailwind 工具类和相对资源路径。Project 04 的专属排版与无依赖交互内聚在单个 HTML 中，两张 PPT 原图作为独立静态资源；Python 结构测试锁定内容与交互契约。

**Tech Stack:** HTML5、页面内 CSS、原生 JavaScript、现有 Tailwind 工具类、Iconify、Python 标准库测试、Git。

**Spec:** `docs/superpowers/specs/2026-09-02-crossborder-project-page-design.md`

## Global Constraints

- 只修改 Project 04、两张图片资产及对应测试。
- 使用 `#f4f1eb`、`#1a1a1a`、`#1a3b5c`、`#ea4313`；淡黄色只作少量高亮。
- 两张 Excel 截图完整展示，不裁剪、不额外脱敏。
- 所有事实来自 PPT：2 个项目、53,000+ 字、8 人、100% 按期交付、13 个里程碑、1,240 处术语不一致纠正。
- 返回链接固定为 `../index.html#timeline`。
- 不增加第三方依赖，不修改全站脚本和其他项目页。
- 不执行推送、PR、GitHub Pages 或线上部署。

---

### Task 1: 建立新版 Project 04 回归测试

**Files:**
- Modify: `tests/verify_portfolio.py`
- Test: `tests/verify_portfolio.py`

**Interfaces:**
- Consumes: `PAGES["04"]` 的 HTML。
- Produces: `validate_project_04_case_study(html)`，锁定新版内容、图片和灯箱契约。

- [ ] **Step 1: 写失败测试**

从 `LEGACY_PAGE_FINGERPRINTS` 删除 `"04"`，新增并调用：

```python
def validate_project_04_case_study(html):
    required_text = [
        "53,000+", "8 人", "2 个项目", "100% 按期交付", "13 个里程碑",
        "1,240", "标准前置", "看板驱动", "三维审核", "风险早判",
    ]
    for text in required_text:
        assert text in html, f"project-04 evidence: {text}"
    assert 'data-case-study="project-04"' in html, "project-04 case study root"
    assert html.count('class="evidence-trigger"') == 2, "project-04 evidence triggers"
    assert '../assets/img/project-04-milestones-risk.png' in html, "milestone image"
    assert '../assets/img/project-04-terminology.png' in html, "terminology image"
    assert 'id="evidence-lightbox"' in html, "project-04 lightbox"
    assert 'aria-modal="true"' in html, "project-04 modal semantics"
    assert "Escape" in html and "prefers-reduced-motion" in html, "project-04 accessible motion"

validate_project_04_case_study(PAGES["04"])
```

- [ ] **Step 2: 运行并确认旧页面失败**

```powershell
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests\verify_portfolio.py
```

Expected: FAIL 于首个新版 Project 04 断言。

- [ ] **Step 3: 提交测试**

```powershell
git add -- tests/verify_portfolio.py
git commit -m "test: define cross-border case page contract"
```

### Task 2: 加入完整项目证据图片

**Files:**
- Create: `assets/img/project-04-milestones-risk.png`
- Create: `assets/img/project-04-terminology.png`

**Interfaces:**
- Consumes: PPT 内嵌 `image1.png`、`image2.png`。
- Produces: 两个由 Project 04 相对路径引用的 PNG 文件。

- [ ] **Step 1: 复制原始图片**

```powershell
Copy-Item -LiteralPath 'D:\OneDrive\文档\作品集\.ppt_analysis_crossborder\template-inspect\assets\ppt\media\image1.png' -Destination 'assets\img\project-04-milestones-risk.png'
Copy-Item -LiteralPath 'D:\OneDrive\文档\作品集\.ppt_analysis_crossborder\template-inspect\assets\ppt\media\image2.png' -Destination 'assets\img\project-04-terminology.png'
```

- [ ] **Step 2: 验证文件**

```powershell
Add-Type -AssemblyName System.Drawing
Get-ChildItem assets\img\project-04-*.png | ForEach-Object {
  $img=[System.Drawing.Image]::FromFile($_.FullName)
  try { "{0}: {1} bytes, {2}x{3}" -f $_.Name,$_.Length,$img.Width,$img.Height }
  finally { $img.Dispose() }
}
```

Expected: 两个文件均大于 300 KB，且能正常读取尺寸。

- [ ] **Step 3: 提交资产**

```powershell
git add -- assets/img/project-04-milestones-risk.png assets/img/project-04-terminology.png
git commit -m "assets: add cross-border project evidence"
```

### Task 3: 重写 Project 04 案例页

**Files:**
- Modify: `pages/project-04.html`
- Test: `tests/verify_portfolio.py`

**Interfaces:**
- Consumes: 两张证据图片。
- Produces: 带 `data-case-study="project-04"`、两个 `.evidence-trigger`、`#evidence-lightbox` 的完整页面。

- [ ] **Step 1: 建立页面语义骨架**

```html
<body data-case-study="project-04" class="bg-base text-ink antialiased overflow-x-hidden">
  <a class="back-link" href="../index.html#timeline">← 返回作品集</a>
  <main>
    <header class="case-meta">PROJECT / 04 · 2023</header>
    <section id="overview"></section>
    <section id="responsibilities"></section>
    <section id="process"></section>
    <section id="risk"></section>
    <section id="standards"></section>
    <section id="outcomes"></section>
    <section id="retrospective"></section>
  </main>
  <div id="evidence-lightbox" role="dialog" aria-modal="true" aria-hidden="true"></div>
</body>
```

- [ ] **Step 2: 写入 PPT 事实**

首屏写四项成果；能力区写三项职责；过程区写六阶段；风险区呈现 R-01 至 R-05 的“风险—动作—结果”；标准区写术语表 v1.0、82 条高频术语、35 条法律/商务术语，以及预计 3,000+ 降至 1,240；结尾写四条方法论。

- [ ] **Step 3: 实现视觉系统**

```css
:root { --paper:#f4f1eb; --ink:#1a1a1a; --navy:#1a3b5c; --red:#ea4313; --highlight:#eadb87; --rule:rgba(26,26,26,.18); }
.display { font-family:Georgia,"Source Serif 4",serif; }
.meta { font-family:"JetBrains Mono",Consolas,monospace; text-transform:uppercase; letter-spacing:.14em; }
.editorial-grid { display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); }
.hand-note { color:var(--red); font-family:"Segoe Print",cursive; transform:rotate(-3deg); }
.stamp { border:2px solid var(--red); border-radius:999px; }
```

桌面使用 12 列编辑网格；`max-width:767px` 下改为单列、指标 2×2、返回按钮触控高度至少 44px。

- [ ] **Step 4: 实现截图灯箱**

两个按钮使用完整图片和说明性 `alt`，例如：

```html
<button class="evidence-trigger" type="button"
  data-full="../assets/img/project-04-milestones-risk.png"
  aria-label="放大查看项目里程碑与风险追踪完整截图">
  <img src="../assets/img/project-04-milestones-risk.png" alt="项目里程碑与风险追踪完整表格">
</button>
```

脚本统一用 `openLightbox(trigger)` 与 `closeLightbox()` 管理灯箱、页面滚动和焦点；关闭按钮、遮罩与 `Escape` 均调用 `closeLightbox()`。

- [ ] **Step 5: 实现渐显与减少动态效果**

```javascript
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  }), { threshold: 0.12 });
  document.querySelectorAll('[data-reveal]').forEach(node => observer.observe(node));
} else {
  document.querySelectorAll('[data-reveal]').forEach(node => node.classList.add('is-visible'));
}
```

- [ ] **Step 6: 运行测试并提交**

```powershell
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests\verify_portfolio.py
git add -- pages/project-04.html
git commit -m "feat: redesign cross-border project case page"
```

Expected: `portfolio verification passed`。

### Task 4: 响应式验证与本地交付

**Files:**
- Verify: `pages/project-04.html`
- Verify: `assets/img/project-04-*.png`
- Verify: `tests/verify_portfolio.py`

**Interfaces:**
- Consumes: 完成的静态页面。
- Produces: 通过结构、响应式、交互和差异范围检查的本地预览。

- [ ] **Step 1: 启动本地服务**

```powershell
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m http.server 4173 --bind 127.0.0.1
```

访问 `http://127.0.0.1:4173/pages/project-04.html`。

- [ ] **Step 2: 检查视口**

检查 1440×900、1024×768、430×932、390×844：标题无截断、正文无页面级横向溢出、指标顺序正确、图片完整可见且窄屏表格可横向浏览。

- [ ] **Step 3: 检查交互**

逐张验证图片灯箱、关闭按钮、遮罩、`Escape`、焦点恢复，以及减少动态效果模式。

- [ ] **Step 4: 最终验证**

```powershell
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests\verify_portfolio.py
git diff --check main...HEAD
git diff --name-status main...HEAD
git status --short
```

Expected: 测试通过；空白检查无输出；变更仅包含设计说明、计划、测试、Project 04 和两张图片；工作树干净。

- [ ] **Step 5: 本地展示**

在 Codex 中打开 `http://127.0.0.1:4173/pages/project-04.html`，交付 HTML 与图片路径、分支名和测试结果，并明确没有推送或更新线上网站。
