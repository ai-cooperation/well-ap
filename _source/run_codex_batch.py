#!/usr/bin/env python3
"""Run codex enrichment over chunk tags with bounded concurrency.
Skips tags whose output already exists (resumable). Logs per-tag status."""
import json, os, subprocess, sys, glob
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
IN_DIR = os.path.join(HERE, "codex_in")
OUT_DIR = os.path.join(HERE, "codex_out")
PROMPT_TMPL = open(os.path.join(HERE, "codex_prompt.txt")).read()
CODEX = "/opt/homebrew/bin/codex"
CONCURRENCY = 3

def all_tags():
    return sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(IN_DIR, "*.json")))

def run_one(tag):
    out_path = os.path.join(OUT_DIR, f"{tag}.json")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        return tag, "SKIP (exists)"
    prompt = PROMPT_TMPL.replace("{TAG}", tag)
    try:
        p = subprocess.run(
            [CODEX, "exec", "--skip-git-repo-check", "--sandbox", "workspace-write", prompt],
            stdin=subprocess.DEVNULL, cwd=ROOT,
            capture_output=True, text=True, timeout=900,
        )
        ok = os.path.exists(out_path) and os.path.getsize(out_path) > 100
        # try to grab token line from output
        tail = (p.stdout or "")[-400:]
        tok = ""
        for line in tail.splitlines():
            if "token" in line.lower():
                tok = line.strip()
        return tag, ("DONE " + tok if ok else f"NO OUTPUT (rc={p.returncode}) {tail[-200:]}")
    except subprocess.TimeoutExpired:
        return tag, "TIMEOUT"
    except Exception as e:
        return tag, f"ERROR {e}"

def main():
    tags = sys.argv[1:] or all_tags()
    pending = [t for t in tags
               if not (os.path.exists(os.path.join(OUT_DIR, f"{t}.json"))
                       and os.path.getsize(os.path.join(OUT_DIR, f"{t}.json")) > 100)]
    print(f"running {len(pending)} chunks (concurrency {CONCURRENCY}): {pending}", flush=True)
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(run_one, t): t for t in pending}
        for f in as_completed(futs):
            tag, status = f.result()
            print(f"[{tag}] {status}", flush=True)
    print("BATCH COMPLETE", flush=True)

if __name__ == "__main__":
    main()
