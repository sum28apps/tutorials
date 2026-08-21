#!/usr/bin/env python3
"""Build the static tutorial site into _dist/ from this repo's markdown.

Purpose-built for this repo's layout: each directory's README.md becomes its
index.html, every other .md maps 1:1, and internal .md links are rewritten to
the rendered pages. Visual language follows ohm's design tokens (paper / ink /
stone / bronze). Styling lives in tools/site.css.

Run:  pip install markdown && python tools/build_site.py
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "_dist"

SITE_NAME = "sum28 tutorials"
REPO_URL = "https://github.com/sum28apps/tutorials"

# Sidebar structure. Hrefs are site-root-relative; labels stay lowercase by
# brand rule (ohm/p2d are lowercase even at sentence start).
NAV: list[tuple[str, list[tuple[str, str]]]] = [
    ("start", [("index.html", "home")]),
    ("ohm — open house, measured", [
        ("ohm/index.html", "about ohm"),
        ("ohm/quickstart.html", "quick start · en"),
        ("ohm/quickstart.zh.html", "快速上手 · 中文"),
        ("ohm/guide/01-first-open-house.html", "1 · first open house"),
        ("ohm/guide/02-sign-in-day.html", "2 · sign-in day"),
        ("ohm/guide/03-live-and-roster.html", "3 · while it's live"),
        ("ohm/guide/04-seller-report.html", "4 · the seller report"),
        ("ohm/guide/05-listings-and-p2d.html", "5 · listings & p2d"),
        ("ohm/faq.html", "faq"),
    ]),
    ("p2d — photo to description", [
        ("p2d/index.html", "about p2d"),
        ("p2d/quickstart.html", "quick start · en"),
        ("p2d/quickstart.zh.html", "快速上手 · 中文"),
        ("p2d/guide/01-your-first-listing.html", "1 · your first listing"),
        ("p2d/guide/02-your-voice.html", "2 · your voice"),
        ("p2d/guide/03-trust-report.html", "3 · the trust report"),
        ("p2d/guide/04-five-formats.html", "4 · five formats"),
        ("p2d/guide/05-credits-and-history.html", "5 · credits & history"),
        ("p2d/faq.html", "faq"),
    ]),
]

# Custom domain for GitHub Pages: when set, a CNAME file in the published
# branch claims the domain. Set to "tutorials.sum28.com" only once the DNS
# record (tutorials CNAME sum28apps.github.io) exists — claiming earlier
# breaks the github.io URL, which redirects to the not-yet-resolving domain.
CUSTOM_DOMAIN = "tutorials.sum28.com"

MD_EXTENSIONS = ["tables", "fenced_code", "toc"]

# Paper-colored favicon with a single bronze dot — quiet, on palette.
FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E"
    "%3Crect width='16' height='16' rx='3' fill='%23F6F3EC'/%3E"
    "%3Ccircle cx='8' cy='8' r='3' fill='none' stroke='%238E7554' stroke-width='1.6'/%3E"
    "%3C/svg%3E"
)

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {site}</title>
<meta name="description" content="Beginner guides and quick starts for ohm and p2d — Sum28's flagship products.">
<link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <a class="brand" href="{root}index.html">sum28 tutorials</a>
  <div class="brand-sub">ohm · p2d — beginner guides</div>
  {nav}
</aside>
<main>
<button class="nav-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">menu</button>
<article>
{body}
</article>
<footer>
  <span>sum28</span> · <a href="https://ohm.sum28.com">ohm.sum28.com</a> ·
  <a href="https://p2dapp.sum28.com">p2dapp.sum28.com</a> ·
  <a href="{repo}">source</a>
</footer>
</main>
</div>
</body>
</html>
"""

EXTERNAL = re.compile(r"^(https?:|mailto:|#)")
HREF = re.compile(r'(href=")([^"]+)(")')
H1 = re.compile(r"^#\s+(.+)$", re.M)


def rewrite_href(href: str) -> str:
    """Map internal markdown links onto the rendered site."""
    if EXTERNAL.match(href):
        return href
    path, sep, frag = href.partition("#")
    if path.endswith(".md"):
        parts = path[:-3].split("/")
        if parts[-1] == "README":
            parts[-1] = "index"
        path = "/".join(parts) + ".html"
    return path + (("#" + frag) if sep else "")


def nav_html(active: str, root: str) -> str:
    out = []
    for label, items in NAV:
        out.append('<div class="nav-section">')
        if label:
            out.append(f'<div class="nav-label">{label}</div>')
        for href, text in items:
            current = ' aria-current="page"' if href == active else ""
            out.append(f'<a href="{root}{href}"{current}>{text}</a>')
        out.append("</div>")
    return "\n".join(out)


def render(src: Path, rel_out: str) -> None:
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    body = HREF.sub(lambda m: m.group(1) + rewrite_href(m.group(2)) + m.group(3), body)
    m = H1.search(text)
    title = m.group(1).strip() if m else SITE_NAME
    title = re.sub(r"[*`]", "", title)
    depth = rel_out.count("/")
    root = "../" * depth
    lang = "zh" if ".zh." in src.name else "en"
    html = PAGE.format(
        lang=lang, title=title, site=SITE_NAME, favicon=FAVICON,
        root=root, nav=nav_html(rel_out, root), body=body, repo=REPO_URL,
    )
    out = DIST / rel_out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "tools" / "site.css", DIST / "assets" / "site.css")

    count = 0
    for src in sorted(ROOT.rglob("*.md")):
        rel = src.relative_to(ROOT)
        if rel.parts[0] in {"_dist", "tools", ".github"}:
            continue
        parts = list(rel.parts)
        parts[-1] = "index.html" if parts[-1] == "README.md" else parts[-1][:-3] + ".html"
        render(src, "/".join(parts))
        count += 1
    if CUSTOM_DOMAIN:
        (DIST / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    # Pages serves 404.html for unknown paths.
    (DIST / "404.html").write_text(
        PAGE.format(
            lang="en", title="not found", site=SITE_NAME, favicon=FAVICON,
            root="", nav=nav_html("", ""), repo=REPO_URL,
            body="<h1>not found</h1><p>That page isn't here. "
                 '<a href="index.html">Start over</a>.</p>',
        ),
        encoding="utf-8",
    )
    print(f"built {count} pages -> {DIST}")


if __name__ == "__main__":
    main()
