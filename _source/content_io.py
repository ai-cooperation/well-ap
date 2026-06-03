#!/usr/bin/env python3
"""Load/save content.js as JSON, preserving the `const WELLAP_CONTENT = {...};`
wrapper. Single source of truth for mutating the content pack programmatically."""
import re, json, os

ROOT = os.path.dirname(os.path.dirname(__file__))
CONTENT_JS = os.path.join(ROOT, "content.js")

def load():
    t = open(CONTENT_JS).read()
    m = re.match(r"(const\s+\w+\s*=\s*)", t.lstrip())
    prefix = re.search(r"const\s+\w+\s*=\s*", t)
    body = t[prefix.end():].strip().rstrip(";").strip()
    var = re.search(r"const\s+(\w+)\s*=", t).group(1)
    return json.loads(body), var

def save(data, var="WELLAP_CONTENT"):
    body = json.dumps(data, ensure_ascii=False, indent=2)
    with open(CONTENT_JS, "w") as f:
        f.write(f"const {var} = {body};\n")

if __name__ == "__main__":
    d, var = load()
    print("var:", var, "| modules:", len(d["modules"]),
          "| ids:", [m["id"] for m in d["modules"]])
