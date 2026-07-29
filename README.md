# Canvas Custom CSS — ERAU Academic Innovation

Custom CSS stylesheets used to theme Embry-Riddle Worldwide online courses. A single `@import` line is uploaded to the Canvas LMS Theme Editor, pulling in `custom-themes.css`, which allows instructional designers to apply one of several Embry-Riddle themes with branded color palettes and layout tweaks on top of Cidilabs DesignPLUS.

**Scope:** currently installed only at the Worldwide (WW) Canvas subaccount.

## Repository Contents

| File(s) | Purpose |
|---|---|
| `custom-themes.css` | Production bundle. @imports all themes and color variants via the jsDelivr CDN. |
| `custom-themes-dev.css` | Development bundle. Same imports as `custom-themes.css`, but references GitHub Pages instead of the CDN, so changes show up without waiting for the CDN cache to purge. |
| `theme-erau-base.css` | Core/base stylesheet for all ERAU branded themes below. Required as a foundation for every theme variant. |
| `theme-erau-<color>.css`<br>`theme-erau-<color>-<accent>.css` | **Solid themes.** Single brand color (`beyond`, `black`, `unrivaled`) with an optional accent variant (`altitude`, `sunrise`; `black` also has an `unrivaled` accent). |
| `theme-erau-gradient-<color1>-<color2>-<accent>.css` | **Gradient themes.** Soft blend between two brand colors, in the direction `<color1>` → `<color2>` (e.g. `beyond-black`, `black-unrivaled`), with an accent variant (`sunrise`, `altitude`, `grey`). |
| `theme-erau-wing-<color1>-<color2>-<accent>.css` | **Wing themes.** Hard-edge split (no gradient) between two brand colors, same direction/accent naming as the gradient themes above. |

## Usage

These stylesheets are loaded through Canvas's Theme Editor, not linked directly from GitHub.

### Production

Add the following line to the CSS uploaded to the LMS:

```css
@import url(https://cdn.jsdelivr.net/gh/ERAU-Academic-Innovation/canvas-custom-css/custom-themes.css);
```

This pulls all themes and variants from the jsDelivr CDN, which caches releases and does not reflect new commits immediately (see [CDN caching](#cdn-caching-jsdelivr) below).

### Development

Upload `custom-themes-dev.css` itself to the LMS. It references the same themes via GitHub Pages instead of the CDN, so changes to this repo show up faster for testing.

### CDN caching (jsDelivr)

The production import above has no version pin (no `@main`, no tag), so per [jsDelivr's own docs](https://github.com/jsdelivr/jsdelivr#the-file-you-are-linking-doesnt-download), an unpinned URL resolves to the latest tagged release if one exists, otherwise it falls back to the repo's default branch — which is what happens here, since this repo has no git tags. jsDelivr itself flags this pattern ("omit the version completely") as **not recommended for production usage**, mainly because of caching:

- **Branch-referenced files** (our case) are cached on jsDelivr's CDN for **12 hours** before it re-checks GitHub for changes.
- **Tagged releases / commit hashes** are cached effectively forever (1-year headers, permanently stored in S3) — immutable, but predictable.
- **`@latest`/version-aliased URLs** are cached for **7 days**.

So after merging a change to `main`, production Canvas courses can take **up to 12 hours** to pick it up.

**To force an update sooner:** purge the specific file by swapping `cdn.` for `purge.` in its URL and requesting it (e.g. in a browser or via `curl`):

```
https://purge.jsdelivr.net/gh/ERAU-Academic-Innovation/canvas-custom-css/custom-themes.css
```

Note that `custom-themes.css` itself `@import`s the individual `theme-erau-*.css` files, each cached separately — if you only changed one theme file, purge that file's own URL too, not just `custom-themes.css`.

**Alternative:** cut a git tag/release and pin the production import to it (e.g. `.../canvas-custom-css@v1.2.0/custom-themes.css`) for immutable, predictable delivery. The trade-off is that production won't pick up new commits at all until the LMS import line is manually updated to point at a new tag.
