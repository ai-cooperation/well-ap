#!/usr/bin/env python3
"""Merge codex-enriched chunks per module and inject into content.js `questions`.
Strips helper fields; emits a suspects report for human review. Run AFTER all
chunks validate clean."""
import json, os, glob, re, collections
from content_io import load, save

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "codex_out")

KEEP = ("id", "stem", "options", "correct", "explanation", "framework", "diagnosis")

def chunk_sort_key(tag):
    m = re.match(r"(M\d+)(?:_([a-z]))?$", tag)
    return (m.group(1), m.group(2) or "")

def clean_question(q):
    out = {k: q[k] for k in KEEP if k in q}
    # options: keep key/text/depth only
    out["options"] = [{"key": o["key"], "text": o["text"], "depth": o.get("depth", 2)}
                      for o in q["options"]]
    return out

def main():
    by_module = collections.defaultdict(list)
    suspects = []
    tags = sorted((os.path.splitext(os.path.basename(p))[0]
                   for p in glob.glob(os.path.join(OUT_DIR, "*.json"))),
                  key=chunk_sort_key)
    for tag in tags:
        mod = chunk_sort_key(tag)[0]
        for q in json.load(open(os.path.join(OUT_DIR, f"{tag}.json"))):
            v = q.get("verify", {})
            if v.get("verdict") == "suspect":
                suspects.append({"id": q["id"], "module": mod,
                                 "note": v.get("note", ""),
                                 "corrected_correct": v.get("corrected_correct", ""),
                                 "stem": q["stem"]})
            by_module[mod].append(clean_question(q))

    data, var = load()
    injected = 0
    for mod in data["modules"]:
        qs = by_module.get(mod["id"], [])
        if qs:
            mod["questions"] = qs
            injected += len(qs)
            print(f"  {mod['id']}: {len(qs)} questions")
    save(data, var)
    print(f"\ninjected {injected} questions into content.js")

    json.dump(suspects, open(os.path.join(HERE, "suspects-report.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"suspects flagged: {len(suspects)} -> suspects-report.json")
    for s in suspects:
        print(f"  {s['id']}: {s['note'][:90]}")

if __name__ == "__main__":
    main()
