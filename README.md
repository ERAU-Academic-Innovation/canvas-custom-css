# Canvas Custom CSS — ERAU Academic Innovation

Custom CSS stylesheets used to theme Embry-Riddle Worldwide online courses. The canvas-ww.css file is uploaded to the Canvas LMS Theme Editor, and allows instructional dersigners to apply one of several Embry-Riddle themes with branded color palettes and layout tweaks on top of Cidilabs DesignPLUS.

## Repository Contents

| File | Purpose |
|---|---|
| `canvas-ww.css` | Stylesheet uploaded to the Worldwide (WW) campus Canvas subaccount. |
| `theme-erau-base.css` | Core/base stylesheet for ERAU branded themes. Required as a foundation for the other ERAU theme color variants. |
| `theme-erau-beyond.css` | "Beyond" color theme. |
| `theme-erau-beyond-altitude.css` | "Beyond" theme, Altitude accent variant. |
| `theme-erau-beyond-sunrise.css` | "Beyond" theme, Sunrise accent variant. |
| `theme-erau-black.css` | "Black" color theme. |
| `theme-erau-black-altitude.css` | "Black" theme, Altitude accent variant. |
| `theme-erau-black-sunrise.css` | "Black" theme, Sunrise accent variant. |
| `theme-erau-black-unrivaled.css` | "Black" theme, Unrivaled accent variant. |
| `theme-erau-unrivaled.css` | "Unrivaled" color theme. |
| `theme-erau-unrivaled-altitude.css` | "Unrivaled" theme, Altitude accent variant. |
| `theme-erau-unrivaled-sunrise.css` | "Unrivaled" theme, Sunrise accent variant. |
| `designtools-customizations.css` | Styling for content created with ERAU's Design Tools page-building blocks (banners, cards, buttons, etc.). |

## Usage

These stylesheets are meant to be loaded through Canvas's Theme Editor, not linked directly from GitHub:

1. Log in to Canvas as an admin and go to **Admin → Themes**.
2. Select **Open in Theme Editor**.
3. Go to the **Upload** tab (or the **Advanced** panel that exposes "Add JS/CSS Files").
4. Upload `canvas-ww.css`.
5. Preview the changes, then **Save** and **Publish** the theme when you're satisfied.

## Contributing

1. Create a branch for your change.
2. Test changes in a Canvas beta/test environment before merging to `main`, since these styles apply instance-wide once published.
3. Open a pull request describing what changed and why.
