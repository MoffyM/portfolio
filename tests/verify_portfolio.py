from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NUMBERS = [f"{number:02}" for number in range(1, 7)]
EXPECTED_TITLES = [
    "自制AI工具",
    "用户召回策略",
    "活动运营IP联动",
    "跨境项目管理",
    "毕业项目网站成果",
    "汉字3D数字化创作",
]
# origin/main project-01..05 after normalizing only the allowed numbering fields.
LEGACY_PAGE_FINGERPRINTS = {
    "02": "9546ca62c1ea15aa242f086ecf831fc2f8fef8506cea3a079e7ecb0dab7821ad",
    "03": "fdfc0c00cfed29309a0affbbe1c32a3a19b24bc53742c5d0d4a1fea3de5ec9b2",
    "05": "3d67e812f4950c12630a453d014f2d9cd78cd55e13c0e7363c73713b2d28dca2",
    "06": "61835c7dbb0df71bb9d974f923f380fdc5d821fd464ef8029d3351f86460a9c5",
}
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class Element:
    def __init__(self, tag, attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []


class DOMParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs)
        self.stack[-1].children.append(element)
        if tag not in VOID_ELEMENTS:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Element(tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_html(html):
    parser = DOMParser()
    parser.feed(html)
    parser.close()
    assert len(parser.stack) == 1, "unclosed HTML elements"
    return parser.root


def element_children(element):
    return [child for child in element.children if isinstance(child, Element)]


def descendants(element):
    for child in element_children(element):
        yield child
        yield from descendants(child)


def find_elements(element, tag=None, **attrs):
    return [
        candidate
        for candidate in descendants(element)
        if (tag is None or candidate.tag == tag)
        and all(candidate.attrs.get(name) == value for name, value in attrs.items())
    ]


def text_content(element):
    parts = []

    def collect(node):
        for child in node.children:
            if isinstance(child, Element):
                collect(child)
            else:
                parts.append(child)

    collect(element)
    return " ".join("".join(parts).split())


def has_classes(element, *required):
    return set(required).issubset(element.attrs.get("class", "").split())


def validate_homepage(html):
    root = parse_html(html)
    html_elements = find_elements(root, "html")
    assert len(html_elements) == 1, "homepage html root"
    assert html_elements[0].attrs.get("lang") == "zh-CN", "homepage language"

    timeline_sections = find_elements(root, "section", id="timeline")
    assert len(timeline_sections) == 1, "homepage project section"
    timeline = timeline_sections[0]
    project_anchors = [
        element
        for element in descendants(timeline)
        if element.tag == "a"
        and re.fullmatch(r"pages/project-(\d{2})\.html", element.attrs.get("href", ""))
    ]
    assert len(project_anchors) == 6, "project section has exactly six project anchors"

    href_numbers = []
    displayed_numbers = []
    articles = []
    for anchor in project_anchors:
        href_numbers.append(re.fullmatch(
            r"pages/project-(\d{2})\.html", anchor.attrs["href"]
        ).group(1))
        anchor_children = element_children(anchor)
        assert [child.tag for child in anchor_children] == ["article"], "project anchor directly contains one article"
        article = anchor_children[0]
        articles.append(article)
        article_children = element_children(article)
        assert article_children, "project article children"
        number_tab_children = element_children(article_children[0])
        assert number_tab_children and number_tab_children[0].tag == "span", "project number tab"
        displayed_numbers.append(text_content(number_tab_children[0]))

    assert href_numbers == EXPECTED_NUMBERS, "ordered project href numbers"
    assert displayed_numbers == EXPECTED_NUMBERS, "href and displayed project numbers correspond"
    direct_structures = [tuple(child.tag for child in element_children(article)) for article in articles]
    assert direct_structures == [("div", "div")] * 6, "six article direct-child structures"

    for article, title in zip(articles, EXPECTED_TITLES):
        assert title in text_content(article), f"homepage card title: {title}"

    ai_article = articles[0]
    assert "AI项目" in text_content(ai_article), "AI card category"
    assert "vibe coding产物 · AI工作提效" in text_content(ai_article), "AI card subtitle"
    badge_containers = [
        element
        for element in descendants(ai_article)
        if element.tag == "div" and has_classes(element, "hidden", "sm:flex", "flex-col", "gap-1")
    ]
    assert len(badge_containers) == 1, "AI card badge container"
    badge_items = element_children(badge_containers[0])
    assert len(badge_items) == 2, "AI card has exactly two direct badge items"
    assert [text_content(item) for item in badge_items] == ["WEB PROJECT", ">_"], "AI card badge order and text"

    watermarks = [
        element
        for element in descendants(timeline)
        if element.tag == "div" and has_classes(element, "story-watermark")
    ]
    assert len(watermarks) == 1 and text_content(watermarks[0]) == "06+ STORIES", "six-project story count"


def normalize_legacy_page(html):
    normalized = html.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"项目 / \d{2}", "项目 / NN", normalized)
    normalized = re.sub(r"项目 \d{2}(?=\s*·)", "项目 NN", normalized)
    normalized = re.sub(r"\[\d{2}\]", "[NN]", normalized)
    return re.sub(r"\d{2} / \d{2}", "NN / TOTAL", normalized)


def normalized_sha256(html):
    return sha256(normalize_legacy_page(html).encode("utf-8")).hexdigest()


def validate_project_page(html, number, title, expected_fingerprint=None):
    assert title in html, f"title missing from project-{number}.html"
    assert re.findall(r"项目 / (\d{2})", html) == [number], f"header number project-{number}.html"
    assert re.findall(r"项目 (\d{2})(?=\s*·)", html) == [number], f"Hero number project-{number}.html"
    bracketed_numbers = re.findall(r"\[\d{2}\]", html)
    assert bracketed_numbers and set(bracketed_numbers) == {f"[{number}]"}, f"bracketed labels project-{number}.html"
    assert re.findall(r"(\d{2}) / (\d{2})", html) == [(number, "06")], f"total count project-{number}.html"
    assert '../index.html#timeline' in html, f"return link project-{number}.html"
    if expected_fingerprint is not None:
        assert normalized_sha256(html) == expected_fingerprint, f"legacy content project-{number}.html"


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


def assert_rejects_mutation(name, expected_message, check):
    try:
        check()
    except AssertionError as error:
        assert expected_message in str(error), (
            f"negative mutation failed for the wrong reason: {name}: {error}"
        )
        print(f"negative mutation rejected: {name} -> {error}")
        return
    raise AssertionError(f"negative mutation was not rejected: {name}")


INDEX = (ROOT / "index.html").read_text(encoding="utf-8-sig")
PAGES = {
    number: (ROOT / "pages" / f"project-{number}.html").read_text(encoding="utf-8-sig")
    for number in EXPECTED_NUMBERS
}

validate_homepage(INDEX)
for number, title in zip(EXPECTED_NUMBERS, EXPECTED_TITLES):
    validate_project_page(PAGES[number], number, title, LEGACY_PAGE_FINGERPRINTS.get(number))

validate_project_04_case_study(PAGES["04"])

for html_path in [ROOT / "index.html", *(ROOT / "pages").glob("project-*.html")]:
    html = html_path.read_text(encoding="utf-8-sig")
    for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
        if ref.startswith(("http://", "https://", "mailto:", "#")) or "{" in ref:
            continue
        target = (html_path.parent / ref.split("#", 1)[0]).resolve()
        assert target.exists(), f"broken local reference: {html_path.name} -> {ref}"

wrong_display, display_mutations = re.subn(
    r'(<a href="pages/project-01\.html".*?<span class="font-sans font-bold text-xl leading-none">)01(</span>)',
    r"\g<1>99\g<2>",
    INDEX,
    count=1,
    flags=re.S,
)
assert display_mutations == 1, "wrong-display mutation fixture"
assert_rejects_mutation(
    "wrong displayed number",
    "href and displayed project numbers correspond",
    lambda: validate_homepage(wrong_display),
)

badge_tail = """>_</div>
                                </div>
                            </div>"""
third_badge = INDEX.replace(
    badge_tail,
    """>_</div>
                                </div>
                                <div>EXTRA</div>
                            </div>""",
    1,
)
assert third_badge != INDEX, "third-badge mutation fixture"
assert_rejects_mutation(
    "third AI badge",
    "AI card has exactly two direct badge items",
    lambda: validate_homepage(third_badge),
)

deleted_body = PAGES["02"].replace("在滴滴参与沉默与流失用户召回", "", 1)
assert deleted_body != PAGES["02"], "deleted-body mutation fixture"
assert_rejects_mutation(
    "deleted legacy body",
    "legacy content project-02.html",
    lambda: validate_project_page(
        deleted_body, "02", EXPECTED_TITLES[1], LEGACY_PAGE_FINGERPRINTS["02"]
    ),
)

wrong_label = PAGES["02"].replace("[02]", "[99]", 1)
assert wrong_label != PAGES["02"], "wrong-label mutation fixture"
assert_rejects_mutation(
    "wrong bracketed label",
    "bracketed labels project-02.html",
    lambda: validate_project_page(
        wrong_label, "02", EXPECTED_TITLES[1], LEGACY_PAGE_FINGERPRINTS["02"]
    ),
)

print("portfolio verification passed")
