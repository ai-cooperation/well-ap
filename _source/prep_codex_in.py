#!/usr/bin/env python3
"""Split the question skeleton into chunked codex input files, each embedding
its module's frameworks so codex can assign framework + enrich grounded in the
WELL v2 standard."""
import json, os, math
from content_io import load

HERE = os.path.dirname(__file__)
SKEL = json.load(open(os.path.join(HERE, "questions-skeleton.json")))
IN_DIR = os.path.join(HERE, "codex_in")
os.makedirs(IN_DIR, exist_ok=True)

CHUNK = 25

def main():
    content, _ = load()
    fw_by_module = {m["id"]: m.get("frameworks", []) for m in content["modules"]}
    manifest = []
    for mid, qs in SKEL.items():
        fws = [{"id": f["id"], "name": f["name"], "desc": f["desc"],
                "covers": f.get("covers", [])} for f in fw_by_module.get(mid, [])]
        nchunks = math.ceil(len(qs) / CHUNK)
        for ci in range(nchunks):
            chunk = qs[ci*CHUNK:(ci+1)*CHUNK]
            tag = f"{mid}_{chr(97+ci)}" if nchunks > 1 else mid
            payload = {
                "module": mid,
                "frameworks": fws,
                "questions": [
                    {"id": q["id"], "stem": q["stem"], "options": q["options"],
                     "correct": q["correct"], "source_explanation": q["explanation"],
                     "framework_hint": q["framework"]}
                    for q in chunk
                ],
            }
            path = os.path.join(IN_DIR, f"{tag}.json")
            json.dump(payload, open(path, "w"), ensure_ascii=False, indent=2)
            manifest.append((tag, mid, len(chunk)))
    print(f"wrote {len(manifest)} chunk files to {IN_DIR}")
    for tag, mid, n in manifest:
        print(f"  {tag:8s} ({n} q)")
    json.dump([{"tag": t, "module": m, "n": n} for t, m, n in manifest],
              open(os.path.join(HERE, "codex_manifest.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
