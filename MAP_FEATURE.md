# Feature spec: APAC geography map (bubbles + cross-border flow arcs)

Goal: a self-contained APAC map that shows, for the selected week, **a bubble per country sized by total deal volume** and **teal arcs for CTBC cross-border lending** (Taiwan → borrower country). Turns the country/`amtUSD`/`ctbc` data into a geographic read of the week — and visualises the "Taiwanese banks exporting balance sheet" story.

## Where it lives
- Add a **"Geography" panel** inside the **Weekly** view (it's week-specific), above or below the deal tracker. Render it from a new `renderMap()` called at the end of `renderWeek()` so it updates on every date switch. (Alternative: a 3rd `VIEW` tab "Map" — pick whichever fits the current View-toggle code; a panel in Weekly is simpler.)
- It reflects `W().deals` for the currently selected week.

## Hard constraints (keep these)
- **Self-contained, no CDN.** Inline SVG + ~10 lines of projection math. Do NOT add D3/Leaflet/Chart.js or any external script — the file must still open by double-click, offline, and be email-able.
- **Theme-aware.** All colours via existing CSS vars (`--ctbc`, `--navy`, `--navy2`, `--muted`, `--line`, `--surface`, sector colours from `SECTOR_COL`). Must read in dark mode.
- **Accessible.** Wrap the SVG with `role="img"` + `<title>`/`<desc>`; the deal table stays the accessible data source. Don't encode meaning by colour alone — keep labels.

## 1) Country display points + projection
Add a lookup (keys must match `deal.country` strings exactly) and an equirectangular projection. Bounding box: lon 60→180, lat 50→−50. Use `viewBox="0 0 720 600"`.

```js
const COUNTRY_PT = { // [lon, lat] display points (economic centres, for recognisability)
  "Taiwan":[121.0,23.8], "China":[114.0,32.0], "Hong Kong":[114.2,22.3], "Macau":[113.5,22.2],
  "Japan":[139.0,36.0], "South Korea":[127.5,36.5], "Singapore":[103.8,1.3], "Malaysia":[101.9,3.6],
  "Indonesia":[106.8,-6.2], "Vietnam":[106.5,16.5], "Philippines":[121.0,14.6],
  "Australia":[134.5,-25.0], "New Zealand":[173.0,-41.0], "India":[78.0,22.0], "Papua New Guinea":[144.0,-6.0]
};
const MAP_W=720, MAP_H=600;
function project(lon,lat){ return [ (lon-60)/120*MAP_W, (50-lat)/100*MAP_H ]; }
```
Off-map countries (no entry above): "Chile (via Asia)", "Mauritius", any Africa/"via Asia" — see §5.

## 2) Aggregate + bubbles
```js
function countryAgg(deals){
  const m={};
  for(const d of deals){
    if(!COUNTRY_PT[d.country]) continue;            // off-map handled separately
    const a=m[d.country]||(m[d.country]={usd:0,n:0,ctbc:0,sec:{}});
    a.usd += d.amtUSD||0; a.n++; if(d.ctbc) a.ctbc++;
    a.sec[d.sector]=(a.sec[d.sector]||0)+(d.amtUSD||0);
  }
  return m;
}
```
- **Radius** ∝ √volume (area ∝ value): `r = Math.max(6, Math.min(46, 0.5*Math.sqrt(a.usd)))` — tune the `0.5`.
- **Fill** = colour of the country's dominant sector (max `a.sec`) via `SECTOR_COL`, OR a neutral `var(--navy2)`. Recommended: neutral fill + **teal stroke/glow when `a.ctbc>0`** (`stroke:var(--ctbc); stroke-width:2`) so CTBC countries pop.
- **Label** the country code/name and total (e.g. `Taiwan · US$X.Xbn`) beside the bubble or on hover.

## 3) Cross-border flow arcs (the CTBC story)
Free-text `leads` can't be parsed reliably, so make arcs **opt-in and accurate**: add an optional `flowFrom` field (origin country) to deals that are led/co-led cross-border. For CTBC's foreign participations, `flowFrom:"Taiwan"`.

Add `flowFrom:"Taiwan"` to these existing deals (and any future CTBC cross-border deal):
- jun8: **San Miguel Global Power** (Philippines)
- jun15: **VPBank**, **HDBank** (Vietnam), **Macquarie Bank Europe** (listed under Australia)
- jun1: **KKR / XCL Education** (Singapore), **Ping An Dianchuang Leasing** (China)

Draw an arc `project(COUNTRY_PT[flowFrom]) → project(COUNTRY_PT[country])`, **teal if `ctbc`** else muted. Quadratic Bézier lifted perpendicular to the chord:
```js
function arcPath(p1,p2){
  const [x1,y1]=p1,[x2,y2]=p2, mx=(x1+x2)/2,my=(y1+y2)/2;
  const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy)||1, lift=Math.min(len*0.25,120);
  const cx=mx-dy/len*lift, cy=my+dx/len*lift;
  return `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`;
}
```
Style: `stroke:var(--ctbc); stroke-width:1.6; fill:none; opacity:.75`, arrowhead `marker-end` at the destination. Optional "flow" animation: animate `stroke-dashoffset` via CSS (subtle, slow). Draw arcs **under** the bubbles.

## 4) Interactions + legend
- **Hover** bubble → tooltip: country, `US$ total`, `# deals`, `# CTBC`.
- **Click** bubble → set the existing `#country` filter value and re-run the table render (reuse current filter/render path), and highlight the bubble; **click empty space** → clear. (This makes the map a filter control, not just a picture.)
- **Legend** (small, inline): bubble size = US$ volume · teal ring = CTBC involved · teal arc = CTBC cross-border lending.

## 5) Off-map outliers
Some borrowers tap Asian liquidity from elsewhere ("Chile (via Asia)", "Mauritius", African DFIs). Don't distort the map: collect them into a small chip under the map — `"+ N off-map: Chile, …"` — clickable to filter the table. Never silently drop them from counts/totals shown elsewhere.

## 6) Optional — globe brand mark (decorative, separate from the map)
A small monochrome CTBC-teal **spinning globe** in the header as identity (your original loader idea, repurposed as a mark). Pure inline SVG + CSS, ~34px, no real outlines needed:
```html
<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true">
  <circle cx="20" cy="20" r="16" fill="none" stroke="var(--ctbc)" stroke-width="1.5"/>
  <g class="globe-spin" style="transform-origin:20px 20px">
    <ellipse cx="20" cy="20" rx="6"  ry="16" fill="none" stroke="var(--ctbc)" stroke-width="1"/>
    <ellipse cx="20" cy="20" rx="12" ry="16" fill="none" stroke="var(--ctbc)" stroke-width=".8" opacity=".55"/>
    <line x1="4" y1="20" x2="36" y2="20" stroke="var(--ctbc)" stroke-width=".8" opacity=".55"/>
  </g>
</svg>
```
```css
.globe-spin{animation:gspin 14s linear infinite}
@keyframes gspin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
```
Keep it slow and quiet — it's a mark, not a focal point.

## 7) Build checklist (for Claude Code)
1. Add `COUNTRY_PT`, `MAP_W/H`, `project()`, `countryAgg()`, `arcPath()` near the other consts/helpers.
2. Add the SVG container + legend markup in the Weekly view (new "Geography" section).
3. Write `renderMap()` that: aggregates `W().deals`, draws arcs (deals with `flowFrom`), then bubbles + labels, wires hover/click to the `#country` filter, and lists off-map outliers. Call it from `renderWeek()`.
4. Add `flowFrom:"Taiwan"` to the six deals in §3.
5. Colours strictly via CSS vars; verify dark mode.

## 8) Validation
- `node --check` on the extracted `<script>` (if Node present); else serve locally (`python3 -m http.server 8080`) and open in a browser.
- Confirm: map renders for **each** week (toggle Jun 1/8/15); bubble sizes look right (Taiwan/Australia largest in their weeks); clicking a bubble filters the deal table; teal arcs appear for the §3 deals; off-map chip shows Chile; **no console errors and no network requests** (still works offline); legible in light + dark.

## 9) Stretch (later)
- "Cumulative (all weeks)" toggle on the map.
- Faint country outlines: inline a *simplified* APAC GeoJSON (note the file-size cost) and stroke it under the bubbles — only if you want shapes; bubbles+arcs already carry the insight.
- Animate bubbles growing on week-switch.
