#!/usr/bin/env python3
"""Parse WELL AP v2 third-party practice-quiz PDFs into structured JSON.

Source: _source/WELL_extracted/*.pdf (13 concept quizzes).
NOTE: third-party practice questions, NOT official IWBI exam questions.
Use for coverage/style reference only; ground truth = WELL v2 standard.
"""
import pypdf, glob, re, json, os

SRC = os.path.join(os.path.dirname(__file__), "WELL_extracted")
OUT = os.path.join(os.path.dirname(__file__), "quizzes-parsed.json")

# Map filename concept -> content-pack module key guess (concept name)
def concept_from_name(fn):
    m = re.search(r"WELL AP v2 (.+?)_\((\d+)\)\.pdf", fn)
    return (m.group(1).strip(), int(m.group(2))) if m else (fn, None)

# An answer marker: <A>..<D>, tolerant of internal spaces e.g. "< C >"
ANS_RE = re.compile(r"<\s*([A-Da-d])\s*>")
# Option line start
OPT_RE = re.compile(r"(?m)^\s*([A-D])\.\s+(.*)")
# Question number line start (1-2 digits + dot)
QNUM_RE = re.compile(r"(?m)^\s*(\d{1,2})\.\s")

def normalize(text):
    # drop the boilerplate header lines
    text = re.sub(r"02\.\s*PRACTICE QUIZZES BY CONCEPT", "", text)
    text = re.sub(r"Practice Quiz \| WELL AP V2 .*", "", text)
    return text

def split_questions(text):
    """Split on answer markers; each chunk = one Q (stem+options) then the
    answer letter, then explanation belongs to following text until next qnum."""
    # Find all answer-marker positions
    blocks = []
    parts = ANS_RE.split(text)  # [pre, letter, mid, letter, mid, ... , tail]
    # parts[0] = first question body; parts[1]=letter; parts[2]=expl+nextQ body...
    if len(parts) < 2:
        return blocks
    # iterate: body[i] ends with question, letter[i], then remainder starts expl
    bodies = parts[0::2]   # question bodies (0,2,4..) -> last is trailing
    letters = parts[1::2]  # answer letters
    for i, letter in enumerate(letters):
        q_body = bodies[i]
        remainder = bodies[i+1] if i+1 < len(bodies) else ""
        # explanation = remainder up to next question-number line
        m = QNUM_RE.search(remainder)
        expl = remainder[:m.start()] if m else remainder
        # but q_body for NEXT question is remainder[m.start():] handled by next iter's bodies?
        # No: bodies already split by markers, so q_body includes prior expl+nextstem.
        # Strip leading explanation belonging to PREVIOUS q from this q_body:
        blocks.append((q_body, letter, expl.strip()))
    return blocks

def parse_block(q_body):
    """From a body containing [prev-expl?] stem + 4 options, extract stem+opts."""
    opt_matches = list(OPT_RE.finditer(q_body))
    if len(opt_matches) < 4:
        return None
    # take the LAST 4 option matches (A,B,C,D nearest the answer)
    # find a contiguous A,B,C,D run from the end
    letters_seq = [m.group(1) for m in opt_matches]
    # locate last index where A starts a run A,B,C,D
    run_start = None
    for idx in range(len(opt_matches)-4, -1, -1):
        if [opt_matches[idx+k].group(1) for k in range(4)] == ["A","B","C","D"]:
            run_start = idx
            break
    if run_start is None:
        return None
    optA = opt_matches[run_start]
    # stem = text before optA, take last question-number occurrence
    stem_region = q_body[:optA.start()]
    qn = list(QNUM_RE.finditer(stem_region))
    stem = stem_region[qn[-1].end():] if qn else stem_region
    stem = re.sub(r"\s+", " ", stem).strip()
    opts = {}
    runs = opt_matches[run_start:run_start+4]
    for k, m in enumerate(runs):
        start = m.start(2)
        end = runs[k+1].start() if k+1 < 4 else optA.start()  # placeholder
        opts[m.group(1)] = (start, m)
    # compute option texts by slicing between option starts
    texts = {}
    for k in range(4):
        s = runs[k].start(2)
        e = runs[k+1].start() if k+1 < 4 else len(q_body)
        # but option D text should stop before answer marker (already removed) -> end of body
        txt = q_body[s:e]
        texts[runs[k].group(1)] = re.sub(r"\s+", " ", txt).strip()
    return stem, texts

def main():
    out = {"_meta": {"source": "third-party WELL AP v2 practice quizzes",
                     "warning": "NOT official IWBI exam questions; coverage/style reference only",
                     "concepts": {}}, "concepts": {}}
    total = 0
    for fn in sorted(glob.glob(os.path.join(SRC, "WELL AP v2 *.pdf"))):
        concept, expected = concept_from_name(os.path.basename(fn))
        r = pypdf.PdfReader(fn)
        text = normalize("\n".join(p.extract_text() or "" for p in r.pages))
        blocks = split_questions(text)
        questions = []
        fails = 0
        for q_body, letter, expl in blocks:
            parsed = parse_block(q_body)
            if not parsed:
                fails += 1
                continue
            stem, opts = parsed
            if not stem or len(opts) != 4:
                fails += 1
                continue
            questions.append({
                "stem": stem,
                "options": opts,
                "correct": letter.upper(),
                "explanation": expl,
            })
        out["concepts"][concept] = questions
        out["_meta"]["concepts"][concept] = {
            "expected": expected, "parsed": len(questions),
            "answer_markers": len(blocks), "parse_fails": fails,
        }
        total += len(questions)
        status = "OK" if expected == len(questions) else "CHECK"
        print(f"[{status}] {concept:16s} expected={expected} markers={len(blocks)} parsed={len(questions)} fails={fails}")
    out["_meta"]["total_parsed"] = total
    with open(OUT, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nTotal parsed: {total}  ->  {OUT}")

if __name__ == "__main__":
    main()
