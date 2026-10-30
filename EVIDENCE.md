# Right-sidebar compact-mode toggle validation

Source: zen-browser/desktop, dev 3fea9dc39820943a91b84af402165897e98474f3, patched commit 8b98aa2e5c468c41be676a818105022f6d7f3ab9.
Platform: Fedora 44 x86_64; Firefox 159 engine; local unofficial Zen development build (the default branding calls it Nightly).

## Build and tests

Full source build: npm run build -- --jobs 12 (passed, about 21 minutes).
UI rebuilds after switching between original/patched styles: npm run build:ui (passed).
Browser-chrome suite: npm test -- compact_mode --headless (33 checks, 4 tests, 0 unexpected results).
ESLint on the new source test and stylelint on both changed stylesheets: passed.

The same regression test fails against the original CSS at sidebar widths 240 and 320 px, with the hide-window-controls preference both enabled and disabled: four horizontal-position assertions fail (164/244 px). It passes all four configurations with the patch (at most 1 CSS px).

## Screenshots

Unedited full-window PNG captures of the actual local Zen executable, running on Xvfb, using Marionette in chrome context. These are not an HTML mockup. A normal Settings tab is open. Fresh isolated profiles use identical preferences and a 1280x800 window. The script invokes the same command as the compact-mode toolbar button.

before-* uses both unmodified dev stylesheets; after-* uses both patched stylesheets. Each sequence opens, closes, and reopens the sidebar. The compact-mode toggle is the split-panel icon in the upper-right part of the window. Raw button coordinates are in the metrics JSON files.

Captured at the default 186px sidebar width:
- Before: expanded x=1099, compact x=1209, reopened x=1099.
- After: expanded x=1245, compact x=1246, reopened x=1245.

Screenshots are published on this separate evidence branch to keep binary evidence out of the source PR.
Only Linux was built and tested; no Windows or macOS build is claimed.
