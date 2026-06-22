// Build: bundle src/template.html + src/data/*.json -> dist/CTBC_Loan_Market_Dashboard.html
// Run: node tools/build.mjs   (or: npm run build)
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const load = (p) => JSON.parse(readFileSync(join(ROOT, p), "utf8"));

const tpl = readFileSync(join(ROOT, "src/template.html"), "utf8");
const shared = load("src/data/shared.json");
const land = load("src/data/world_land.json");

const weekFiles = readdirSync(join(ROOT, "src/data"))
  .filter((f) => f.endsWith(".json") && !["shared.json", "world_land.json"].includes(f));
const weeks = weekFiles.map((f) => load("src/data/" + f)).sort((a, b) => (a.date < b.date ? -1 : 1)); // newest last → opens by default

const WEEKS = Object.fromEntries(weeks.map((w) => [w.key, w.week]));
const ORDER = weeks.map((w) => ({ key: w.key, label: w.tab }));
const J = (o) => JSON.stringify(o);

const data =
  `const WORLD_LAND=${J(land)};\n` +
  `const WIDER=${J(shared.wider)};\n` +
  `const GLOSS=${J(shared.gloss)};\n` +
  `const WEEKS=${J(WEEKS)};\n` +
  `const ORDER=${J(ORDER)};\n` +
  `const SECONDARY=${J(shared.secondary)};`;

if (!tpl.includes("/*__DATA__*/")) throw new Error("template marker /*__DATA__*/ missing");
mkdirSync(join(ROOT, "dist"), { recursive: true });
writeFileSync(join(ROOT, "dist/CTBC_Loan_Market_Dashboard.html"), tpl.replace("/*__DATA__*/", data));
console.log(`✓ built dist/CTBC_Loan_Market_Dashboard.html (${weeks.length} weeks: ${weeks.map((w) => w.key).join(", ")})`);
