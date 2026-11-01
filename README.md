# Existing left/right compact-mode toggle behavior

Captured on 2026-11-01 using the actual local Zen browser, Firefox 159, Fedora 44 x86_64 and Xvfb. The default unofficial build uses Nightly branding.

Both changed stylesheets were restored to unmodified dev commit 3fea9dc39820943a91b84af402165897e98474f3 and rebuilt with npm run build:ui before these captures. The PR's CSS fix is not applied to either side of this comparison.

Fresh isolated profiles, same 1280x800 window, Settings tab, expanded sidebar, multiple-toolbar layout, compact mode hides the sidebar only. The only preference changed between runs is zen.tabs.vertical.right-side. capture.py invokes the real compact-mode toolbar command. PNGs are unedited full-window captures.

The split-panel icon near the outside top corner is the compact-mode toggle.
- Left: expanded x=5, compact x=1, reopened x=5. It stays near the outside edge, with a 4px padding change.
- Right: expanded x=1099, compact x=1209, reopened x=1099. It jumps horizontally by 110px.

Both sequences include expanded, compact and reopened states; raw geometry is recorded in the JSON files.

Related PR: https://github.com/zen-browser/desktop/pull/16282
