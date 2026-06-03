#!/usr/bin/env python3
"""Split the question bank out of content.js into a Firebase upload payload.
- firebase-bank.json : { <moduleId>: { <qid>: questionObj } }  -> RTDB wellap/question_bank
- content.js (rewritten): questions/reinforcement emptied (public static, no quiz data)
                          + firebase config injected
The engine fetches wellap/question_bank after Google login and repopulates
module.questions in memory."""
import json, os
from content_io import load, save

FB_CONFIG = {
    "apiKey": "AIzaSyDNPfxqX1hsa0pni1x8nkQeInZbDljSi0w",
    "authDomain": "wellap-learn.firebaseapp.com",
    "databaseURL": "https://wellap-learn-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "wellap-learn",
    "storageBucket": "wellap-learn.firebasestorage.app",
    "messagingSenderId": "970394406936",
    "appId": "1:970394406936:web:390c13e5efef2d73a3336d",
}

HERE = os.path.dirname(__file__)

def main():
    data, var = load()
    bank = {}
    total = 0
    for m in data["modules"]:
        qs = m.get("questions", [])
        if qs:
            bank[m["id"]] = {q["id"]: q for q in qs}
            total += len(qs)
        # strip from static content pack
        m["questions"] = []
        m["reinforcement"] = []
    # inject firebase config (overwrite any existing)
    data["firebase"] = FB_CONFIG
    save(data, var)
    json.dump(bank, open(os.path.join(HERE, "firebase-bank.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"extracted {total} questions to firebase-bank.json across {len(bank)} modules")
    print("content.js questions emptied; firebase config injected")

if __name__ == "__main__":
    main()
