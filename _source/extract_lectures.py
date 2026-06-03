#!/usr/bin/env python3
"""Extract per-feature lecture content from wellv2-standard.txt (authoritative).
Output: lectures-data.json grouped by concept. No LLM — verbatim from the standard,
just structured + de-noised."""
import re, json, os, collections

HERE = os.path.dirname(__file__)
TXT = os.path.join(HERE, "wellv2-standard.txt")

PREFIX_TO_MODULE = {
    "A": ("M01", "空氣 Air"), "W": ("M02", "水 Water"), "N": ("M03", "飲食 Nourishment"),
    "L": ("M04", "光 Light"), "V": ("M05", "運動 Movement"), "T": ("M06", "熱舒適 Thermal Comfort"),
    "S": ("M07", "聲音 Sound"), "X": ("M08", "材料 Materials"), "M": ("M09", "心理 Mind"),
    "C": ("M10", "社區 Community"), "I": ("M12", "創新 Innovation"),
}
# WELL concept code prefixes. Header e.g. "A01 AIR QUALITY | P" or, when the
# P/O type wraps to the next line, "X02 INTERIOR HAZARDOUS ... |". β pilot
# features carry a Greek "Β" before the name.
HEADER_RE = re.compile(r"^\f?([AWNLVTSXMCI])(\d{2})\s+(?:Β\s+)?([A-Z][A-Z0-9 &,'’/()\-\.]+?)\s*\|\s*([PO])?\s*$")
FOOTER_RE = re.compile(r"©\s*Copyright|Page\s+\d+\s+of\s+\d+|All Rights Reserved")
PART_RE = re.compile(r"^\s*(Part\s+\d+\b.*)$")
SECTION_RE = re.compile(r"^(Intent|Summary):\s*(.*)$")
# labels that end an Intent/Summary capture (background we drop)
STOP_RE = re.compile(r"^(Issue|Solutions|Note):")

def clean_lines(lines):
    out = []
    for ln in lines:
        ln = ln.replace("\f", "").rstrip()
        if not ln.strip():
            continue
        if FOOTER_RE.search(ln):
            continue
        out.append(ln)
    return out

def parse():
    raw = open(TXT, encoding="utf-8").read().splitlines()
    # find header line indices
    headers = []
    for i, ln in enumerate(raw):
        m = HEADER_RE.match(ln)
        if m:
            typ = m.group(4)
            if not typ:  # P/O wrapped to a following non-empty line
                for j in range(i + 1, min(i + 4, len(raw))):
                    nxt = raw[j].replace("\f", "").strip()
                    if nxt in ("P", "O"):
                        typ = nxt; break
                    if nxt.upper().startswith("PRECONDITION"):
                        typ = "P"; break
                    if nxt.upper().startswith("OPTIMIZATION"):
                        typ = "O"; break
                    if nxt:
                        break
            headers.append((i, m, typ or "O"))
    feats = []
    seen = set()
    for idx, (i, m, typ) in enumerate(headers):
        prefix, num, name = m.group(1), m.group(2), m.group(3)
        code = f"{prefix}{num}"
        if code in seen:
            continue          # dedupe (WELL Core repeats)
        seen.add(code)
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(raw)
        body = clean_lines(raw[i + 1:end])
        intent_buf, summary_buf = [], []
        parts = []
        cur = None        # current Part being filled
        sect = None       # 'intent' | 'summary' | None (accumulating prose)
        for ln in body:
            sm = SECTION_RE.match(ln)
            pm = PART_RE.match(ln)
            if sm:
                sect = "intent" if sm.group(1) == "Intent" else "summary"
                (intent_buf if sect == "intent" else summary_buf).append(sm.group(2))
                cur = None
            elif pm:
                cur = {"title": pm.group(1).strip(), "lines": []}
                parts.append(cur)
                sect = None
            elif STOP_RE.match(ln):
                sect = None        # Issue/Solutions background — stop capturing
            elif cur is not None:
                cur["lines"].append(ln)
            elif sect == "intent":
                intent_buf.append(ln)
            elif sect == "summary":
                summary_buf.append(ln)
        intent = " ".join(intent_buf).strip()
        summary = " ".join(summary_buf).strip()
        feats.append({
            "code": code, "name": name.title(), "type": "precondition" if typ == "P" else "optimization",
            "prefix": prefix, "intent": intent.strip(), "summary": summary.strip(),
            "parts": [{"title": p["title"], "body": " ".join(p["lines"]).strip()[:3200]} for p in parts],
        })
    return feats

def main():
    feats = parse()
    by_mod = collections.OrderedDict()
    for f in feats:
        mid, mname = PREFIX_TO_MODULE[f["prefix"]]
        by_mod.setdefault(mid, {"module": mid, "name": mname, "features": []})
        by_mod[mid]["features"].append(f)
    # order modules M01..M12 (no M11 here — cert process authored separately)
    ordered = {k: by_mod[k] for k in sorted(by_mod)}
    json.dump(ordered, open(os.path.join(HERE, "lectures-data.json"), "w"),
              ensure_ascii=False, indent=2)
    print("feature count:", len(feats))
    for mid, d in ordered.items():
        nf = len(d["features"])
        npre = sum(1 for x in d["features"] if x["type"] == "precondition")
        print(f"  {mid} {d['name']:22s} features={nf:2d} (precond {npre}) "
              f"codes={','.join(x['code'] for x in d['features'])}")

if __name__ == "__main__":
    main()
