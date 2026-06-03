#!/usr/bin/env python3
"""Wire lecture deep-links into the content pack:
- top-level lectureBaseUrl + lecturePages (feature-code prefix -> lecture page file)
- per-module lecturePage (fallback target for concept/process questions)
- per-question lectureRefs = feature codes referenced in the stem (∩ real codes)
The engine resolves a wrong-answer review link to lectures/<page>#<CODE>."""
import re, json, os
from content_io import load, save

HERE = os.path.dirname(__file__)
LD = json.load(open(os.path.join(HERE, "lectures-data.json")))

SLUG = {"M01":"air","M02":"water","M03":"nourishment","M04":"light","M05":"movement",
        "M06":"thermal","M07":"sound","M08":"materials","M09":"mind","M10":"community",
        "M11":"certification","M12":"innovation"}
PREFIX_PAGE = {"A":"M01-air.html","W":"M02-water.html","N":"M03-nourishment.html",
               "L":"M04-light.html","V":"M05-movement.html","T":"M06-thermal.html",
               "S":"M07-sound.html","X":"M08-materials.html","M":"M09-mind.html",
               "C":"M10-community.html","I":"M12-innovation.html"}

VALID = set()
for m in LD.values():
    for f in m["features"]:
        VALID.add(f["code"])

CODE_RE = re.compile(r"\b([AWNLVTSXMCI]\d{2})\b")

def main():
    data, var = load()
    data["lectureBaseUrl"] = "lectures/"
    data["lecturePages"] = PREFIX_PAGE
    withrefs = 0; norefs = 0
    for m in data["modules"]:
        m["lecturePage"] = f'{m["id"]}-{SLUG[m["id"]]}.html'
        for q in m.get("questions", []):
            codes = []
            for c in CODE_RE.findall(q["stem"]):
                if c in VALID and c not in codes:
                    codes.append(c)
            codes = codes[:2]
            if codes:
                q["lectureRefs"] = codes
                withrefs += 1
            else:
                q.pop("lectureRefs", None)
                norefs += 1
    save(data, var)
    print(f"questions with feature deep-link: {withrefs} | fallback to concept page: {norefs}")

if __name__ == "__main__":
    main()
