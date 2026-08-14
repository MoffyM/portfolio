# AI 运营工具六项目体系 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不丢失现有五个项目内容的前提下新增 AI 运营工具为 Project 01，并把首页与全部二级页统一为六项目编号体系。

**Architecture:** 保持现有静态 HTML 与手写 Tailwind 工具类架构，不引入运行时卡片渲染或新视觉系统。用一个 Python 标准库结构校验脚本锁定编号、链接、卡片骨架、旧内容保存和相对资源路径，再做最小 HTML 修改。

**Tech Stack:** HTML5、现有 `assets/css/main.css`、Iconify、Python 3 标准库、Git。

## Global Constraints

- 正式入口始终是根目录 `index.html`，GitHub Pages 最终仍从 `main` 根目录读取该文件。
- 本次只在 `codex/add-ai-project` 分支修改，不自动合并 `main`。
- 新卡片类别、标题、副标题分别为“AI项目”“自制AI工具”“vibe coding产物 · AI工作提效”。
- 新卡片使用现有 Project 05 的 `#2b6b6b` 配色；右侧仅有 `WEB PROJECT` 与 `>_`，布局沿用原 Project 04。
- 六张首页卡片保持相同的 `a > article` 顶层 DOM 骨架。
- 原五个项目内容完整顺延至 `project-02.html` 至 `project-06.html`，不得覆盖或删除。
- 首页必须使用 `<html lang="zh-CN">`。
- 所有站内资源继续使用 GitHub Pages 兼容的相对路径。
- 不修改 `vendor.js`、`iconify.js`、`tailwind-config.js`，除非测试证明需求无法用现有文件实现。
- 不复制 `index1.html`、`index2.html` 等历史文件；历史只由 Git 保存。

---

### Task 1: 建立六项目结构回归测试

**Files:**
- Create: `tests/verify_portfolio.py`
- Read: `index.html`
- Read: `pages/project-01.html` through `pages/project-06.html`

**Interfaces:**
- Consumes: 仓库根目录中的静态 HTML 文件。
- Produces: 命令 `python tests/verify_portfolio.py`，成功时打印 `portfolio verification passed` 并返回 0；任一约束失败时抛出带约束名称的 `AssertionError`。

- [ ] **Step 1: 写入预期失败的结构测试**

```python
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8-sig")
EXPECTED_TITLES = [
    "自制AI工具", "用户召回策略", "活动运营IP联动",
    "跨境项目管理", "毕业项目网站成果", "汉字3D数字化创作",
]

assert '<html lang="zh-CN">' in INDEX, "homepage language"
cards = re.findall(
    r'<a href="pages/project-(\d{2})\.html" class="block"><article class="([^"]+)">(.*?)</article></a>',
    INDEX,
    re.S,
)
assert [number for number, _, _ in cards] == ["01", "02", "03", "04", "05", "06"], "six ordered cards"
assert all(body.count("flex-1 flex items-center justify-between") == 1 for _, _, body in cards), "shared card skeleton"
assert "AI项目" in cards[0][2] and "自制AI工具" in cards[0][2], "AI card copy"
assert "vibe coding产物 · AI工作提效" in cards[0][2], "AI card subtitle"
assert cards[0][2].count("WEB PROJECT") == 1 and cards[0][2].count(">_") == 1, "AI card badges"

for number, title in enumerate(EXPECTED_TITLES, start=1):
    page = ROOT / "pages" / f"project-{number:02}.html"
    assert page.exists(), f"missing {page.name}"
    html = page.read_text(encoding="utf-8-sig")
    assert title in html, f"title missing from {page.name}"
    assert f"项目 / {number:02}" in html, f"header number {page.name}"
    assert f"{number:02} / 06" in html, f"total count {page.name}"
    assert '../index.html#timeline' in html, f"return link {page.name}"

for html_path in [ROOT / "index.html", *(ROOT / "pages").glob("project-*.html")]:
    html = html_path.read_text(encoding="utf-8-sig")
    for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
        if ref.startswith(("http://", "https://", "mailto:", "#")) or "{" in ref:
            continue
        target = (html_path.parent / ref.split("#", 1)[0]).resolve()
        assert target.exists(), f"broken local reference: {html_path.name} -> {ref}"

print("portfolio verification passed")
```

- [ ] **Step 2: 运行测试并确认因六项目尚不存在而失败**

Run: `python tests/verify_portfolio.py`

Expected: FAIL，首个失败是 `homepage language` 或 `six ordered cards`，证明测试检测到当前五项目结构。

- [ ] **Step 3: 提交测试基线**

```powershell
git add -- tests/verify_portfolio.py
git commit -m "test: define six-project portfolio structure"
```

### Task 2: 新增首页 AI 卡片并顺延原卡片

**Files:**
- Modify: `index.html`
- Test: `tests/verify_portfolio.py`
- Inspect only unless required: `assets/css/main.css`

**Interfaces:**
- Consumes: 当前首页 Project 04 的徽标 DOM、Project 05 的 `#2b6b6b` 色值及现有 `a > article` 卡片骨架。
- Produces: 六张按 01–06 排列且链接到相同编号二级页的首页卡片。

- [ ] **Step 1: 把首页语言改为中文**

将唯一的 `<html lang="en">` 替换为 `<html lang="zh-CN">`。

- [ ] **Step 2: 在现有 Project 01 前插入新卡片**

新卡片必须使用现有顶层结构：

```html
<a href="pages/project-01.html" class="block"><article class="flex border border-ink bg-base relative hover:-translate-y-1 transition-transform shadow-[4px_4px_0px_rgba(26,26,26,1)] hover:bg-grid/5 transition-colors cursor-pointer">
```

编号栏使用 `bg-[#2b6b6b]`，正文文字使用 `text-[#2b6b6b]`。右侧徽标区使用原 Project 04 的 `hidden sm:flex flex-col gap-1` 容器以及两个同尺寸边框项，内容严格为 `WEB PROJECT` 和 `>_`。

- [ ] **Step 3: 原五张卡片整体顺延编号和 href**

只修改每张卡片的注释编号、`href` 和左侧显示编号：原 01→02、02→03、03→04、04→05、05→06。保留原标题、副标题、图标、颜色、徽标和响应式类。

- [ ] **Step 4: 检查新增类是否已经存在于手写 CSS**

Run: `rg -n -F '.bg-\\[\\#2b6b6b\\]' assets/css/main.css`

Expected: 至少一处匹配；若没有匹配，只把新卡片实际使用且缺失的选择器按现有生成格式补入 `assets/css/main.css`，不做其他 CSS 修改。

- [ ] **Step 5: 运行结构测试并确认仍因二级页未顺延而失败**

Run: `python tests/verify_portfolio.py`

Expected: 首页相关断言通过，随后因 `project-06.html` 缺失或旧页编号未更新而 FAIL。

- [ ] **Step 6: 提交首页改动**

```powershell
git add -- index.html assets/css/main.css
git commit -m "feat: add AI project card to portfolio"
```

如果 `assets/css/main.css` 无改动，则只暂存 `index.html`。

### Task 3: 无损顺延五个二级页并创建新 Project 01

**Files:**
- Create: `pages/project-06.html`
- Modify: `pages/project-01.html`
- Modify: `pages/project-02.html`
- Modify: `pages/project-03.html`
- Modify: `pages/project-04.html`
- Modify: `pages/project-05.html`
- Test: `tests/verify_portfolio.py`

**Interfaces:**
- Consumes: `main` 中原 `project-01.html` 至 `project-05.html` 的完整文件内容。
- Produces: `project-01.html` 至 `project-06.html`，页面编号、标签编号与总数一致。

- [ ] **Step 1: 从高到低复制原页面，避免覆盖源内容**

依次复制原 05→新 06、原 04→新 05、原 03→新 04、原 02→新 03、原 01→新 02。复制后只替换目标页中的页眉 `项目 / NN`、Hero `项目 NN`、所有标签 `[NN]` 和 Deck 计数 `NN / 06`；标题、描述、指标、占位卡片和资源引用保持原样。

- [ ] **Step 2: 用现有二级页模板重建 Project 01**

以原页面完整结构为模板，设置：

```html
<title>自制AI工具 - 周芷琦 · 个人作品集</title>
<span>项目 / 01</span>
项目 01 · AI项目
<h1 class="font-sans font-bold text-5xl md:text-7xl leading-[0.9] tracking-tight uppercase mb-8 text-[#2b6b6b]">
    自制AI工具
</h1>
<p class="text-sm md:text-base max-w-2xl leading-relaxed font-semibold mb-12">
    vibe coding产物 · AI工作提效
</p>
```

关键数据只使用已确认信息，标签为“AI项目”“vibe coding”“AI工作提效”“WEB PROJECT”，每项编号均为 `[01]`。Deck 计数为 `01 / 06`，PPT 展示区及四张占位卡片沿用现有模板。

- [ ] **Step 3: 检查不存在旧五项目总数或错位编号**

Run: `rg -n "0[1-6] / 05|项目 / 0[1-6]|\[0[1-6]\]" pages/project-*.html`

Expected: 不出现 `NN / 05`；每个文件中的页眉、标签和 Deck 编号只对应文件名编号。

- [ ] **Step 4: 运行完整结构测试**

Run: `python tests/verify_portfolio.py`

Expected: PASS，输出 `portfolio verification passed`。

- [ ] **Step 5: 提交二级页改动**

```powershell
git add -- pages/project-01.html pages/project-02.html pages/project-03.html pages/project-04.html pages/project-05.html pages/project-06.html
git commit -m "feat: expand project pages to six-item system"
```

### Task 4: 最终验证、diff 审查与草稿 PR

**Files:**
- Verify: `index.html`
- Verify: `assets/css/main.css`
- Verify: `assets/js/vendor.js`
- Verify: `assets/js/iconify.js`
- Verify: `assets/js/tailwind-config.js`
- Verify: `assets/img/moon.svg`
- Verify: `pages/project-01.html` through `pages/project-06.html`
- Verify: `tests/verify_portfolio.py`

**Interfaces:**
- Consumes: 完成的分支提交。
- Produces: 已推送的 `codex/add-ai-project` 分支与未合并的草稿 PR。

- [ ] **Step 1: 运行新鲜的全量结构验证**

Run: `python tests/verify_portfolio.py`

Expected: PASS，输出 `portfolio verification passed`。

- [ ] **Step 2: 检查空白错误和变更范围**

Run: `git diff --check origin/main...HEAD`

Expected: 无输出，退出码 0。

Run: `git diff --stat origin/main...HEAD`

Expected: 只包含设计说明、实施计划、测试、`index.html`、六个项目页，以及确有必要时的 `main.css`。

- [ ] **Step 3: 确认未删除或改名资源**

Run: `git diff --name-status origin/main...HEAD`

Expected: 不出现 `D`；现有 CSS、JS、图片路径没有重命名。

- [ ] **Step 4: 推送安全分支**

Run: `git push -u origin codex/add-ai-project`

Expected: 首次运行时由 Git Credential Manager 打开 GitHub 登录授权；授权后分支推送成功。

- [ ] **Step 5: 创建草稿 PR，不合并 main**

PR 标题：`feat: add AI project and six-project numbering`

PR 正文列出修改文件、每个文件作用、新增文件、零删除、零路径更改、潜在风险和 GitHub Pages 相对路径检查结果。创建后保持 Draft 状态并把链接交给用户。
