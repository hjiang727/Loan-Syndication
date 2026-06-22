# CTBC APAC Syndicated Loan Tracker

Internal **confidential** weekly dashboard + briefing on the Asia-Pacific syndicated loan market, with a Taiwan / CTBC lens, for the CTBC corporate-banking desk.

> ⚠️ **Read [NOTICE.md](NOTICE.md) before sharing or hosting.** This is confidential and built partly from licensed IFR / LSEG LPC material — it must stay on CTBC-controlled, access-restricted systems.

## What's in here

| File | What it is |
|------|------------|
| `dist/CTBC_Loan_Market_Dashboard.html` | The interactive dashboard — **one self-contained file**, no internet needed. **Built from `src/` — don't hand-edit.** |
| `src/` | Editable source: `template.html` (CSS + JS + structure) and `data/*.json` (one small file per week, plus `shared.json` + `world_land.json`). |
| `tools/`, `package.json` | Build (`npm run build`) + jsdom smoke test (`npm test`). |
| `CTBC_Loan_Market_Briefing.md` | The written briefing — **this Markdown file is the source of truth**. |
| `CTBC_Loan_Market_Briefing.docx` | Word version, generated from the Markdown (see below). |
| `CTBC_Loan_Market_Deck.pptx` | Slide deck for the supervisor discussion. |
| `Weekly_Update_Runbook.md` | How the weekly refresh works. |

## Build it

```bash
npm install          # once — pulls jsdom for the test
npm run build        # bundle src/ -> dist/CTBC_Loan_Market_Dashboard.html
npm test             # jsdom smoke test (every week renders & switches)
npm run verify       # build + test in one go
```
No Node? `python3 tools/build.py` is a drop-in build (same output).

## Preview it locally (no hosting needed)

After building, **double-click `dist/CTBC_Loan_Market_Dashboard.html`** — it opens in your browser. For live-reload while editing, use the VS Code **Live Server** extension on `src/template.html` (note: the template shows the page chrome but not the data until you build), or serve the folder:
```bash
python3 -m http.server 8080
# then open http://localhost:8080/dist/CTBC_Loan_Market_Dashboard.html
```
All of these are **local only** — nothing is published.

## Editing the dashboard

Data is separated from presentation. **To change the data**, edit the small JSON files in `src/data/` (one per week: `jun15.json` = `{key, tab, date, week:{deals, kpis, whatsnew, ladder, risks, …}}`; plus `shared.json` for the cross-week panels). **To change look/behaviour**, edit `src/template.html` (CSS + vanilla JS). Then `npm run build`. **To add a week**, drop a new `src/data/<week>.json` (copy a sibling, set `key`/`tab`/`date`) and rebuild — the build re-sorts the date toggle by `date` automatically; no other file to touch.

## Regenerate the Word briefing (optional)

The `.docx` is generated from `CTBC_Loan_Market_Briefing.md`:
```bash
pandoc CTBC_Loan_Market_Briefing.md -o CTBC_Loan_Market_Briefing.docx --toc --toc-depth=2
```

## Version control (local)

```bash
git init
git add .
git commit -m "Initial commit: CTBC loan tracker dashboard + briefing"
```
Commit as you work. **Do not add a public/personal remote** — see [NOTICE.md](NOTICE.md). The live, access-controlled link is created by **CTBC**, on CTBC systems; you build and maintain the files here.

## Weekly refresh

A scheduled task can refresh this each Monday from the new IFR / LSEG reading (adds a new selectable week to the dashboard and refreshes the briefing). Drop the new reading PDF into the parent `Finance` folder. See `Weekly_Update_Runbook.md`.
