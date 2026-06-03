#!/usr/bin/env python3
"""Mechanical transform: parsed practice quizzes -> content-pack question schema.

Carries the verified stem/options/correct/explanation from the third-party
quizzes (the BASE), auto-maps each question to a module framework via the WELL
feature code referenced in its stem. depth/diagnosis are left for the codex
enrichment pass. Outputs questions-skeleton.json + a coverage report.
"""
import re, json, os, collections

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
QUIZZES = json.load(open(os.path.join(HERE, "quizzes-parsed.json")))

# concept (quiz filename) -> module id
CONCEPT_TO_MODULE = {
    "Air": "M01", "Water": "M02", "Nourishment": "M03", "Light": "M04",
    "Movement": "M05", "Thermal Comfort": "M06", "Sound": "M07",
    "Materials": "M08", "Mind": "M09", "Community": "M10",
    "Certification": "M11", "Portfolio": "M11", "Innovation": "M12",
}

def load_content():
    t = open(os.path.join(ROOT, "content.js")).read()
    m = re.search(r"const\s+\w+\s*=\s*", t)
    body = t[m.end():].strip().rstrip(";")
    return json.loads(body)

CODE_RE = re.compile(r"\b([A-Z]\d{2})\b")

def build_framework_index(content):
    """code -> list of (module_id, framework_id). And module -> [framework_ids]."""
    code_idx = collections.defaultdict(list)
    mod_fws = collections.defaultdict(list)
    for mod in content["modules"]:
        for fw in mod.get("frameworks", []):
            mod_fws[mod["id"]].append(fw["id"])
            for c in fw.get("covers", []):
                cm = CODE_RE.match(c.strip())
                if cm:
                    code_idx[cm.group(1)].append((mod["id"], fw["id"]))
    return code_idx, mod_fws

def map_framework(stem, module_id, code_idx):
    """Pick framework whose covers includes a feature code in the stem AND
    belongs to this module. Returns (framework_id|None, codes_found)."""
    codes = CODE_RE.findall(stem)
    # count framework votes within this module
    votes = collections.Counter()
    for c in codes:
        for (mid, fid) in code_idx.get(c, []):
            if mid == module_id:
                votes[fid] += 1
    if votes:
        return votes.most_common(1)[0][0], codes
    return None, codes

def main():
    content = load_content()
    code_idx, mod_fws = build_framework_index(content)
    out = collections.defaultdict(list)   # module_id -> [question dicts]
    report = collections.defaultdict(lambda: {"total": 0, "mapped": 0, "unmapped": 0})
    unmapped_samples = []
    counters = collections.Counter()

    for concept, qs in QUIZZES["concepts"].items():
        mid = CONCEPT_TO_MODULE[concept]
        for q in qs:
            counters[mid] += 1
            qid = f"{mid}_Q{counters[mid]:02d}"
            fw, codes = map_framework(q["stem"], mid, code_idx)
            options = [{"key": k, "text": q["options"][k]} for k in "ABCD"]
            item = {
                "id": qid,
                "stem": q["stem"],
                "options": options,
                "correct": q["correct"],
                "explanation": q["explanation"],
                "framework": fw or "",
                "_source": {"concept": concept, "codes": codes},
            }
            out[mid].append(item)
            report[mid]["total"] += 1
            if fw:
                report[mid]["mapped"] += 1
            else:
                report[mid]["unmapped"] += 1
                if len(unmapped_samples) < 15:
                    unmapped_samples.append((qid, codes, q["stem"][:80]))

    # write skeleton
    skel_path = os.path.join(HERE, "questions-skeleton.json")
    json.dump(dict(out), open(skel_path, "w"), ensure_ascii=False, indent=2)

    print(f"{'module':8s} {'total':>5s} {'mapped':>6s} {'unmapped':>8s}")
    gt = gm = 0
    for mid in sorted(report):
        r = report[mid]
        gt += r["total"]; gm += r["mapped"]
        print(f"{mid:8s} {r['total']:5d} {r['mapped']:6d} {r['unmapped']:8d}")
    print(f"{'TOTAL':8s} {gt:5d} {gm:6d} {gt-gm:8d}   ({100*gm//gt}% auto-mapped)")
    print("\n-- sample unmapped (need codex/manual framework) --")
    for qid, codes, stem in unmapped_samples:
        print(f"  {qid} codes={codes} :: {stem}")
    print(f"\nwrote {skel_path}")

if __name__ == "__main__":
    main()
