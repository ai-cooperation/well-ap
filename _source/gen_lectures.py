#!/usr/bin/env python3
"""Generate the WELL AP standard lecture pages (講義) from lectures-data.json.
- lectures/lectures.css                shared style (WELL teal, CJK, reading-glasses, RWD)
- lectures/index.html                  hub linking all 12 concepts
- lectures/M01-air.html ... M12-...     one page per concept, feature-by-feature
- lectures/M11-certification.html       cert+portfolio process (authored, not feature-based)
Content is verbatim from the WELL v2 standard; chrome is Traditional Chinese.
No emoji per house style.
"""
import json, os, html, re

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "lectures")
DATA = json.load(open(os.path.join(HERE, "lectures-data.json")))

SLUG = {"M01":"air","M02":"water","M03":"nourishment","M04":"light","M05":"movement",
        "M06":"thermal","M07":"sound","M08":"materials","M09":"mind","M10":"community",
        "M11":"certification","M12":"innovation"}

# Traditional-Chinese one-line orientation per concept (chrome, not standard text)
INTRO = {
 "M01":"從源頭控制、通風稀釋到監測過濾，建立可量測的室內空氣品質基準線。",
 "M02":"確保飲用與環境用水的化學、微生物與感官品質，並管理水患與衛生。",
 "M03":"以蔬果可得性、營養透明與飲食教育，把健康飲食設計進空間。",
 "M04":"用照度、晝夜節律照明與眩光控制，支持視覺表現與生理時鐘。",
 "M05":"以空間設計與政策鼓勵日常活動，減少久坐、促進身體活動。",
 "M06":"以熱性能、個人控制與監測，維持可接受且可調的熱舒適。",
 "M07":"從聲學規劃、隔音到吸音與背景噪音，管理聲環境品質。",
 "M08":"限制有害物質、提升材料透明度與優化，降低暴露風險。",
 "M09":"以設計、政策與方案支持認知與情緒健康，涵蓋壓力、睡眠與成癮。",
 "M10":"建立包容、互助與韌性的使用者社群，涵蓋健康福利與緊急準備。",
 "M11":"WELL 認證的計分等級、必備門檻、文件與 Performance Verification 流程，以及 WELL Portfolio。",
 "M12":"鼓勵專案提出新介入或採用既有等同成果，最多取得 10 分創新分。",
}

CSS = """
:root{
  --teal:#008F7A; --teal-700:#00715F; --teal-50:#E6F4F1;
  --bg:#fdfdfd; --bg-soft:#f6f8f7; --card:#ffffff; --line:#e4e9e7;
  --text:#1a1f1c; --text-soft:#4d5250; --text-mute:#7d8280;
  --pre:#B4233B; --pre-bg:#FBEAED; --opt:#00715F; --opt-bg:#E6F4F1;
  --radius:12px; --radius-sm:7px; --maxw:880px;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;font-family:"Noto Sans TC",system-ui,sans-serif;color:var(--text);
  background:var(--bg);font-size:18px;line-height:1.75;-webkit-text-size-adjust:100%;}
a{color:var(--teal-700);text-decoration:none;}
a:hover{text-decoration:underline;}
.topbar{position:sticky;top:0;z-index:20;background:rgba(253,253,253,.92);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line);}
.topbar-in{max-width:var(--maxw);margin:0 auto;padding:14px 20px;display:flex;
  align-items:center;gap:14px;}
.brand{font-weight:700;font-size:18px;color:var(--teal-700);white-space:nowrap;}
.brand b{background:var(--teal);color:#fff;border-radius:6px;padding:2px 7px;margin-right:8px;font-size:15px;}
.topbar .sp{flex:1;}
.topbar a.nav{font-size:15px;color:var(--text-soft);}
.wrap{max-width:var(--maxw);margin:0 auto;padding:28px 20px 80px;}
.crumb{font-size:14px;color:var(--text-mute);margin-bottom:8px;}
h1{font-size:30px;line-height:1.3;margin:.2em 0 .1em;letter-spacing:.5px;}
.lede{font-size:18px;color:var(--text-soft);margin:0 0 18px;text-wrap:pretty;}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 26px;}
.chip{font-size:14px;background:var(--bg-soft);border:1px solid var(--line);
  border-radius:999px;padding:5px 13px;color:var(--text-soft);}
.chip b{color:var(--text);}
.toc{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;margin:0 0 30px;}
.toc-h{font-size:13px;letter-spacing:1px;color:var(--text-mute);text-transform:uppercase;margin-bottom:10px;}
.toc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px 18px;}
.toc-grid a{font-size:15.5px;padding:3px 0;display:flex;gap:8px;}
.toc-code{font-family:"JetBrains Mono",monospace;color:var(--teal);font-weight:600;min-width:42px;}
.feat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:22px 24px;margin:0 0 18px;scroll-margin-top:74px;}
.feat-head{display:flex;align-items:baseline;flex-wrap:wrap;gap:10px;margin-bottom:6px;}
.feat-code{font-family:"JetBrains Mono",monospace;font-weight:700;color:var(--teal);font-size:17px;}
.feat-name{font-size:21px;font-weight:700;line-height:1.3;}
.tag{font-size:12.5px;font-weight:600;border-radius:6px;padding:2px 9px;white-space:nowrap;}
.tag.pre{color:var(--pre);background:var(--pre-bg);}
.tag.opt{color:var(--opt);background:var(--opt-bg);}
.intent{margin:10px 0 8px;padding:12px 16px;background:var(--teal-50);
  border-left:4px solid var(--teal);border-radius:0 var(--radius-sm) var(--radius-sm) 0;
  font-size:17px;color:var(--text);text-wrap:pretty;}
.intent .k{font-size:12px;letter-spacing:1px;color:var(--teal-700);text-transform:uppercase;display:block;margin-bottom:2px;}
.summary{color:var(--text-soft);font-size:16.5px;margin:6px 0 14px;text-wrap:pretty;}
.part{border-top:1px solid var(--line);padding-top:12px;margin-top:12px;}
.part-t{font-weight:700;font-size:16.5px;color:var(--teal-700);margin-bottom:4px;}
.part-b{font-size:16px;color:var(--text-soft);text-wrap:pretty;}
.feat-zh{font-size:17px;font-weight:600;color:var(--text-soft);}
.zh-box{background:var(--teal-50);border:1px solid #cfe8e2;border-radius:var(--radius-sm);
  padding:14px 16px;margin:10px 0 12px;}
.zh-h{font-size:12.5px;letter-spacing:1px;color:var(--teal-700);font-weight:700;margin-bottom:7px;}
.zh-sum{font-size:17px;color:var(--text);line-height:1.8;text-wrap:pretty;}
.zh-specs{margin:10px 0 0;padding-left:20px;}
.zh-specs li{font-size:15.5px;color:var(--text-soft);line-height:1.7;margin-bottom:4px;text-wrap:pretty;}
.en-ref{margin-top:6px;border-top:1px dashed var(--line);padding-top:8px;}
.en-ref>summary{cursor:pointer;font-size:13.5px;color:var(--text-mute);letter-spacing:.5px;
  list-style:none;user-select:none;padding:3px 0;}
.en-ref>summary::-webkit-details-marker{display:none;}
.en-ref>summary::before{content:"▸ ";color:var(--teal);}
.en-ref[open]>summary::before{content:"▾ ";}
.note{font-size:14.5px;color:var(--text-mute);background:var(--bg-soft);
  border-radius:var(--radius-sm);padding:10px 14px;margin:20px 0;}
/* index hub */
.hub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin-top:24px;}
.hub-card{display:block;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);padding:18px 20px;transition:.15s;}
.hub-card:hover{border-color:var(--teal);box-shadow:0 4px 16px rgba(0,143,122,.10);text-decoration:none;transform:translateY(-2px);}
.hub-card .hc-id{font-family:"JetBrains Mono",monospace;color:var(--teal);font-weight:700;font-size:14px;}
.hub-card .hc-name{font-size:19px;font-weight:700;margin:3px 0 6px;color:var(--text);}
.hub-card .hc-meta{font-size:14px;color:var(--text-mute);}
.hub-card .hc-desc{font-size:15px;color:var(--text-soft);margin-top:8px;line-height:1.6;text-wrap:pretty;}
@media(max-width:600px){
  body{font-size:17px;}
  h1{font-size:25px;} .feat{padding:18px 16px;} .wrap{padding:20px 15px 60px;}
  .feat-name{font-size:19px;} .brand{font-size:16px;}
  .toc-grid{grid-template-columns:1fr;}
}
"""

def esc(s): return html.escape(s or "")

def feature_html(f):
    tag = ('<span class="tag pre">必備 Precondition</span>' if f["type"]=="precondition"
           else '<span class="tag opt">加分 Optimization</span>')
    # Chinese quick-study block (for fast learning) — shown first
    zh = ""
    if f.get("zh_summary") or f.get("zh_specs"):
        specs = "".join(f'<li>{esc(s)}</li>' for s in f.get("zh_specs", []))
        specs_html = f'<ul class="zh-specs">{specs}</ul>' if specs else ""
        zh = (f'<div class="zh-box"><div class="zh-h">中文重點 · 快速學習</div>'
              f'<div class="zh-sum">{esc(f.get("zh_summary",""))}</div>{specs_html}</div>')
    zh_name = f'<span class="feat-zh">{esc(f["zh_name"])}</span>' if f.get("zh_name") else ""
    # English reference (collapsible)
    parts = ""
    for p in f["parts"]:
        parts += f'<div class="part"><div class="part-t">{esc(p["title"])}</div><div class="part-b">{esc(p["body"])}</div></div>'
    summ = f'<div class="summary">{esc(f["summary"])}</div>' if f["summary"] else ""
    intent = (f'<div class="intent"><span class="k">Intent 目的</span>{esc(f["intent"])}</div>'
              if f["intent"] else "")
    en = (f'<details class="en-ref"><summary>英文原文 standard reference</summary>'
          f'{intent}{summ}{parts}</details>')
    return (f'<section class="feat" id="{f["code"]}">'
            f'<div class="feat-head"><span class="feat-code">{f["code"]}</span>'
            f'<span class="feat-name">{esc(f["name"])}</span>{zh_name}{tag}</div>'
            f'{zh}{en}</section>')

def page_shell(title, body):
    return (f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(title)}</title>'
            f'<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="lectures.css?v=2"></head><body>'
            f'<div class="topbar"><div class="topbar-in">'
            f'<span class="brand"><b>WA</b>WELL AP 標準講義</span><span class="sp"></span>'
            f'<a class="nav" href="index.html">講義總覽</a>'
            f'<a class="nav" href="../index.html">回學習站</a>'
            f'</div></div><div class="wrap">{body}</div></body></html>')

def concept_page(mid, data):
    feats = data["features"]
    npre = sum(1 for x in feats if x["type"]=="precondition")
    nopt = len(feats)-npre
    toc = '<div class="toc"><div class="toc-h">本概念 Features</div><div class="toc-grid">' + "".join(
        f'<a href="#{f["code"]}"><span class="toc-code">{f["code"]}</span>{esc(f["name"])}</a>' for f in feats
    ) + '</div></div>'
    chips = (f'<div class="chips"><span class="chip"><b>{len(feats)}</b> features</span>'
             f'<span class="chip"><b>{npre}</b> 必備 precondition</span>'
             f'<span class="chip"><b>{nopt}</b> 加分 optimization</span></div>')
    body = (f'<div class="crumb"><a href="index.html">講義總覽</a> · {mid}</div>'
            f'<h1>{esc(data["name"])}</h1><p class="lede">{esc(INTRO[mid])}</p>'
            f'{chips}{toc}'
            f'<div class="note">內容為 WELL v2 (Q4 2020) 標準原文之結構化整理，僅保留 Intent / Summary / Parts；'
            f'完整條文與註腳請對照官方 WELL v2 standard。</div>'
            + "".join(feature_html(f) for f in feats))
    return page_shell(f'{data["name"]} · WELL AP 標準講義', body)

# ---- M11 Certification & Portfolio (authored from cert facts, not feature-based) ----
M11_SECTIONS = [
 ("認證等級與計分", [
   "WELL v2 共 110 分可爭取，分四個認證等級：WELL Bronze 40 分、WELL Silver 50 分、WELL Gold 60 分、WELL Platinum 80 分。",
   "每等級皆須先達成全部 24 個 preconditions（強制門檻，100% 達成，不可部分）。",
   "各等級對「每個 concept 的最低分」要求不同：Silver 每概念至少 1 分、Gold 每概念至少 2 分、Platinum 每概念至少 3 分；Bronze 不要求 optimization。",
   "WELL v2 共有 10 個 concepts、24 個 preconditions、98 個 optimizations；Innovation concept 最多 10 分。",
 ]),
 ("專案類型與註冊", [
   "WELL v2 專案主要分兩大類：owner-occupied 與 WELL Core。",
   "專案於 projects.wellcertified.com 註冊（registration）。WELL 由 Delos 開創、IWBI（public benefit corporation）管理、GBCI 負責認證執行。",
   "自註冊日起，專案有 5 年完成文件提交並安排 Performance Verification。",
 ]),
 ("文件與角色", [
   "需提交 annotated documents，類型包含 design drawings 與 operations schedules。",
   "Letter of Assurance 須由具執照的專業簽署（如 architects、engineers、contractors）；property managers 不在此列。",
   "角色分工：owner / WELL project administrator / WELL AP（協助流程）/ WELL Assessor（GBCI 訓練核可的 Performance Testing Agent，執行現場測試）。",
 ]),
 ("Performance Verification 與認證後維持", [
   "新建專案安排 Performance Verification 的條件：documentation 經核准、取得使用執照滿一個月、且達 50% occupancy。",
   "既有建築應在 Documentation Review 於 WELL Online 標記 approved 後，才安排 Performance Verification。",
   "performance testing 需可涵蓋至少 2.5% 的 total building floor area；專案過大時，WELL Assessor 可雇用其督導下的 pre-qualified testing organization 協助。",
   "認證後須持續回報以維持狀態：occupancy survey 結果、維護紀錄、環境參數監測等。New/Existing Building 每 3 年申請 recertification。",
 ]),
 ("WELL Portfolio", [
   "WELL Portfolio 讓組織能規模化（at scale）提升 well-being 並改善人們所處場所。",
   "enrollment period 為六個月，可再延長六個月（最多一年）；最低承諾為五年訂閱。",
   "defined portfolio 至少 10 個專案；若成員全球總 portfolio 少於 10 個，最低為 2 個。",
   "portfolio administrator 監督計畫流程並協調 defined portfolio 的文件作業。",
   "documentation scales：individual-scale documents、shareable documents 與 guideline documents。feature review 期間，project documents 與 performance testing results 可在任何時間上傳。GBCI 訓練並核可 WELL Portfolio 的 Performance Testing Agents。",
 ]),
]
def m11_page():
    body = (f'<div class="crumb"><a href="index.html">講義總覽</a> · M11</div>'
            f'<h1>WELL 認證與 Portfolio</h1><p class="lede">{esc(INTRO["M11"])}</p>'
            f'<div class="chips"><span class="chip"><b>110</b> 分</span>'
            f'<span class="chip"><b>4</b> 等級</span><span class="chip"><b>24</b> preconditions</span></div>'
            f'<div class="note">本頁為 WELL 認證流程與 WELL Portfolio 的重點整理（非 feature 條文）。'
            f'數值依 WELL v2 與認證指南，實際以官方 WELL Online 與 certification guidebook 為準。</div>')
    for i,(t,items) in enumerate(M11_SECTIONS,1):
        lis = "".join(f'<div class="part-b">• {esc(x)}</div>' for x in items)
        body += f'<section class="feat"><div class="feat-head"><span class="feat-code">{i}</span><span class="feat-name">{esc(t)}</span></div>{lis}</section>'
    return page_shell("WELL 認證與 Portfolio · WELL AP 標準講義", body)

def index_page():
    cards = ""
    order = ["M01","M02","M03","M04","M05","M06","M07","M08","M09","M10","M11","M12"]
    names = {**{k:DATA[k]["name"] for k in DATA}, "M11":"WELL 認證與 Portfolio"}
    for mid in order:
        if mid == "M11":
            meta = "認證流程 · Portfolio"
        else:
            feats = DATA[mid]["features"]; npre=sum(1 for x in feats if x["type"]=="precondition")
            meta = f'{len(feats)} features · {npre} 必備'
        cards += (f'<a class="hub-card" href="{mid}-{SLUG[mid]}.html">'
                  f'<div class="hc-id">{mid}</div><div class="hc-name">{esc(names[mid])}</div>'
                  f'<div class="hc-meta">{meta}</div>'
                  f'<div class="hc-desc">{esc(INTRO[mid])}</div></a>')
    body = (f'<h1>WELL AP 標準講義</h1>'
            f'<p class="lede">依 WELL v2 的 11 個 Knowledge Domains 加 Innovation 整理，逐 feature 列出 '
            f'Intent、Summary 與 Parts。先讀懂標準，再進學習站做三問法測驗。</p>'
            f'<div class="note">資料來源：WELL v2 (Q4 2020) 標準原文之結構化整理，僅供學習參考；'
            f'正式條文以 IWBI 官方文件為準。</div>'
            f'<div class="hub-grid">{cards}</div>')
    return page_shell("WELL AP 標準講義 · 總覽", body)

def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT,"lectures.css"),"w").write(CSS)
    n=0
    for mid,data in DATA.items():
        open(os.path.join(OUT,f"{mid}-{SLUG[mid]}.html"),"w").write(concept_page(mid,data)); n+=1
    open(os.path.join(OUT,"M11-certification.html"),"w").write(m11_page()); n+=1
    open(os.path.join(OUT,"index.html"),"w").write(index_page())
    print(f"wrote {n} concept pages + index + lectures.css -> {OUT}")
    print("pages:", sorted(os.listdir(OUT)))

if __name__ == "__main__":
    main()
