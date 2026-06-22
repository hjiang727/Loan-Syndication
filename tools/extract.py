# -*- coding: utf-8 -*-
"""One-off: pull the data out of the monolithic HTML into src/template.html + src/data/*.json.
Uses a tiny JS-object-literal parser (the data uses a small JSON-ish subset: double-quoted
strings, unquoted identifier keys, numbers, null, trailing commas)."""
import re, json, os
ROOT="/Users/henryjiang/Documents/Claude/Projects/Finance/CTBC-Loan-Tracker"
src=open(ROOT+"/CTBC_Loan_Market_Dashboard.html",encoding="utf-8").read()

class P:
    def __init__(s,t,i): s.t=t; s.i=i
    def ws(s):
        t=s.t
        while s.i<len(t):
            c=t[s.i]
            if c in ' \t\r\n': s.i+=1
            elif c=='/' and t[s.i+1]=='*': s.i=t.index('*/',s.i+2)+2
            else: break
    def val(s):
        s.ws(); c=s.t[s.i]
        if c=='{': return s.obj()
        if c=='[': return s.arr()
        if c=='"': return s.string()
        if c=='`': return s.tstr()
        return s.lit()
    def tstr(s):
        t=s.t; s.i+=1; out=[]
        while True:
            c=t[s.i]
            if c=='\\': out.append(t[s.i+1]); s.i+=2
            elif c=='`': s.i+=1; return ''.join(out)
            else:
                if c=='$' and t[s.i+1]=='{': raise Exception("template interpolation in data string — not pure data")
                out.append(c); s.i+=1
    def obj(s):
        s.i+=1; o={}
        while True:
            s.ws()
            if s.t[s.i]=='}': s.i+=1; return o
            if s.t[s.i]=='"': k=s.string()
            else:
                m=re.match(r'[A-Za-z_$][\w$]*', s.t[s.i:]); k=m.group(0); s.i+=len(k)
            s.ws(); assert s.t[s.i]==':', s.t[s.i:s.i+20]; s.i+=1
            o[k]=s.val(); s.ws()
            if s.t[s.i]==',': s.i+=1
            elif s.t[s.i]=='}': s.i+=1; return o
            else: raise Exception("obj@"+repr(s.t[s.i:s.i+30]))
    def arr(s):
        s.i+=1; a=[]
        while True:
            s.ws()
            if s.t[s.i]==']': s.i+=1; return a
            a.append(s.val()); s.ws()
            if s.t[s.i]==',': s.i+=1
            elif s.t[s.i]==']': s.i+=1; return a
            else: raise Exception("arr@"+repr(s.t[s.i:s.i+30]))
    def string(s):
        t=s.t; s.i+=1; out=[]; esc={'"':'"','\\':'\\','/':'/','n':'\n','t':'\t','r':'\r','b':'\b','f':'\f'}
        while True:
            c=t[s.i]
            if c=='\\':
                n=t[s.i+1]
                if n=='u': out.append(chr(int(t[s.i+2:s.i+6],16))); s.i+=6
                else: out.append(esc.get(n,n)); s.i+=2
            elif c=='"': s.i+=1; return ''.join(out)
            else: out.append(c); s.i+=1
    def lit(s):
        m=re.match(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?|true|false|null', s.t[s.i:])
        x=m.group(0); s.i+=len(x)
        if x=='true': return True
        if x=='false': return False
        if x=='null': return None
        return float(x) if ('.' in x or 'e' in x or 'E' in x) else int(x)

def grab(name):
    m=re.search(r'const '+name+r'\s*=\s*', src); p=P(src,m.end()); return p.val(), m, p.i

WORLD_LAND,_,_=grab("WORLD_LAND")
WIDER,_,_=grab("WIDER")
GLOSS,_,_=grab("GLOSS")
WEEKS,_,_=grab("WEEKS")
ORDER,_,_=grab("ORDER")
SECONDARY, sm, send=grab("SECONDARY")

# sanity
nd=sum(len(WEEKS[o['key']]['deals']) for o in ORDER)
print("rings",len(WORLD_LAND),"weeks",list(WEEKS.keys()),"order",[o['key'] for o in ORDER],"deals",nd,"secondary",len(SECONDARY))
assert nd==108 and len(WORLD_LAND)==732 and len(ORDER)==3

# ---- write src/data ----
os.makedirs(ROOT+"/src/data",exist_ok=True)
json.dump(WORLD_LAND, open(ROOT+"/src/data/world_land.json","w"), separators=(",",":"))
json.dump({"wider":WIDER,"gloss":GLOSS,"secondary":SECONDARY},
          open(ROOT+"/src/data/shared.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
DATE={"jun1":"2026-06-01","jun8":"2026-06-08","jun15":"2026-06-15"}
for o in ORDER:
    k=o['key']
    rec={"key":k,"tab":o['label'],"date":DATE[k],"week":WEEKS[k]}
    json.dump(rec, open(ROOT+"/src/data/"+k+".json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- write src/template.html (data span -> marker) ----
a=src.index("const WORLD_LAND=")
# swallow a preceding inlined-land comment if present
cmt=src.rfind("/* ---- inlined", 0, a)
if cmt!=-1 and src[cmt:a].strip().endswith("*/"): a=cmt
# end = just past SECONDARY's terminating ';'
b=send
while src[b] in ' \t\r\n': b+=1
assert src[b]==';'; b+=1
template=src[:a]+"/*__DATA__*/"+src[b:]
open(ROOT+"/src/template.html","w",encoding="utf-8").write(template)
print("template bytes",len(template),"(was",len(src),") marker present:", "/*__DATA__*/" in template)
