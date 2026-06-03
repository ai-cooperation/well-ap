#!/usr/bin/env python3
"""WELL-adapted quiz-quality-guard scan over the injected content.js question bank.
Checks the learner-visible fields for leaks/imbalance. English-aware (options are
third-party English text; uses word-ish length, not the Chinese char caps)."""
import re, sys, collections
from content_io import load

# answer-letter leak in explanation (Chinese + English forms)
LEAK_RE = re.compile(r"答案[是為]\s*[A-D]\b|正確答案[是為]?\s*[A-D]\b|[Tt]he answer is\s*[A-D]\b|[Oo]ption\s+[A-D]\s+is correct|選\s*[A-D]\b")
# absolute-language traps that can make an option obviously right/wrong
ABS_RE = re.compile(r"\b(always|never|only|all|none|completely|exclusively|guaranteed)\b", re.I)

def scan():
    data, _ = load()
    leaks, imbalance, abs_hits, design = [], [], [], []
    per_mod = collections.Counter()
    total = 0
    for mod in data["modules"]:
        for q in mod.get("questions", []):
            total += 1; per_mod[mod["id"]] += 1
            qid = q["id"]
            expl = q.get("explanation", "")
            stem = q.get("stem", "")
            # 1. answer letter leak in explanation/stem
            if LEAK_RE.search(expl) or LEAK_RE.search(stem):
                leaks.append(f"{qid}: answer-letter leak")
            # 2. design-thought leak in learner-visible fields
            for o in q["options"]:
                if re.search(r"\((trap|correct|wrong|陷阱|正確|錯誤)\)", o["text"], re.I):
                    design.append(f"{qid} opt{o['key']}: design label in option")
            # 3. option length outlier (correct option a length outlier vs others)
            lens = {o["key"]: len(o["text"]) for o in q["options"]}
            correct = q["correct"]
            others = [v for k, v in lens.items() if k != correct]
            avg_other = sum(others) / len(others) if others else 0
            cl = lens[correct]
            if others and (cl > avg_other * 1.8 or cl < avg_other * 0.55) and abs(cl - avg_other) > 25:
                imbalance.append(f"{qid}: correct opt len {cl} vs others avg {avg_other:.0f}")
            # 4. absolute language in correct option (could be a giveaway-by-elimination)
            cor_text = next(o["text"] for o in q["options"] if o["key"] == correct)
            if ABS_RE.search(cor_text):
                abs_hits.append(f"{qid}: absolute word in CORRECT option :: {cor_text[:60]}")

    print(f"scanned {total} questions across {len(per_mod)} modules")
    for name, items in [("ANSWER-LETTER LEAK", leaks), ("DESIGN-LABEL LEAK", design),
                         ("OPTION-LENGTH OUTLIER (correct)", imbalance),
                         ("ABSOLUTE WORD in correct opt", abs_hits)]:
        print(f"\n== {name}: {len(items)} ==")
        for it in items[:25]:
            print(f"  - {it}")
    # gate: leaks/design must be 0; imbalance/abs are advisory (human review)
    blocking = len(leaks) + len(design)
    print(f"\nBLOCKING issues (leak+design): {blocking}")
    return blocking

if __name__ == "__main__":
    sys.exit(1 if scan() else 0)
