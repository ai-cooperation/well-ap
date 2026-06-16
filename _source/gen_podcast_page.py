#!/usr/bin/env python3
"""
gen_podcast_page.py — 產生 podcasts/index.html（通勤 Podcast hub + 全域底部播放器）。

沿用 _source/gen_lectures.py 的「產生器在 _source/、輸出到站台目錄」慣例。
資料源：講義 hub 的概念描述 + ffprobe 量到的時長。每集都標單元名稱（中 + EN）。
改集數 / 時長 / 描述後重跑本檔即可重生整頁。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "podcasts", "index.html")

# (id, 中文名, 英文名, features 標註, 時長 mm:ss, 一句話描述)
EPISODES = [
    ("M01", "空氣", "Air",            "14 features · 4 必備", "24:16", "從源頭控制、通風稀釋到監測過濾，建立可量測的室內空氣品質基準線。"),
    ("M02", "水", "Water",            "9 features · 3 必備",  "13:26", "確保飲用與環境用水的化學、微生物與感官品質，並管理水患與衛生。"),
    ("M03", "飲食", "Nourishment",    "14 features · 2 必備", "17:50", "以蔬果可得性、營養透明與飲食教育，把健康飲食設計進空間。"),
    ("M04", "光", "Light",            "9 features · 2 必備",  "14:57", "用照度、晝夜節律照明與眩光控制，支持視覺表現與生理時鐘。"),
    ("M05", "運動", "Movement",       "11 features · 2 必備", "20:16", "以空間設計與政策鼓勵日常活動，減少久坐、促進身體活動。"),
    ("M06", "熱舒適", "Thermal Comfort", "9 features · 1 必備", "23:51", "以熱性能、個人控制與監測，維持可接受且可調的熱舒適。"),
    ("M07", "聲音", "Sound",          "8 features · 1 必備",  "14:28", "從聲學規劃、隔音到吸音與背景噪音，管理聲環境品質。"),
    ("M08", "材料", "Materials",      "12 features · 3 必備", "28:26", "限制有害物質、提升材料透明度與優化，降低暴露風險。"),
    ("M09", "心理", "Mind",           "11 features · 2 必備", "22:11", "以設計、政策與方案支持認知與情緒健康，涵蓋壓力、睡眠與成癮。"),
    ("M10", "社區", "Community",      "18 features · 4 必備", "17:53", "建立包容、互助與韌性的使用者社群，涵蓋健康福利與緊急準備。"),
    ("M11", "WELL 認證與 Portfolio", "Certification", "認證流程 · Portfolio", "13:28", "WELL 認證的計分等級、必備門檻、文件與 Performance Verification 流程。"),
    ("M12", "創新", "Innovation",     "5 features · 0 必備",  "19:24", "鼓勵專案提出新介入或採用既有等同成果，最多取得 10 分創新分。"),
]

PLAY_SVG = ('<svg class="ep-icon-play" viewBox="0 0 24 24" width="20" height="20">'
            '<polygon points="6,3 20,12 6,21" fill="currentColor"/></svg>'
            '<svg class="ep-icon-pause" viewBox="0 0 24 24" width="20" height="20">'
            '<rect x="5" y="3" width="5" height="18" rx="1" fill="currentColor"/>'
            '<rect x="14" y="3" width="5" height="18" rx="1" fill="currentColor"/></svg>')

# Firebase Web config 的單一來源 = content.js 的 WELLAP_CONTENT.firebase。
# 不在本頁重複寫一份 config（DRY + 避免 secret-scan hook 誤判 Firebase Web apiKey）。
# Firebase Web config 非 secret（ship 在 browser bundle，安全靠 Auth + Security Rules，見 CONSUMERS.md）。
FB_SCRIPTS = (
    '<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>\n'
    '<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>'
)

# 未登入時顯示的登入閘；登入後才顯示 #epArea。
# 注意：這是「介面層」登入閘——音檔仍是公開靜態 URL，非真正內容保護。
# 真保護需經認證端點發送音檔（Cloudflare Worker + signed URL），屬之後接 cooperation-hub 的工作。
AUTH_JS = """(function(){
  if (typeof firebase === 'undefined') return;
  // config 取自 content.js 的 WELLAP_CONTENT.firebase（單一來源，不重複寫）
  var cfg = (typeof WELLAP_CONTENT !== 'undefined' && WELLAP_CONTENT.firebase) || null;
  if (!cfg) { console.error('Firebase config 未載入（content.js?）'); return; }
  firebase.initializeApp(cfg);
  var gate = document.getElementById('loginGate');
  var epArea = document.getElementById('epArea');
  var authBtn = document.getElementById('authBtn');
  function login(){
    var p = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(p).catch(function(e){
      if (e && e.code && e.code.indexOf('popup') >= 0) firebase.auth().signInWithRedirect(p);
    });
  }
  function logout(){ firebase.auth().signOut(); }
  document.querySelectorAll('[data-login]').forEach(function(b){
    b.addEventListener('click', function(e){ e.preventDefault(); login(); });
  });
  firebase.auth().onAuthStateChanged(function(user){
    if (user){
      if (gate) gate.hidden = true;
      if (epArea) epArea.hidden = false;
      if (authBtn){ authBtn.textContent = '登出'; authBtn.onclick = function(e){ e.preventDefault(); if (confirm('登出？')) logout(); }; }
    } else {
      if (gate) gate.hidden = false;
      if (epArea) epArea.hidden = true;
      var a = document.getElementById('gp-audio'); if (a) a.pause();
      var gp = document.getElementById('gp'); if (gp) gp.classList.add('gp--hidden');
      document.body.classList.remove('gp-active');
      var rb = document.querySelector('.gp-resume'); if (rb) rb.remove();
      if (authBtn){ authBtn.textContent = '登入會員'; authBtn.onclick = function(e){ e.preventDefault(); login(); }; }
    }
  });
})();"""


def dur_to_sec(d):
    m, s = d.split(":")
    return int(m) * 60 + int(s)


def card(ep):
    eid, zh, en, meta, dur, desc = ep
    en_html = f'<span class="en">{en}</span>' if en else ''
    return (
        f'<button class="ep-card" data-ep="{eid}" onclick="PodcastPlayer.play(\'{eid}\')" '
        f'aria-label="播放 {eid} {zh} {en}">'
        f'<span class="ep-play" aria-hidden="true">{PLAY_SVG}</span>'
        f'<span class="ep-text">'
        f'<span class="ep-top"><span class="ep-id">{eid}</span>'
        f'<span class="ep-name">{zh} {en_html}</span></span>'
        f'<span class="ep-meta">{meta} · <span class="dur">{dur}</span></span>'
        f'<span class="ep-desc">{desc}</span>'
        f'</span></button>'
    )


def playlist_js():
    rows = []
    for i, (eid, zh, en, meta, dur, desc) in enumerate(EPISODES, 1):
        title = f"{zh} {en}".strip()
        rows.append(
            f'  {{ n:{i}, id:"{eid}", title:"{title}", dur:"{dur}", durSec:{dur_to_sec(dur)}, '
            f'zh:"audio/{eid}.m4a", en:null }}'
        )
    return "var PLAYLIST = [\n" + ",\n".join(rows) + "\n];"


def build():
    cards = "\n".join(card(ep) for ep in EPISODES)
    total_sec = sum(dur_to_sec(ep[4]) for ep in EPISODES)
    total = f"{total_sec // 3600} 小時 {(total_sec % 3600) // 60} 分"

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WELL AP Podcast · 12 概念中文複習</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="podcasts.css?v=2">
{FB_SCRIPTS}
</head>
<body>

<div class="topbar"><div class="topbar-in">
  <span class="brand"><b>WA</b>WELL AP Podcast</span>
  <span class="sp"></span>
  <a class="nav" href="../lectures/index.html">標準講義</a>
  <a class="nav" href="../index.html">回學習站</a>
  <a class="nav" id="authBtn" href="#" style="font-weight:700;color:var(--teal-700);">登入會員</a>
</div></div>

<div class="wrap">
  <h1>Podcast · 中文複習</h1>
  <p class="lede">把 WELL v2 的 12 個概念做成中文對談式 podcast，每集對應一頁標準講義，從考試重點切入：feature 目的、關鍵門檻數值、precondition 與 optimization 的差別。適合通勤時做第一階段的聽覺預習。</p>
  <div class="note">共 12 集 · 總長約 <b>{total}</b>。內容由 NotebookLM 依標準講義生成，屬學習輔助；正式條文與數值以 IWBI 官方文件為準。登入會員後即可收聽，底部播放器支援背景播放、倍速與自動接續下一集。</div>

  <div id="loginGate" class="login-gate">
    <div class="lg-card">
      <div class="lg-title">登入會員後即可收聽</div>
      <p class="lg-sub">這 12 集中文 podcast 為 WELL AP 會員內容。用 Google 帳號登入即解鎖全部單元，支援背景播放與續聽。</p>
      <button class="lg-btn" data-login>使用 Google 登入</button>
      <div class="lg-alt"><a href="../lectures/index.html">先看標準講義 →</a></div>
    </div>
  </div>

  <div id="epArea" hidden>
    <div class="ep-list">
{cards}
    </div>
  </div>
</div>

<!-- Global bottom player -->
<div id="gp" class="gp gp--hidden" role="complementary" aria-label="Podcast 播放器">
  <audio id="gp-audio" preload="metadata"></audio>
  <div class="gp-progress" id="gp-progress"><div class="gp-progress-fill" id="gp-progress-fill"></div></div>
  <div class="gp-body">
    <div class="gp-controls">
      <button id="gp-prev" class="gp-btn" aria-label="上一集" title="上一集">
        <svg viewBox="0 0 24 24" width="20" height="20"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z" fill="currentColor"/></svg>
      </button>
      <button id="gp-play" class="gp-btn gp-btn--play" aria-label="播放">
        <svg class="gp-icon-play" viewBox="0 0 24 24" width="28" height="28"><polygon points="6,3 20,12 6,21" fill="currentColor"/></svg>
        <svg class="gp-icon-pause" viewBox="0 0 24 24" width="28" height="28" style="display:none"><rect x="5" y="3" width="5" height="18" rx="1" fill="currentColor"/><rect x="14" y="3" width="5" height="18" rx="1" fill="currentColor"/></svg>
      </button>
      <button id="gp-next" class="gp-btn" aria-label="下一集" title="下一集">
        <svg viewBox="0 0 24 24" width="20" height="20"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" fill="currentColor"/></svg>
      </button>
    </div>
    <div class="gp-info">
      <a id="gp-title" class="gp-title" href="#">選一集開始</a>
      <span class="gp-time"><span id="gp-cur">0:00</span> / <span id="gp-dur">0:00</span></span>
    </div>
    <div class="gp-right">
      <select id="gp-speed" class="gp-speed" aria-label="播放速度">
        <option value="0.75">0.75x</option>
        <option value="1" selected>1x</option>
        <option value="1.25">1.25x</option>
        <option value="1.5">1.5x</option>
        <option value="2">2x</option>
      </select>
      <button id="gp-close" class="gp-btn gp-btn--close" aria-label="關閉播放器" title="關閉">&times;</button>
    </div>
  </div>
</div>

<script>
{playlist_js()}
</script>
<script src="player.js?v=1"></script>
<!-- content.js 提供 WELLAP_CONTENT.firebase（Firebase config 單一來源） -->
<script src="../content.js?v=3"></script>
<script>
{AUTH_JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    html = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html)} bytes, {len(EPISODES)} episodes)")
