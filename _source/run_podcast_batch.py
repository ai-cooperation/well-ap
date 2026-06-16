#!/usr/bin/env python3
"""
run_podcast_batch.py — 用 notebooklm-py 把 12 個 WELL AP 概念講義生成中文學習 podcast。

每個 concept 一集（對應 12 頁講義 1:1），流程：
  create notebook -> source add 講義公開 URL -> generate audio (zh_Hant) -> download mp3

設計重點（對齊 _source/run_zh_batch.py 的批次風格 + SB 筆記裡 notebooklm-py 的踩雷清單）：
- 素材用「公開講義 URL」，繞過 notebooklm-py 中文 md/txt 上傳會回 None 的 bug（URL 抓取正常）
- idempotent：mp3 已存在且 > MIN_BYTES 就跳過，可中斷續跑
- notebook id 存進 podcast_out/state.json，重跑不會重複建 notebook
- 產出後驗證 mp3 實際大小，不假設成功（audio 高負載會無聲失敗回 None）
- 順序執行（非並行）：batchexecute 有嚴格限速，靠 CLI 自身 --wait + --retry 退避

前置（只能你本人做）：
  notebooklm login            # 瀏覽器登入 Google，首次下載 Chromium ~170MB
  notebooklm auth check --json
  批次量產 12 集建議 NotebookLM Plus（免費帳號每日 Audio Overview 約 3 集上限）

用法：
  python3 run_podcast_batch.py            # 全部 12 集（已存在的跳過）
  python3 run_podcast_batch.py M01        # 只跑 M01（先驗證品質用）
  python3 run_podcast_batch.py M01 M02    # 跑指定幾集
"""
import os
import sys
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "podcast_out")
STATE = os.path.join(OUT, "state.json")
PROMPT = open(os.path.join(HERE, "podcast_prompt.txt"), encoding="utf-8").read().strip()

# notebooklm CLI 路徑（uv tool 安裝在 ~/.local/bin）
NLM = os.path.expanduser("~/.local/bin/notebooklm")
if not os.path.exists(NLM):
    NLM = "notebooklm"  # fallback 到 PATH

BASE_URL = "https://wellap.cooperation.tw/lectures/"
LANG = "zh_Hant"        # 繁體中文（zh-TW 是無效碼，會被 CLI 擋下）
FORMAT = "deep-dive"    # 兩位主持人對談式
LENGTH = "default"      # default ~10-15 分鐘；要涵蓋更多 feature 可改 "long"
GEN_TIMEOUT = 1800      # 單集生成最多等 30 分鐘
MIN_BYTES = 500_000     # 真實音檔至少 ~0.5MB，低於視為失敗（無聲失敗防線）

# (module_id, 顯示名, 講義檔名) — 對應 lectures/ 實際檔名
MODULES = [
    ("M01", "空氣 Air",            "M01-air.html"),
    ("M02", "水 Water",            "M02-water.html"),
    ("M03", "營養 Nourishment",    "M03-nourishment.html"),
    ("M04", "光 Light",            "M04-light.html"),
    ("M05", "運動 Movement",       "M05-movement.html"),
    ("M06", "溫熱舒適 Thermal",     "M06-thermal.html"),
    ("M07", "聲音 Sound",          "M07-sound.html"),
    ("M08", "材料 Materials",      "M08-materials.html"),
    ("M09", "心理 Mind",           "M09-mind.html"),
    ("M10", "社區 Community",      "M10-community.html"),
    ("M11", "認證 Certification",  "M11-certification.html"),  # 講義較短，品質視試聽結果決定是否補來源
    ("M12", "創新 Innovation",     "M12-innovation.html"),
]


def nlm(args):
    """跑 notebooklm 子指令，回 CompletedProcess。"""
    return subprocess.run([NLM, *args], capture_output=True, text=True)


def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(s):
    json.dump(s, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def ensure_auth():
    r = nlm(["auth", "check", "--json"])
    try:
        status = json.loads(r.stdout).get("status")
    except Exception:
        status = None
    if status != "ok":
        sys.exit("未登入 NotebookLM。先跑：notebooklm login  （需在瀏覽器登入 Google）")


def gen_one(mid, title, fname, state, source_only=False):
    mp3 = os.path.join(OUT, f"{mid}.mp3")
    if os.path.exists(mp3) and os.path.getsize(mp3) > MIN_BYTES:
        return mid, f"SKIP（已存在 {os.path.getsize(mp3)//1024} KB）"

    entry = state.setdefault(mid, {})

    # 1. notebook（已建過就沿用，避免重跑建重複）
    nb = entry.get("notebook")
    if not nb:
        r = nlm(["create", f"WELL AP {mid} {title}", "--json"])
        try:
            nb = json.loads(r.stdout)["notebook"]["id"]
        except Exception:
            return mid, f"FAIL create: {(r.stderr or r.stdout)[-200:].strip()}"
        entry["notebook"] = nb
        save_state(state)

    # 2. add source（公開講義 URL；已加過就略過）
    if not entry.get("source_added"):
        url = BASE_URL + fname
        rs = nlm(["source", "add", url, "-n", nb, "--type", "url", "--timeout", "60", "--json"])
        if rs.returncode != 0:
            return mid, f"FAIL source: {(rs.stderr or rs.stdout)[-200:].strip()}"
        entry["source_added"] = True
        save_state(state)

    # PODCAST_SOURCE_ONLY=1：只 prefill 講義來源、不生成音檔（可先灌好所有模組）
    if source_only:
        return mid, f"SOURCE READY（notebook {nb[:8]}…，講義已上傳）"

    # 3. generate audio（繁中、對談式、等完成）
    rg = nlm(["generate", "audio", PROMPT, "-n", nb,
              "--format", FORMAT, "--length", LENGTH, "--language", LANG,
              "--wait", "--timeout", str(GEN_TIMEOUT), "--retry", "3", "--json"])
    if rg.returncode != 0:
        return mid, f"FAIL generate: {(rg.stderr or rg.stdout)[-200:].strip()}"

    # 4. download（URL 數小時過期，生成完立即抓）
    rd = nlm(["download", "audio", mp3, "-n", nb, "--latest", "--force", "--json"])

    # 5. 驗證實際檔案（不信 returncode，看磁碟上的真檔）
    if os.path.exists(mp3) and os.path.getsize(mp3) > MIN_BYTES:
        return mid, f"DONE {os.path.getsize(mp3)//1024} KB -> {mp3}"
    return mid, f"FAIL verify（無有效音檔）: {(rd.stderr or rd.stdout)[-200:].strip()}"


def main():
    os.makedirs(OUT, exist_ok=True)
    ensure_auth()

    source_only = os.environ.get("PODCAST_SOURCE_ONLY") == "1"
    want = {a.upper() for a in sys.argv[1:]}
    todo = [m for m in MODULES if (not want or m[0] in want)]
    state = load_state()

    mode = "只上傳講義（不生成）" if source_only else "生成音檔"
    print(f"模式：{mode}　要處理：{[m[0] for m in todo]}", flush=True)
    for mid, title, fname in todo:
        print(f"[{mid}] {title} {'上傳中' if source_only else '生成中'}…", flush=True)
        m, s = gen_one(mid, title, fname, state, source_only=source_only)
        print(f"[{m}] {s}", flush=True)
    print("BATCH COMPLETE", flush=True)


if __name__ == "__main__":
    main()
