# APAC Syndicated Loan Tracker

A weekly dashboard and written briefing on the Asia-Pacific syndicated loan market, with a Taiwan lens. I built it during my summer 2026 capital markets internship at CTBC Bank to learn the market one week at a time.

**Status: archive.** The internship has ended. This repository covers four weekly readings (1, 8, 15 and 22 June 2026) and is no longer updated.

> Please read [NOTICE.md](NOTICE.md). It explains where the market content came from and what the MIT licence does and does not cover.

## What it does

- **Weekly view.** The week's lead theme, what changed since the week before, key numbers, a sortable and filterable deal table, a pricing ladder, risks to watch, a pan-and-zoom world map with one dot per deal, a secondary-market panel showing where loans trade, and a glossary of loan terms.
- **Trends view.** Charts worked out across all weeks from the deal data: volume, sector mix, a theme tracker, CTBC's involvement and a pricing scatter.
- **Present mode and print.** A larger, higher-contrast layout for screen sharing, and a print stylesheet that turns the page into a one-page briefing.
- **One file, no network.** The built dashboard is a single self-contained HTML file. It opens with a double-click and makes no network requests.

## What's in here

| Path | What it is |
|------|------------|
| `dist/CTBC_Loan_Market_Dashboard.html` | The built dashboard, one self-contained file. It is generated from `src/`, so don't edit it by hand. |
| `src/template.html` | All the CSS, JavaScript and page structure, with a single marker where the build injects the data. |
| `src/data/` | One JSON file per week (`jun1.json`, `jun8.json`, `jun15.json`, `jun22.json`), plus `shared.json` for the cross-week panels and `world_land.json` for the map's land outlines. |
| `tools/` | `build.mjs` (the build), `build.py` (the same build without Node), `test.mjs` (a jsdom smoke test) and `extract.py` (the one-off script that split the original single-file dashboard into `src/`). |
| `CTBC_Loan_Market_Briefing.md` | The written briefing. This Markdown file is the source, and the `.docx` is generated from it. |
| `CTBC_Loan_Market_Deck.pptx` | The slide deck that went with the briefing. |
| `Weekly_Update_Runbook.md` | How the weekly refresh worked. |
| `MAP_FEATURE.md` | Design notes for the deal map. |
| `CLAUDE.md` | Project context for working on the code with Claude. |

## Build it

```bash
npm install          # once, pulls jsdom for the test
npm run build        # bundle src/ into dist/CTBC_Loan_Market_Dashboard.html
npm test             # jsdom smoke test: every week renders and switches
npm run verify       # build and test in one go
```

No Node? `python3 tools/build.py` produces the same output.

## Preview it

After building, double-click `dist/CTBC_Loan_Market_Dashboard.html` to open it in a browser. To serve the folder instead:

```bash
python3 -m http.server 8080
# then open http://localhost:8080/dist/CTBC_Loan_Market_Dashboard.html
```

For live reload while editing, the VS Code Live Server extension works on `src/template.html`. The template shows the page frame but no data until you build.

## How it is organised

Data is kept apart from presentation.

- **To change the data,** edit the JSON files in `src/data/`. Each week is one file shaped `{key, tab, date, week: {deals, kpis, whatsnew, ladder, risks, ...}}`. `shared.json` holds the panels that span weeks.
- **To change the look or behaviour,** edit `src/template.html` (CSS and plain JavaScript, no framework).
- **To add a week,** copy a sibling file to `src/data/<week>.json`, set its `key`, `tab` and `date`, and rebuild. The build sorts the date toggle by `date`, so no other file changes.

Then run `npm run build`.

## Regenerate the Word briefing

```bash
pandoc CTBC_Loan_Market_Briefing.md -o CTBC_Loan_Market_Briefing.docx --toc --toc-depth=2
```

## How the weekly refresh worked

Each Monday a scheduled Claude task read that week's Asia-Pacific loan coverage, wrote a new `src/data/<week>.json`, rebuilt the dashboard and refreshed the briefing. `Weekly_Update_Runbook.md` has the details. The publications it read are licensed and were never part of this repository.

## Licence

The code is under the MIT licence (see [LICENSE](LICENSE)). The market content and data are not. See [NOTICE.md](NOTICE.md).
