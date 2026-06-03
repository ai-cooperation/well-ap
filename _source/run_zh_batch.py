import os, glob, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
PROMPT=open(os.path.join(HERE,"zh_prompt.txt")).read()
tags=sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(HERE,"zh_in","*.json")))
pending=[t for t in tags if not (os.path.exists(os.path.join(HERE,"zh_out",f"{t}.json")) and os.path.getsize(os.path.join(HERE,"zh_out",f"{t}.json"))>50)]
print("pending:",pending,flush=True)
def run(t):
    out=os.path.join(HERE,"zh_out",f"{t}.json")
    p=subprocess.run(["/opt/homebrew/bin/codex","exec","--skip-git-repo-check","--sandbox","workspace-write",PROMPT.replace("{TAG}",t)],
                     stdin=subprocess.DEVNULL,cwd=ROOT,capture_output=True,text=True,timeout=900)
    ok=os.path.exists(out) and os.path.getsize(out)>50
    return t,("DONE" if ok else f"FAIL rc={p.returncode} "+(p.stdout or "")[-150:])
with ThreadPoolExecutor(max_workers=3) as ex:
    for f in as_completed({ex.submit(run,t):t for t in pending}):
        t,s=f.result(); print(f"[{t}] {s}",flush=True)
print("BATCH COMPLETE",flush=True)
