# Weekly Loan-Tracker Update — How It Works

A small system that keeps your CTBC loan-market study materials current every week.

## The cadence

A new IFR / LSEG LPC **Asia-Pacific syndicated loans tracker** comes out every **Monday**. This setup refreshes your briefing and dashboard from each new edition.

**Your only job each week:** drop the new tracker PDF into this folder
(`/Users/henryjiang/Documents/Claude/Projects/Finance/`). That's it.

## What runs automatically

A scheduled task — **"weekly-loan-tracker"** — fires **every Monday (~9:00 AM)**. When it runs it:

1. Looks for a **new** tracker PDF in this folder (newer than the dashboard's current "Week of" date).
2. If it finds one, it:
   - archives the current briefing + dashboard into `archive/<date>/`,
   - reads the new PDF, builds that week's **deal list**, and refreshes market figures with a few web checks,
   - **writes a new `src/data/<week>.json`** for the reading and **rebuilds `dist/`** (`npm run build`) — the new reading becomes a selectable week (prior weeks stay; switch with the date toggle), newest shown by default,
   - refreshes **`CTBC_Loan_Market_Briefing.docx`** for the new week,
   - fills the **"What's new"** panel by diffing against the previous week (debuts, upsizes, new mandates, new lead themes, pricing moves),
   - refreshes the **Trends** (cross-week) view — the charts and KPIs recompute automatically, and the `TRENDS_NARRATIVE` commentary is rewritten each week to fold in the new reading,
   - posts a short summary and shows you the updated files.
3. If it finds **no** new PDF, it changes nothing and just nudges you to add this week's reading.

> Scheduled tasks run while the Claude app is open. If the app was closed when it was due, it runs on next launch — so don't worry if you miss a Monday.

## Standing rules baked in

- **"CBC" / "CBC Bank" = CTBC.** Always treated as CTBC (not OCBC or ICBC, which are different banks).
- **Taiwan-centric, CTBC-focused lens**, with every loan term explained (you're still building the vocabulary).
- **No invented deals** — only what's in the reading, plus clearly-sourced market context.

## Doing it manually / changing it

- **Refresh now:** add the PDF, then open the **Scheduled** section in the sidebar and hit **Run now** on "weekly-loan-tracker" — or just ask me here: *"refresh the loan tracker with this week's reading."*
- **Change the day/time:** ask me, e.g. *"run the loan tracker task Monday at 5pm instead."*
- **Want the slide deck refreshed too?** Just ask — the deck (`CTBC_Loan_Market_Deck.pptx`) isn't auto-rebuilt by default, but I can regenerate it any week.

## Files in this folder

| File | What it is |
|---|---|
| `dist/CTBC_Loan_Market_Dashboard.html` | Living dashboard (built) — open in a browser; **date toggle** (top right) switches weeks |
| `src/data/*.json` | The editable per-week data the build bundles into the dashboard |
| `CTBC_Loan_Market_Briefing.docx` | Full written briefing (Word) |
| `CTBC_Loan_Market_Briefing.md` | Same briefing in Markdown (source) |
| `CTBC_Loan_Market_Deck.pptx` | Slide deck for the supervisor discussion |
| `Weekly_Update_Runbook.md` | This file |
| `archive/<date>/` | Prior weeks' briefing + dashboard (created automatically) |

*Set up June 2026. Tracked editions so far: weeks of Mon 1, 8, 15 and 22 Jun 2026 (switch with the date toggle).*
