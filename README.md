# yanjordan.github.io

Academic website of Zeyin Yan — Institute of Nanotechnology and Intelligence (inAI), Jinan University.
Published by GitHub Pages from the repository root.

## How it works

The HTML at the repository root is **generated**. Do not edit it by hand; edit the
sources in `src/` and rebuild.

```
src/
  content.py            all prose, links, CV entries, nav — the file you edit most
  data/publications.bib the single source of truth for every publication
  templates/            Jinja2 templates (base.html + one per page)
  static/css/site.css   the stylesheet
  bibparse.py           minimal BibTeX reader (stdlib only)
  optimize_images.py    figure -> WebP
  make_favicon.py       favicon.svg / favicon.ico / apple-touch-icon.png
build.py                the generator
```

Publications are rendered from `src/data/publications.bib` only, so a citation can
no longer drift out of sync with the journal record by hand-editing HTML.

## Rebuilding

```bash
python build.py            # regenerate the HTML at the repository root
python build.py --check    # also report broken local links
python build.py --serve    # build, then serve at http://localhost:8000
```

Occasional maintenance:

```bash
python src/optimize_images.py --write   # regenerate .webp after adding a figure
python src/make_favicon.py              # regenerate the favicons
```

Then commit the generated HTML together with the source change. There is no CI
step and no Ruby/Jekyll toolchain: `.nojekyll` tells GitHub Pages to serve the
files as they are.

## Adding a publication

1. Append the entry to `src/data/publications.bib`. Beyond the standard BibTeX
   fields, these custom ones are understood:

   | field | meaning |
   |---|---|
   | `abbrev` | journal abbreviation used in the citation line |
   | `local_pdf`, `local_si` | paths to the PDF and supporting information |
   | `preprint_pdf`, `preprint_si` | preprint versions |
   | `local_image` | graphical abstract |
   | `code_url` | repository for the accompanying code |
   | `selected` | `true` to feature it on the home page |
   | `equal_contrib` | `true` to mark joint first authorship (‡) |
   | `note` | one-paragraph plain-language summary |

2. Drop the PDF/figure into `research/`.
3. `python src/optimize_images.py --write`
4. `python build.py --check`
