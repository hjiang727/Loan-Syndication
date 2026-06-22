# -*- coding: utf-8 -*-
"""No-Node build: bundle src/template.html + src/data/*.json -> dist/CTBC_Loan_Market_Dashboard.html.
Mirror of build.mjs (kept so the dashboard is buildable without a Node install)."""
import json, glob, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def L(p): return json.load(open(os.path.join(ROOT,p),encoding="utf-8"))

tpl=open(os.path.join(ROOT,"src/template.html"),encoding="utf-8").read()
shared=L("src/data/shared.json"); land=L("src/data/world_land.json")
weeks=[L("src/data/"+os.path.basename(f)) for f in glob.glob(os.path.join(ROOT,"src/data/*.json"))
       if os.path.basename(f) not in ("shared.json","world_land.json")]
weeks.sort(key=lambda w:w["date"])                      # chronological; newest last = opens by default
WEEKS={w["key"]:w["week"] for w in weeks}
ORDER=[{"key":w["key"],"label":w["tab"]} for w in weeks]
def js(o): return json.dumps(o,ensure_ascii=False,separators=(",",":"))
data=("const WORLD_LAND="+js(land)+";\n"
      "const WIDER="+js(shared["wider"])+";\n"
      "const GLOSS="+js(shared["gloss"])+";\n"
      "const WEEKS="+js(WEEKS)+";\n"
      "const ORDER="+js(ORDER)+";\n"
      "const SECONDARY="+js(shared["secondary"])+";")
assert "/*__DATA__*/" in tpl, "template marker missing"
out=tpl.replace("/*__DATA__*/", data)
os.makedirs(os.path.join(ROOT,"dist"),exist_ok=True)
open(os.path.join(ROOT,"dist/CTBC_Loan_Market_Dashboard.html"),"w",encoding="utf-8").write(out)
print("built dist/CTBC_Loan_Market_Dashboard.html  (%d weeks: %s, %d bytes)" % (
    len(weeks), ", ".join(w["key"] for w in weeks), len(out)))
