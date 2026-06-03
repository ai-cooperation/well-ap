#!/usr/bin/env python3
"""Merge codex Chinese summaries into lectures-data.json + numeric consistency check:
every number token in zh_specs/zh_summary must appear in that feature's English source,
else flag for review (guards against hallucinated thresholds)."""
import json, os, re, glob
HERE=os.path.dirname(__file__)
data=json.load(open(os.path.join(HERE,"lectures-data.json")))
zh={}
for p in glob.glob(os.path.join(HERE,"zh_out","*.json")):
    for o in json.load(open(p)):
        zh[o["code"]]=o
NUM=re.compile(r"\d+(?:\.\d+)?")
def norm(s): return s.replace(",","")
attached=0; missing=[]; mism=[]
for mid,m in data.items():
    for f in m["features"]:
        z=zh.get(f["code"])
        if not z:
            missing.append(f["code"]); continue
        f["zh_name"]=z.get("zh_name",""); f["zh_summary"]=z.get("zh_summary","")
        f["zh_specs"]=z.get("zh_specs",[])
        attached+=1
        # numeric check
        src=norm(" ".join([f["intent"],f["summary"]]+[p["body"] for p in f["parts"]]))
        srcnums=set(NUM.findall(src))
        zhtext=norm(" ".join([f["zh_summary"]]+f["zh_specs"]))
        for n in NUM.findall(zhtext):
            # ignore tiny ints 1-9 (часто appear; low risk) and feature-code digits
            if n in srcnums: continue
            if len(n)<=1: continue
            mism.append((f["code"],n))
json.dump(data,open(os.path.join(HERE,"lectures-data.json"),"w"),ensure_ascii=False,indent=2)
print(f"attached zh to {attached} features | missing zh: {len(missing)} {missing}")
print(f"numeric mismatches (zh number not in EN source): {len(mism)}")
from collections import Counter
for code,cnt in Counter(c for c,_ in mism).most_common(20):
    nums=[n for c,n in mism if c==code]
    print(f"  {code}: {nums}")
