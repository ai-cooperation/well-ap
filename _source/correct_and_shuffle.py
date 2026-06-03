#!/usr/bin/env python3
"""(1) Apply the 4 verified answer corrections (answer + depth + diagnosis rekey).
(2) Shuffle option ORDER per question so the correct-answer position is not biased.
Option TEXT is preserved verbatim — only the A-D letter assignment changes.
Questions whose options reference position ('All of the above', 'Both A and B',
'None of the above', etc.) are left in source order to keep them answerable."""
import json, os, re, hashlib, random, collections
from content_io import load, save

# qid -> (new_correct, {old_correct_key_now_wrong: (depth, gap, followup)})
# Only the option that FLIPS from correct->wrong needs a new diagnosis entry;
# the new correct's old diagnosis entry is removed automatically.
CORRECTIONS = {
 "M02_Q03": ("A", {"C": (3,
   "把 turbidity 的 on-site 驗證誤當長期數據回報",
   "turbidity ≤ 1.0 NTU 屬 W01 的 water quality indicator，是用一次性 on-site performance test 確認，還是長期 data report？")}),
 "M02_Q19": ("D", {"C": (3,
   "RO/carbon 著重物理捕捉 contaminants，carbon bed 反而可能孳生微生物",
   "要『抑制微生物生長』，靠物理捕捉的 RO/carbon，還是能殺滅 coliforms 與 pathogens 的 UV？")}),
 "M08_Q46": ("B", {"D": (3,
   "把非 WELL 指定的 Soil Quality Guidance 一併納入而誤選 Both",
   "X04 指定的是 ASTM E1527 Phase I 與 E1903 Phase II；選項 A 的 Sustainable Remediation 標準是否在其列？")}),
 "M10_Q39": ("A", {"D": (3,
   "誤以為 C09 對 lactation room 沒有任何最低要求",
   "C09 Part 2 要求至少一間 dedicated lactation room，這還能算『沒有具體要求』嗎？")}),
}

PIN_RE = re.compile(r"\b(all of the above|none of the above|both a|a & b|a and b|all of the following|neither of)\b", re.I)

def apply_correction(q):
    new_correct, flip = CORRECTIONS[q["id"]]
    old_correct = q["correct"]
    if new_correct == old_correct:
        return
    # depth swap: new correct -> 4, old correct -> demoted value from flip spec
    for o in q["options"]:
        if o["key"] == new_correct:
            o["depth"] = 4
        elif o["key"] == old_correct:
            o["depth"] = flip[old_correct][0]
    # diagnosis: drop new-correct entry, add old-correct entry
    diag = dict(q.get("diagnosis", {}))
    diag.pop(new_correct, None)
    d, gap, fu = flip[old_correct]
    diag[old_correct] = {"gap": gap, "followup": fu}
    q["diagnosis"] = diag
    q["correct"] = new_correct

def shuffle_question(q):
    """Deterministic per-qid permutation of options; re-letter A-D; remap
    correct + diagnosis keys; keep text/depth bound to each option."""
    opts = q["options"]
    seed = int(hashlib.md5(q["id"].encode()).hexdigest(), 16) & 0xffffffff
    order = list(range(4))
    random.Random(seed).shuffle(order)
    new_opts = []
    oldkey_to_new = {}
    for newpos, oldidx in enumerate(order):
        o = opts[oldidx]
        newkey = "ABCD"[newpos]
        oldkey_to_new[o["key"]] = newkey
        new_opts.append({"key": newkey, "text": o["text"], "depth": o["depth"]})
    # keep options in A,B,C,D order
    new_opts.sort(key=lambda o: o["key"])
    q["options"] = new_opts
    q["correct"] = oldkey_to_new[q["correct"]]
    q["diagnosis"] = {oldkey_to_new[k]: v for k, v in q.get("diagnosis", {}).items()}

def main():
    data, var = load()
    corrected = 0
    shuffled = 0
    pinned = 0
    dist = collections.Counter()
    bad = []
    for m in data["modules"]:
        for q in m.get("questions", []):
            if q["id"] in CORRECTIONS:
                apply_correction(q)
                corrected += 1
            if any(PIN_RE.search(o["text"]) for o in q["options"]):
                pinned += 1
            else:
                shuffle_question(q)
                shuffled += 1
            # integrity
            keys = [o["key"] for o in q["options"]]
            d4 = [o for o in q["options"] if o["depth"] == 4]
            diagk = set(q.get("diagnosis", {}).keys())
            if (keys != ["A","B","C","D"] or q["correct"] not in keys
                    or len(d4) != 1 or d4[0]["key"] != q["correct"]
                    or diagk != ({"A","B","C","D"} - {q["correct"]})):
                bad.append(q["id"])
            dist[q["correct"]] += 1
    save(data, var)
    print(f"corrected: {corrected} | shuffled: {shuffled} | pinned(kept order): {pinned}")
    print(f"new GLOBAL correct distribution: {dict(sorted(dist.items()))}")
    print(f"integrity-bad questions: {len(bad)} {bad[:10]}")

if __name__ == "__main__":
    main()
