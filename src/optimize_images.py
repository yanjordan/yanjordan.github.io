#!/usr/bin/env python
"""Generate WebP versions of the figures used on the site.

Originals are left untouched: templates emit a <picture> element that serves
WebP to browsers that support it and falls back to the original file otherwise.

    python src/optimize_images.py          # report what would change
    python src/optimize_images.py --write  # actually write the .webp files
    python src/optimize_images.py --write --force   # ignore the mtime cache

Why this matters here: research.html used to pull ~8 MB of PNG/JPG on load
(D2AF.png alone was 2.7 MB) because the figures sit inside collapsed panels that
browsers download anyway.

Notes for future me
-------------------
* ``method=4`` instead of Pillow's slowest ``method=6``: the size difference is
  under 1 % on these figures but the run drops from minutes to seconds, which
  matters because an interrupted run used to leave the output half-written.
* The run is incremental (skips figures whose .webp is newer than the source),
  so re-running is cheap and an interrupted run simply resumes.
* Figures whose WebP comes out *larger* than the original are recorded in
  ``.webp-skip`` so we do not re-encode them on every run.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SKIP_LIST = ROOT / "src" / "data" / "webp-skip.txt"

# Site chrome that must stay in its original format.
EXCLUDE = {"apple-touch-icon.png", "favicon.png"}

MAX_WIDTH = 1400   # figures are displayed at ~700 px; 2x is plenty
QUALITY = 82
METHOD = 4


def targets() -> list[Path]:
    found = [p for p in (ROOT / "research").glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    found += [
        p for p in ROOT.glob("*")
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"} and p.name not in EXCLUDE
    ]
    return sorted(found)


def load_skips() -> set[str]:
    if not SKIP_LIST.exists():
        return set()
    return {
        line.strip()
        for line in SKIP_LIST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def save_skips(names: set[str]) -> None:
    SKIP_LIST.parent.mkdir(parents=True, exist_ok=True)
    SKIP_LIST.write_text(
        "# Figures where WebP came out larger than the original: keep the original.\n"
        + "\n".join(sorted(names))
        + "\n",
        encoding="utf-8",
    )


def human(n: int) -> str:
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1048576:.2f} MB"


def encode(path: Path, out: Path) -> None:
    with Image.open(path) as im:
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > MAX_WIDTH:
            ratio = MAX_WIDTH / im.width
            im = im.resize((MAX_WIDTH, round(im.height * ratio)), Image.LANCZOS)
        tmp = out.with_suffix(".webp.part")
        im.save(tmp, "WEBP", quality=QUALITY, method=METHOD)
    tmp.replace(out)   # atomic: never leave a truncated .webp behind


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write .webp files")
    ap.add_argument("--force", action="store_true", help="re-encode even if up to date")
    args = ap.parse_args()

    skips = load_skips()
    total_before = total_after = 0
    n_new = n_cached = 0

    for path in targets():
        rel = path.relative_to(ROOT).as_posix()
        out = path.with_suffix(".webp")
        before = path.stat().st_size

        if rel in skips and not args.force:
            print(f"  {rel:38s} {human(before):>9s}  (original kept: WebP is larger)")
            if out.exists():
                out.unlink()
            total_before += before
            total_after += before
            continue

        fresh = out.exists() and out.stat().st_mtime >= path.stat().st_mtime
        if fresh and not args.force:
            after = out.stat().st_size
            n_cached += 1
            print(f"  {rel:38s} {human(before):>9s} -> {human(after):>9s}  (cached)")
            total_before += before
            total_after += after
            continue

        if not args.write:
            print(f"  {rel:38s} {human(before):>9s}  (dry run)")
            total_before += before
            total_after += before
            continue

        encode(path, out)
        after = out.stat().st_size
        if after >= before:
            out.unlink()
            skips.add(rel)
            after = before
            print(f"  {rel:38s} {human(before):>9s}  (original kept: WebP is larger)")
        else:
            n_new += 1
            print(f"  {rel:38s} {human(before):>9s} -> {human(after):>9s}  (-{100 * (1 - after / before):.0f}%)")
        total_before += before
        total_after += after

    if args.write:
        save_skips(skips)
    print(f"\n  {n_new} encoded, {n_cached} cached, {len(skips)} kept as original")
    print(f"  payload {human(total_before)} -> {human(total_after)} "
          f"(-{100 * (1 - total_after / total_before):.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
