#!/usr/bin/env python3
"""Validate codex-enriched question chunks against the content-pack quality bars.
Usage: python3 validate_enriched.py [TAG ...]   (default: all chunks in codex_out)"""
import json, os, sys, glob, re

HERE = os.path.dirname(__file__)
IN_DIR = os.path.join(HERE, "codex_in")
OUT_DIR = os.path.join(HERE, "codex_out")

def validate_chunk(tag):
    inp = json.load(open(os.path.join(IN_DIR, f"{tag}.json")))
    out_path = os.path.join(OUT_DIR, f"{tag}.json")
    if not os.path.exists(out_path):
        return [f"{tag}: OUTPUT MISSING"], 0
    try:
        out = json.load(open(out_path))
    except Exception as e:
        return [f"{tag}: INVALID JSON ({e})"], 0
    errs = []
    fw_ids = {f["id"] for f in inp["frameworks"]}
    in_by_id = {q["id"]: q for q in inp["questions"]}
    if len(out) != len(inp["questions"]):
        errs.append(f"{tag}: count {len(out)} != input {len(inp['questions'])}")
    seen = set()
    for q in out:
        qid = q.get("id", "?")
        seen.add(qid)
        src = in_by_id.get(qid)
        if not src:
            errs.append(f"{qid}: id not in input"); continue
        # verbatim stem/correct
        if q.get("stem") != src["stem"]:
            errs.append(f"{qid}: stem altered")
        if q.get("correct") != src["correct"] and q.get("verify", {}).get("verdict") != "suspect":
            errs.append(f"{qid}: correct changed without suspect flag")
        # framework
        if q.get("framework") not in fw_ids:
            errs.append(f"{qid}: framework '{q.get('framework')}' not in module")
        # options + depth
        opts = q.get("options", [])
        if len(opts) != 4:
            errs.append(f"{qid}: {len(opts)} options")
        depth4 = [o for o in opts if o.get("depth") == 4]
        for o in opts:
            d = o.get("depth")
            if not isinstance(d, int) or not (1 <= d <= 4):
                errs.append(f"{qid}: opt {o.get('key')} bad depth {d}")
        correct = q.get("correct")
        cdepth = next((o.get("depth") for o in opts if o.get("key") == correct), None)
        if cdepth != 4:
            errs.append(f"{qid}: correct option depth={cdepth} (want 4)")
        # diagnosis exactly 3 non-correct keys
        diag = q.get("diagnosis", {})
        expect = {"A","B","C","D"} - {correct}
        if set(diag.keys()) != expect:
            errs.append(f"{qid}: diagnosis keys {sorted(diag.keys())} != {sorted(expect)}")
        for k, v in diag.items():
            if not v.get("gap") or not v.get("followup"):
                errs.append(f"{qid}: diagnosis {k} missing gap/followup")
        # explanation present, no answer letter leak
        expl = q.get("explanation", "")
        if not expl or len(expl) < 10:
            errs.append(f"{qid}: explanation too short")
        if re.search(r"答案是\s*[A-D]|正確答案為?\s*[A-D]|選\s*[A-D]\b", expl):
            errs.append(f"{qid}: explanation leaks answer letter")
    missing = set(in_by_id) - seen
    for m in missing:
        errs.append(f"{m}: missing from output")
    return errs, len(out)

def main():
    tags = sys.argv[1:] or [os.path.splitext(os.path.basename(p))[0]
                            for p in sorted(glob.glob(os.path.join(IN_DIR, "*.json")))]
    total_errs = 0
    suspects = []
    for tag in tags:
        errs, n = validate_chunk(tag)
        status = "OK" if not errs else f"{len(errs)} ISSUES"
        print(f"[{status:9s}] {tag} ({n} q)")
        for e in errs[:20]:
            print(f"    - {e}")
        total_errs += len(errs)
        # collect suspect flags
        op = os.path.join(OUT_DIR, f"{tag}.json")
        if os.path.exists(op):
            try:
                for q in json.load(open(op)):
                    v = q.get("verify", {})
                    if v.get("verdict") == "suspect":
                        suspects.append((q["id"], v.get("note",""), v.get("corrected_correct","")))
            except Exception:
                pass
    print(f"\nTOTAL ISSUES: {total_errs}")
    if suspects:
        print(f"\n-- SUSPECT questions flagged by codex ({len(suspects)}) --")
        for qid, note, cc in suspects:
            print(f"  {qid}: {note} {'-> correct?='+cc if cc else ''}")

if __name__ == "__main__":
    main()
