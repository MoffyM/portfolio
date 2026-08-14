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
