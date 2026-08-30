"""Minimal BibTeX reader for the personal site.

Only supports what this site needs: @article/@inproceedings/@misc entries with
brace-delimited values that may span multiple lines. No dependency beyond the
standard library.
"""

from __future__ import annotations

import re
from pathlib import Path

# LaTeX escapes that show up in Web of Science exports.
_LATEX = {
    r"\&": "&",
    r"\%": "%",
    r"\_": "_",
    r"\$": "$",
    r"{[}": "[",
    r"{]}": "]",
    "{": "",
    "}": "",
}

_ENTRY_START = re.compile(r"^\s*@(\w+)\s*\{\s*([^,]*),\s*$")
_FIELD_START = re.compile(r"^\s*([A-Za-z][\w-]*)\s*=\s*(.*)$")


def _clean(value: str) -> str:
    """Collapse whitespace and unescape the handful of LaTeX bits we care about."""
    value = value.strip().rstrip(",").strip()
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
    for src, dst in _LATEX.items():
        value = value.replace(src, dst)
    return re.sub(r"\s+", " ", value).strip()


def _split_authors(raw: str) -> list[str]:
    """'Yan, Zeyin and Chung, Lung Wa' -> ['Zeyin Yan', 'Lung Wa Chung']."""
    names = []
    for part in re.split(r"\s+and\s+", raw):
        part = part.strip()
        if not part:
            continue
        if "," in part:
            last, first = part.split(",", 1)
            part = f"{first.strip()} {last.strip()}".strip()
        names.append(re.sub(r"\s+", " ", part))
    return names


def parse(path: str | Path) -> list[dict]:
    """Parse a .bib file into a list of dicts with lowercase field names."""
    text = Path(path).read_text(encoding="utf-8-sig")
    entries: list[dict] = []
    entry: dict | None = None
    key: str | None = None
    buf: list[str] = []
    depth = 0

    def flush() -> None:
        nonlocal key, buf, depth
        if entry is not None and key:
            entry[key] = _clean(" ".join(buf))
        key, buf, depth = None, [], 0

    for line in text.splitlines():
        start = _ENTRY_START.match(line)
        if start and depth == 0:
            flush()
            if entry:
                entries.append(entry)
            entry = {"entrytype": start.group(1).lower(), "key": start.group(2).strip()}
            continue

        if entry is None:
            continue

        if depth > 0:  # continuation of a multi-line value
            buf.append(line)
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                flush()
            continue

        if line.strip() == "}":  # end of entry
            flush()
            entries.append(entry)
            entry = None
            continue

        field = _FIELD_START.match(line)
        if field:
            flush()
            key = field.group(1).lower()
            value = field.group(2)
            buf = [value]
            depth = value.count("{") - value.count("}")
            if depth <= 0:
                flush()

    flush()
    if entry:
        entries.append(entry)

    for e in entries:
        e["authors"] = _split_authors(e.get("author", ""))
    return entries


if __name__ == "__main__":  # quick inspection helper
    import sys

    fields = (
        "key entrytype year journal title volume number pages "
        "doi article-number type author"
    ).split()
    for e in parse(sys.argv[1]):
        print("=" * 70)
        for f in fields:
            if e.get(f):
                print(f"{f:15s} {e[f]}")
