#!/usr/bin/env python3
"""Regenerate the DesignPLUS copy-paste doc pages (docs/*.html) from
custom-themes.manifest.css and the theme-erau-*.css files' actual class
names. Run after editing the manifest or any theme file, or after
changing a PAGE config below."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "custom-themes.manifest.css"
DOCS = ROOT / "docs"

IMPORT_RE = re.compile(r"@import url\((theme-[A-Za-z0-9-]+\.css)\);")
WRAPPER_CLASS_RE = re.compile(r"\.([a-z0-9]+(?:-[a-z0-9]+)*)-wrapper\b")

COLOR_ORDER = ["unrivaled", "beyond", "black", "sunrise", "grey", "altitude"]
COLOR_HEADERS = {
    "unrivaled": "Unrivaled Blue",
    "beyond": "Beyond Blue",
    "black": "Black",
    "sunrise": "Sunrise Yellow",
    "grey": "Grey",
    "altitude": "Altitude Blue",
}

# One-off themes built for a specific outside sponsor/org rather than as a
# general ERAU color option. Filed under their own "Sponsored Themes"
# section instead of grouped by ERAU color. Keyed by the theme's *-wrapper
# class slug; add an entry here for each new sponsored theme file.
SPONSORED_THEME_NAMES = {
    "her": "hER Women's Professional Network",
}


def load_theme_rows():
    """Parse the manifest + each theme file's actual .*-wrapper class to
    build the canonical list of {kind, name, slug, color} theme rows,
    in manifest (load) order."""
    manifest_text = MANIFEST.read_text()
    rows = []
    for fname in IMPORT_RE.findall(manifest_text):
        if fname == "theme-erau-base.css":
            continue
        if fname.startswith("theme-erau-solid-"):
            kind = "solid"
        elif fname.startswith("theme-erau-gradient-"):
            kind = "gradient"
        elif fname.startswith("theme-erau-wing-"):
            kind = "wing"
        elif fname.startswith("theme-erau-"):
            sys.exit(f"error: unrecognized theme file in manifest: {fname}")
        else:
            kind = "sponsored"

        theme_file = ROOT / fname
        if not theme_file.exists():
            sys.exit(f"error: {fname} referenced in manifest but not found")

        match = WRAPPER_CLASS_RE.search(theme_file.read_text())
        if not match:
            sys.exit(f"error: no *-wrapper class found in {fname}")
        slug = match.group(1)

        if kind == "sponsored":
            if slug not in SPONSORED_THEME_NAMES:
                sys.exit(f"error: {fname} has no SPONSORED_THEME_NAMES entry for slug '{slug}'")
            name = SPONSORED_THEME_NAMES[slug]
            color = None
        elif kind == "solid":
            name = " ".join(p.capitalize() for p in slug.split("-"))
            color = slug.split("-")[0]
        else:
            rest = slug[len(kind) + 1:]
            parts = rest.split("-")
            name = f"{kind.capitalize()} {'-'.join(p.capitalize() for p in parts[:-1])} {parts[-1].capitalize()}"
            color = parts[0]

        rows.append({"kind": kind, "name": name, "slug": slug, "color": color})
    return rows


def group_by_color(rows):
    groups = []
    for color in COLOR_ORDER:
        color_rows = [r for r in rows if r["kind"] != "sponsored" and r["color"] == color]
        if color_rows:
            groups.append({"header": COLOR_HEADERS[color], "rows": color_rows})

    sponsored_rows = [r for r in rows if r["kind"] == "sponsored"]
    if sponsored_rows:
        groups.append({"header": "Sponsored Themes", "rows": sponsored_rows})

    return groups


# ---------------------------------------------------------------------------
# Page configs — add a new dict here for each new DesignPLUS content-block
# table. `row_cells(row)` maps a theme row to that page's column values.
# ---------------------------------------------------------------------------

PAGES = [
    {
        "filename": "designplus-themes.html",
        "page_title": "DesignPLUS ERAU Theme Content Blocks",
        "canvas_area": "ERAU Themes",
        "block_intro": (
            'Add your own custom themes by adding classes to the table.'
            '<strong><mark class="badge rounded-pill cp-bg-success"></mark></strong>'
        ),
        "columns": [
            "Theme Name",
            "Heading Styles Classes",
            "Banner Title Classes",
            "Link Grid/Nav Classes",
            "Image Classes",
            "Default Banner Image",
            "Active",
        ],
        "row_cells": lambda r: [
            r["name"],
            f'dp-wrapper erau-wrapper {r["slug"]}-wrapper',
            f'dp-header erau-header {r["slug"]}-header',
            f'container-fluid dp-link-grid erau-link-grid {r["slug"]}-link-grid',
            "",
            "",
            "Y",
        ],
        "markdown": {
            "filename": "designplus-themes.md",
            "title": "DesignPLUS ERAU Theme Table",
            "intro": (
                'Reference table for the "ERAU Themes" content blocks in the DesignPLUS '
                'settings course. For pasting into Canvas, use the '
                '[copy-paste page](https://erau-academic-innovation.github.io/canvas-custom-css/docs/designplus-themes.html) '
                'instead — its **Copy Content Block** buttons include the required '
                '`div.dp-content-block` wrapper, which a table copied from this rendered '
                "markdown does not. This file exists for looking up or verifying a theme's "
                "exact classes directly on GitHub.\n\n"
                "Themes are grouped by their primary/dominant color so instructional "
                "designers can find every theme that pairs with a given banner image color, "
                "regardless of whether it's a solid, gradient, or wing (hard-edge split) "
                "treatment. Two-color gradient/wing themes are filed under their "
                'first-listed (dominant) color only — e.g. "Black-Beyond" lives under '
                'Black, "Beyond-Black" lives under Beyond — so no theme is listed twice. '
                'One-off themes built for a specific outside sponsor rather than as a '
                'general ERAU color option are filed under their own "Sponsored Themes" '
                "section instead.\n\n"
                "This file is generated from `custom-themes.manifest.css` and the actual "
                "`.css` files' class names by `scripts/generate_docs.py`, and regenerates "
                "automatically via CI whenever theme variants change — see "
                "[`README.md`](../README.md) for the underlying naming conventions."
            ),
        },
    },
    {
        # Banner header: the main-page header where an image sits alongside
        # the heading text and other content.
        "filename": "designplus-banner-header-styles.html",
        "page_title": "DesignPLUS ERAU Banner Header Style Content Blocks",
        "canvas_area": "ERAU Styles",
        "block_intro": None,
        "columns": [
            "Style Name",
            "CSS Classes to apply to Banner Titles",
            "Active",
        ],
        "row_cells": lambda r: [
            r["name"],
            f'erau-header {r["slug"]}-header',
            "Y",
        ],
    },
    {
        "filename": "designplus-link-grid-styles.html",
        "page_title": "DesignPLUS ERAU Link Grid Style Content Blocks",
        "canvas_area": "ERAU Styles",
        "block_intro": None,
        "columns": [
            "Style Name",
            "CSS Classes to apply to Link Grid",
            "Active",
        ],
        "row_cells": lambda r: [
            r["name"],
            f'erau-link-grid {r["slug"]}-link-grid',
            "Y",
        ],
    },
    {
        # Text heading styles: generic H3/H4/H5 text styling used
        # throughout the page body, distinct from the banner header above.
        "filename": "designplus-text-header-styles.html",
        "page_title": "DesignPLUS ERAU Text Header (H3–H5) Style Content Blocks",
        "canvas_area": "ERAU Styles",
        "block_intro": "The following table includes classes for new DesignPLUS styles.",
        "columns": [
            "Style Name",
            "CSS Classes to apply to wrapper",
            "Active",
        ],
        "row_cells": lambda r: [
            r["name"],
            f'erau-wrapper {r["slug"]}-wrapper',
            "Y",
        ],
    },
]


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<style>
  :root {{
    color-scheme: light dark;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.5;
  }}
  h1 {{ font-size: 1.5rem; }}
  .instructions {{
    background: rgba(127,127,127,0.1);
    border: 1px solid rgba(127,127,127,0.3);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 2rem;
  }}
  .instructions ol {{ margin: 0.5rem 0 0; padding-left: 1.25rem; }}
  section.group {{
    border: 1px solid rgba(127,127,127,0.3);
    border-radius: 8px;
    padding: 1rem 1.25rem 1.25rem;
    margin-bottom: 1.5rem;
  }}
  .group-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }}
  .group-header h2 {{ margin: 0; font-size: 1.2rem; }}
  button.copy-btn {{
    font-size: 0.9rem;
    padding: 0.4rem 0.9rem;
    border-radius: 6px;
    border: 1px solid rgba(127,127,127,0.4);
    background: rgba(127,127,127,0.08);
    cursor: pointer;
  }}
  button.copy-btn:hover {{ background: rgba(127,127,127,0.18); }}
  button.copy-btn.copied {{ background: #2e7d32; color: white; border-color: #2e7d32; }}
  table.preview {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.75rem;
    font-size: 0.85rem;
  }}
  table.preview th, table.preview td {{
    border: 1px solid rgba(127,127,127,0.3);
    padding: 0.35rem 0.5rem;
    text-align: left;
    vertical-align: top;
  }}
  table.preview th {{ background: rgba(127,127,127,0.1); }}
  table.preview tr:nth-child(even) td {{ background: rgba(127,127,127,0.05); }}
  code {{ font-size: 0.85em; }}
  #copy-all-wrap {{ margin-bottom: 1.5rem; }}
</style>
</head>
<body>
<h1>{page_title}</h1>
<div class="instructions">
  For each section below, click <strong>Copy Content Block</strong>, then in Canvas's DesignPLUS course:
  <ol>
    <li>Open the settings course page and switch to the HTML/source editor for the "{canvas_area}" area.</li>
    <li>Paste the copied block where you want that color group to appear (it already includes its own heading and table &mdash; no need to create a block or heading manually).</li>
    <li>Save.</li>
  </ol>
  This page is generated from <code>custom-themes.manifest.css</code> and the theme CSS files' actual class names, so it always reflects what's really shipped. It regenerates automatically when those files change (see <code>scripts/generate_docs.py</code>).
</div>
<div id="copy-all-wrap">
  <button class="copy-btn" id="copy-all-btn">Copy All Content Blocks</button>
</div>
<div id="groups"></div>

<script id="page-data" type="application/json">{page_data_json}</script>
<script>
const PAGE = JSON.parse(document.getElementById('page-data').textContent);
const COLUMNS = PAGE.columns;
const GROUPS = PAGE.groups;
const BLOCK_INTRO = PAGE.blockIntro;

function rowHtml(cells) {{
  const tds = cells.map(c => `                        <td>${{c}}</td>`).join('\\n');
  return `                    <tr>\\n${{tds}}\\n                    </tr>`;
}}

function blockHtml(group) {{
  const rows = group.rows.map(r => rowHtml(r.cells)).join('\\n');
  const ths = COLUMNS.map(c => `                        <th scope="col">${{c}}</th>`).join('\\n');
  const introHtml = BLOCK_INTRO ? `\\n        <p>${{BLOCK_INTRO}}</p>` : '';
  return `<div class="dp-content-block">
        <h3>${{group.header}}</h3>${{introHtml}}
        <div class="dp-table-scroll">
            <table class="table table-striped" data-active-table="true">
                <thead>
                    <tr>
${{ths}}
                    </tr>
                </thead>
                <tbody class="">
${{rows}}
                </tbody>
            </table>
        </div>
    </div>`;
}}

function copyText(text, btn) {{
  const onSuccess = () => {{
    const original = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = original; btn.classList.remove('copied'); }}, 1500);
  }};
  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(text).then(onSuccess).catch(() => fallbackCopy(text, onSuccess));
  }} else {{
    fallbackCopy(text, onSuccess);
  }}
}}

function fallbackCopy(text, onSuccess) {{
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {{ document.execCommand('copy'); onSuccess(); }} catch (e) {{ alert('Copy failed — please copy manually.'); }}
  document.body.removeChild(ta);
}}

const container = document.getElementById('groups');
GROUPS.forEach(group => {{
  const section = document.createElement('section');
  section.className = 'group';

  const header = document.createElement('div');
  header.className = 'group-header';
  header.innerHTML = `<h2>${{group.header}}</h2>`;

  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copy Content Block';
  btn.addEventListener('click', () => copyText(blockHtml(group), btn));
  header.appendChild(btn);

  section.appendChild(header);

  const table = document.createElement('table');
  table.className = 'preview';
  const theadHtml = '<thead><tr>' + COLUMNS.map(c => `<th>${{c}}</th>`).join('') + '</tr></thead>';
  table.innerHTML = theadHtml;
  const tbody = document.createElement('tbody');
  group.rows.forEach(r => {{
    const tr = document.createElement('tr');
    tr.innerHTML = r.cells.map(c => `<td>${{c}}</td>`).join('');
    tbody.appendChild(tr);
  }});
  table.appendChild(tbody);
  section.appendChild(table);

  container.appendChild(section);
}});

document.getElementById('copy-all-btn').addEventListener('click', (e) => {{
  const all = GROUPS.map(blockHtml).join('\\n\\n');
  copyText(all, e.target);
}});
</script>
</body>
</html>
"""


def render_page(page, groups):
    page_data = {
        "columns": page["columns"],
        "blockIntro": page["block_intro"],
        "groups": [
            {
                "header": g["header"],
                "rows": [{"cells": page["row_cells"](r)} for r in g["rows"]],
            }
            for g in groups
        ],
    }
    return PAGE_TEMPLATE.format(
        page_title=page["page_title"],
        canvas_area=page["canvas_area"],
        page_data_json=json.dumps(page_data),
    )


def render_markdown(page, groups):
    md = page["markdown"]
    lines = [f'# {md["title"]}', "", md["intro"], ""]
    for g in groups:
        lines.append(f'## {g["header"]}')
        lines.append("")
        lines.append("| " + " | ".join(page["columns"]) + " |")
        lines.append("|" + "---|" * len(page["columns"]))
        for r in g["rows"]:
            cells = page["row_cells"](r)
            lines.append("| " + " | ".join(c if c else "" for c in cells) + " |")
        lines.append("")
    return "\n".join(lines)


def main():
    rows = load_theme_rows()
    groups = group_by_color(rows)

    DOCS.mkdir(exist_ok=True)
    for page in PAGES:
        html = render_page(page, groups)
        out_path = DOCS / page["filename"]
        out_path.write_text(html)
        print(f"wrote {out_path.relative_to(ROOT)}")

        if page.get("markdown"):
            md_text = render_markdown(page, groups)
            md_path = DOCS / page["markdown"]["filename"]
            md_path.write_text(md_text)
            print(f"wrote {md_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
