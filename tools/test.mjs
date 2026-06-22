// Smoke test: load the built dist in jsdom, render every week, switch between them, exercise the table.
// Run: npm install   (once, pulls jsdom)   then:   node tools/test.mjs   (or: npm test)
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(ROOT, "dist/CTBC_Loan_Market_Dashboard.html");
if (!existsSync(dist)) { console.error("dist not built — run `npm run build` first."); process.exit(1); }

let fails = 0;
const ok = (cond, msg) => { console.log((cond ? "  ✓ " : "  ✗ ") + msg); if (!cond) fails++; };

const dom = new JSDOM(readFileSync(dist, "utf8"), { runScripts: "dangerously", pretendToBeVisual: true });
const { window } = dom;
const doc = window.document;
const $ = (s) => doc.querySelector(s);
const $$ = (s) => [...doc.querySelectorAll(s)];

console.log("Loading dashboard…");
ok($("#kpis .kpi") != null, "dashboard scripts ran without throwing");

// every week renders + the date toggle switches
const weekBtns = $$("#dateseg button");
ok(weekBtns.length >= 1, `date toggle lists ${weekBtns.length} reading(s)`);
for (const b of weekBtns) {
  b.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  const k = b.dataset.k;
  ok($$("#rows tr.drow").length > 0, `week ${k}: deal rows render (${$$("#rows tr.drow").length})`);
  ok($$("#kpis .kpi").length === 5, `week ${k}: 5 KPI cards`);
  ok($("#mapsvg svg") != null, `week ${k}: deal map renders`);
}

// table interactions on the current (latest) week
const row = $("#rows tr.drow");
row.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
ok(row.getAttribute("aria-expanded") === "true", "row expands on click (accessible detail)");

const th = $('thead th[data-k="borrower"]');
th.dispatchEvent(new window.KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
ok(["ascending", "descending"].includes(th.getAttribute("aria-sort")), "header sorts via keyboard");

// filter narrows the table
const only = $("#ctbcOnly"); only.checked = true; only.dispatchEvent(new window.Event("input", { bubbles: true }));
const ctbcRows = $$("#rows tr.drow").length;
only.checked = false; only.dispatchEvent(new window.Event("input", { bubbles: true }));
ok(ctbcRows > 0 && ctbcRows < $$("#rows tr.drow").length, `CTBC-only filter narrows the table (${ctbcRows} of ${$$("#rows tr.drow").length})`);

// trends + secondary panels present
$("#viewseg button[data-v='trends']").dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
ok($$("#trendsView svg").length >= 4, `Trends view renders charts (${$$("#trendsView svg").length} svgs)`);
ok($$("#secDist div[title]").length > 0 && $$("#secLinks .card").length > 0, "secondary distribution + cross-link render");

console.log(fails ? `\n✗ ${fails} check(s) failed` : "\n✓ all checks passed");
process.exit(fails ? 1 : 0);
