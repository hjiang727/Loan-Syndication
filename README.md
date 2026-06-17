# CTBC APAC Syndicated Loan Tracker

Internal **confidential** weekly dashboard + briefing on the Asia-Pacific syndicated loan market, with a Taiwan / CTBC lens, for the CTBC corporate-banking desk.

> ⚠️ **Read [NOTICE.md](NOTICE.md) before sharing or hosting.** This is confidential and built partly from licensed IFR / LSEG LPC material — it must stay on CTBC-controlled, access-restricted systems.

## What's in here

| File | What it is |
|------|------------|
| `CTBC_Loan_Market_Dashboard.html` | The interactive dashboard — **one self-contained file**, no internet needed. Toggle between weeks (Jun 1 / Jun 15) with the date control at the top right. |
| `CTBC_Loan_Market_Briefing.md` | The written briefing — **this Markdown file is the source of truth**. |
| `CTBC_Loan_Market_Briefing.docx` | Word version, generated from the Markdown (see below). |
| `CTBC_Loan_Market_Deck.pptx` | Slide deck for the supervisor discussion. |
| `Weekly_Update_Runbook.md` | How the weekly refresh works. |

## Preview it locally (no hosting needed)

The dashboard is a single self-contained file, so the simplest option is to **double-click `CTBC_Loan_Market_Dashboard.html`** — it opens in your browser.

For live-reload while you edit, in VS Code:
1. Install the **Live Server** extension (VS Code will offer it from `.vscode/extensions.json`).
2. Right-click `CTBC_Loan_Market_Dashboard.html` → **Open with Live Server**.

Or run a tiny local server from this folder:
```bash
python3 -m http.server 8080
# then open http://localhost:8080/CTBC_Loan_Market_Dashboard.html
```
All of these are **local only** — nothing is published.

## Editing the dashboard

It's plain HTML + CSS + vanilla JavaScript, no build step. All the data lives in the **`WEEKS` object** inside the `<script>` near the bottom of the HTML — one entry per week, each with `deals`, `kpis`, `whatsnew`, `ladder`, `risks`, etc. To add a week, copy an existing block, edit the values, and add its `{key,label}` to the `ORDER` array.

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
