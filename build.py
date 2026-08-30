#!/usr/bin/env python
"""Static site generator for yanjordan.github.io.

Usage
-----
    python build.py            # build the site into the repository root
    python build.py --serve    # build, then serve at http://localhost:8000
    python build.py --check    # build, then report broken local links

Design
------
Content lives in src/ and is rendered with Jinja2 into plain HTML files at the
repository root, which is what GitHub Pages publishes. There is no Ruby, no
Jekyll and no CI step: run this script, commit the output, done.

Publications come exclusively from src/data/publications.bib, so a paper can
never again be mis-cited by hand-editing HTML.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from jinja2 import Environment, FileSystemLoader, StrictUndefined  # noqa: E402

import bibparse  # noqa: E402
import content  # noqa: E402

# Every spelling of the site owner's name that appears in the bibliography.
SELF_NAMES = {"Zeyin Yan", "Z. Yan", "Zeyin YAN"}

# Optional bib fields the templates may reference. Filled in with None so the
# templates can stay readable (``p.local_si``) while Jinja runs with
# StrictUndefined, which is what catches genuine typos.
OPTIONAL_FIELDS = (
    "abbrev", "volume", "number", "pages", "articleno", "doi", "note", "school",
    "local_pdf", "local_si", "local_image", "preprint_pdf", "preprint_si",
    "code_url", "slides_pdf", "selected", "equal_contrib",
)


# ---------------------------------------------------------------------------
# Publications
# ---------------------------------------------------------------------------
def is_self(name: str) -> bool:
    return name.strip() in SELF_NAMES


def abbreviate(name: str) -> str:
    """'Yunteng Sam Liao' -> 'Y. S. Liao'; leaves already-short forms alone."""
    parts = name.split()
    if len(parts) < 2:
        return name
    *firsts, last = parts
    initials = " ".join(p if p.endswith(".") else f"{p[0]}." for p in firsts)
    return f"{initials} {last}"


def author_html(entry: dict) -> str:
    """Author list with the site owner in bold."""
    out = []
    for name in entry["authors"]:
        short = abbreviate(name)
        if is_self(name):
            marker = "&#8225;" if entry.get("equal_contrib") == "true" else ""
            out.append(f'<strong class="self">{short}{marker}</strong>')
        else:
            out.append(short)
    return ", ".join(out)


def venue_html(entry: dict) -> str:
    """'<em>Nat. Commun.</em> 2024, <strong>15</strong>, 4181'."""
    if entry.get("entrytype") == "phdthesis":
        return f'{entry.get("school", "")}, {entry.get("year", "")}'

    bits = [f'<em>{entry.get("abbrev") or entry.get("journal", "")}</em>']
    bits.append(f'{entry["year"]},')
    if entry.get("volume"):
        vol = f'<strong>{entry["volume"]}</strong>'
        if entry.get("number"):
            vol += f'({entry["number"]})'
        bits.append(vol + ",")
    tail = entry.get("pages") or entry.get("articleno")
    if tail:
        bits.append(tail)
    return " ".join(bits).rstrip(",")


def load_publications() -> dict:
    entries = bibparse.parse(SRC / "data" / "publications.bib")

    papers, theses = [], []
    for e in entries:
        for field in OPTIONAL_FIELDS:
            e.setdefault(field, None)
        e["author_html"] = author_html(e)
        e["venue_html"] = venue_html(e)
        e["is_selected"] = e.get("selected") == "true"
        e["is_equal"] = e.get("equal_contrib") == "true"
        e["is_first_author"] = bool(e["authors"]) and is_self(e["authors"][0])
        e["doi_url"] = f'https://doi.org/{e["doi"]}' if e.get("doi") else None
        e["image_webp"] = webp_name(e.get("local_image"))
        (theses if e["entrytype"] == "phdthesis" else papers).append(e)

    papers.sort(key=lambda e: (int(e["year"]), e.get("doi", "")), reverse=True)

    by_year: dict[str, list] = {}
    for p in papers:
        by_year.setdefault(p["year"], []).append(p)

    return {
        "all": papers,
        "by_year": sorted(by_year.items(), key=lambda kv: int(kv[0]), reverse=True),
        "selected": [p for p in papers if p["is_selected"]],
        "theses": theses,
        "count": len(papers),
        "first_author_count": sum(1 for p in papers if p["is_first_author"]),
    }


def webp_name(path: str | None) -> str | None:
    """research/NC2024.jpg -> research/NC2024.webp, if that file exists."""
    if not path:
        return None
    candidate = Path(path).with_suffix(".webp")
    return str(candidate).replace("\\", "/") if (ROOT / candidate).exists() else None


# ---------------------------------------------------------------------------
# Content normalisation
# ---------------------------------------------------------------------------
# Optional keys per content block, so entries in content.py only need to spell
# out the fields they actually use while Jinja still runs with StrictUndefined.
CODE_ITEM_DEFAULTS = {"paper": None, "paper_doi": None, "links": []}
CV_LIST_DEFAULTS = {
    "appointments": {"period": None, "role": None, "org": None, "place": None, "detail": None},
    "education": {"period": None, "degree": None, "org": None, "place": None, "detail": None},
    "funding": {"period": None, "title": None, "org": None, "detail": None},
    "talks": {"title": None, "venue": None, "year": None},
    "skills": {"label": None, "items": None},
}


def _fill(items, defaults) -> None:
    for item in items:
        if isinstance(item, dict):
            for key, value in defaults.items():
                item.setdefault(key, list(value) if isinstance(value, list) else value)


def normalize_content() -> None:
    for group in content.CODE["groups"]:
        _fill(group["items"], CODE_ITEM_DEFAULTS)
    for key, defaults in CV_LIST_DEFAULTS.items():
        _fill(content.CV.get(key, []), defaults)
    # Skill rows accept either a string or a list of tools.
    for row in content.CV.get("skills", []):
        if isinstance(row.get("items"), (list, tuple)):
            row["items"] = ", ".join(row["items"])


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
PAGES = [
    ("index.html", "page_home.html", "Home"),
    ("research.html", "page_research.html", "Research"),
    ("publications.html", "page_publications.html", "Publications"),
    ("code.html", "page_code.html", "Code"),
    ("cv.html", "page_cv.html", "CV"),
    ("news.html", "page_news.html", "News"),
    ("teaching.html", "page_teaching.html", "Teaching"),
    ("join.html", "page_join.html", "Join us"),
    # Kept only so the old URL does not 404; deliberately absent from the nav.
    ("personal.html", "page_personal.html", "Personal"),
]


def build() -> list[Path]:
    env = Environment(
        loader=FileSystemLoader(SRC / "templates"),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,  # content.py and the bib hold trusted, hand-written HTML
    )

    pubs = load_publications()
    normalize_content()

    # Attach WebP variants to the home-page figures, if they were generated.
    for fig in content.HOME["figures"]:
        fig["webp"] = webp_name(fig["src"])

    written = []

    for out_name, template_name, title in PAGES:
        html = env.get_template(template_name).render(
            site=content.SITE,
            links=content.LINKS,
            nav=content.NAV,
            home=content.HOME,
            research=content.RESEARCH,
            code=content.CODE,
            cv=content.CV,
            news=content.NEWS,
            news_empty=content.NEWS_EMPTY,
            teaching=content.TEACHING,
            join=content.JOIN,
            pubs=pubs,
            page_title=title,
            page_file=out_name,
            build_date=date.today().isoformat(),
        )
        target = ROOT / out_name
        target.write_text(html, encoding="utf-8", newline="\n")
        written.append(target)

    # Stylesheet: copied rather than inlined so browsers can cache it.
    css_out = ROOT / "stylesheets" / "site.css"
    css_out.parent.mkdir(exist_ok=True)
    shutil.copyfile(SRC / "static" / "css" / "site.css", css_out)
    written.append(css_out)

    # .nojekyll stops GitHub Pages from running these files through Jekyll.
    nojekyll = ROOT / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.write_text("", encoding="utf-8")
        written.append(nojekyll)

    return written


# ---------------------------------------------------------------------------
# Link checking
# ---------------------------------------------------------------------------
_LOCAL_REF = re.compile(r'(?:href|src)="(?!https?:|mailto:|#)([^"]+)"')


def check_links() -> int:
    problems = 0
    for page in ROOT.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        for ref in set(_LOCAL_REF.findall(text)):
            path = (ROOT / ref.split("#")[0].split("?")[0]).resolve()
            if not path.exists():
                print(f"  BROKEN  {page.name} -> {ref}")
                problems += 1
    print("  no broken local links" if not problems else f"  {problems} broken link(s)")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true", help="serve the site after building")
    ap.add_argument("--check", action="store_true", help="verify local links after building")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    written = build()
    pubs = load_publications()
    print(f"built {len(written)} file(s); {pubs['count']} publications "
          f"({pubs['first_author_count']} as first author)")

    rc = check_links() if args.check else 0

    if args.serve:
        import functools
        import http.server
        import socketserver

        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"serving http://localhost:{args.port}  (Ctrl+C to stop)")
            httpd.serve_forever()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
