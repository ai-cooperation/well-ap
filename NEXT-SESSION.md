# WELL AP 學習站 — 接續開發指引

> 來源：2026-06-02 AI100 namespace session 規劃。在 `/Users/user/projects/wellap/` 開新 Claude Code session 後，先讀本檔。

## 貼這段給 Claude（新 session 開場）

```
WELL AP 考試學習站開發。專案在 /Users/user/projects/wellap/。
先讀 NEXT-SESSION.md（本檔）+ engine/content-schema.json（content pack 合約）+ _source/（WELL 來源資料）。
任務：A 生題庫（codex 協助，過 quiz-quality-guard）→ C 雲端上線。
工作規則：先規劃再動手；改 JS/CSS 必 ?v= cache-bust；commit 前 Playwright render 驗證 + 手機版。
```

---

## 這是什麼

WELL AP（WELL 健康建築認證專家）考試學習站。
- **架構** = `three-question-engine`（通用三問法學習引擎）+ WELL v2 content pack。引擎零改動，只填 content pack。
- **語言**：中文 UI + 英文術語保留（feature 名/門檻/標準引用用英文）
- **部署**：獨立 repo + 獨立域名 `wellap.cooperation.tw`（非掛現有 repo 子路徑）
- **版面**：用 S100 引擎 UI（**不套 agent-kb app-shell**——那是 KB 瀏覽用，不適合引導式考試流程；想更新只調 theme tokens）

## 目前狀態（2026-06-02）

| 項目 | 狀態 |
|---|---|
| content pack 結構（codex Phase 1）| ✅ 11 模組 + 45 frameworks + 13 debates，**題庫 questions/reinforcement 全空** |
| 引擎 copy（含 hero 通用化修正）| ✅ engine/ |
| render 驗證 | ✅ HTTP 200、WELL teal #008F7A、11 模組顯示、無 JS error |
| git | ✅ init + commit（本地，未推遠端）|
| **A 題庫（Phase 2）** | ❌ 未做 |
| **C 雲端**（repo/Pages/DNS/Firebase）| ❌ 未做 |

## 檔案結構

```
wellap/
├── index.html / analytics.html / content.js   ← 學習站（content.js = content pack）
├── engine/        ← three-question-engine/engine 的快照（含 hero 修正；未來引擎改進需手動 re-sync）
│   ├── learn-engine.js / learn-ui.js / learn-layer2.js / learn.css
│   ├── analytics-template.html / content-schema.json
├── _source/       ← 生題的事實基礎
│   ├── wellap-handbook.txt    考試藍圖（pdftotext）
│   ├── wellv2-standard.txt    完整 WELL v2 標準（pdftotext，112 features + 門檻）
│   ├── wellv2-standard.pdf    原始（.gitignore）
│   └── README.md
├── CNAME          ← wellap.cooperation.tw
└── .gitignore
```

## 事實來源（生題依據，在 _source/）

- **wellap-handbook.txt**：11 Knowledge Domains + 各域題數（Air 11 / Water 9 / Nourishment 10 / Light 9 / Movement 7 / Thermal Comfort 7 / Sound 8 / Materials 9 / Mind 9 / Community 9 / WELL Certification & Portfolio 12 = **100 題**）+ 各域 Knowledge of/Skill in + sample questions（生題風格校準）+ 及格分 170。
- **wellv2-standard.txt**：完整 WELL v2 (Q4 2020) — 112 features 的 code(A01…)、intent、Parts、門檻數值（如 PM2.5 < 15 µg/m³）。生題的事實精準度靠這個。

## content pack 合約（engine/content-schema.json）

- module 必含：`frameworks` `debates` `questions` `reinforcement`
- question：`{id, stem(≥20), options[4]{key:A-D, text, depth:1-4}, correct, explanation, framework, diagnosis{A-D:{gap,followup}}, lectureRefs}`
- 頂層新增欄位（本 session 加，引擎已支援，fallback 安全）：`hero{title,lede}`、`moduleListIntro`
- questionStyle：`optionLength:[38,55]`, `diffMax:8`, `stemMin:60`（英文術語比 s100 寬）

---

## 下一步任務計畫

### A — Phase 2 題庫（codex 協助）

1. 依各模組 frameworks + wellv2 門檻/Parts + handbook sample Q 風格生題
2. 數量：比照考試權重（Air 11、Cert 12…）或先各 10 seed，引擎 runtime AI 補足模擬考
3. **過濾關（必做，AI 產出 ≠ 可交付）**：`quiz-quality-guard` skill 掃洩答案/選項失衡/陷阱露餡 + questionStyle 約束 + 人工抽審
4. diagnosis 逐選項追問：AI 預生成
5. **考古題**（用戶要求順便抓）：⚠️ WELL AP 真考題版權不公開（handbook 明載「IWBI does not release exam questions」），市面只有**第三方練習題**（prep 商/Quizlet）；只能當**風格/覆蓋率參考**，正解仍是從 WELL v2 標準 AI 生題。抓第三方題時標清來源、不可當官方。

codex prompt 模式（沿用 Phase 1）：read-only 給 _source + schema + 一個 module 範例 → workspace-write 生題 → Claude review + quiz-quality-guard + render 驗證。

### C — 雲端上線（待用戶確認命名）

1. `gh repo create ai-cooperation/well-ap`（**HTTPS 推**，照 github-multi-account 規則，ai-cooperation namespace 必走 HTTPS 不走 SSH）+ push
2. GitHub Pages enable + `wellap.cooperation.tw` Cloudflare CNAME（CNAME 檔已備）
3. Firebase 專案 `wellap-learn`（RTDB asia-southeast1，同 S100 區）→ config 寫進 content.js 的 `firebase` 欄
4. api.cooperation.tw proxy **沿用**（英文內容 Groq/Gemini 都吃，不必新建）

## 已定決策（不要重議）

- 語言：中文 UI + 英文術語
- 部署：獨立 repo + 獨立域名
- 版面：S100 引擎 UI（agent-kb app-shell 已評估否決）
- 執行器：opencode 單獨（Webwright 暫不用）

## 待用戶確認

- repo 名（建議 `ai-cooperation/well-ap`）
- Firebase 專案 ID（建議 `wellap-learn`，**永久不可改**）

## 關鍵教訓 / 注意

- **引擎 hero/intro 原硬編碼 S100**（淨零/iPAS），本 session 已修成讀 content pack（fallback 保留預設）。engine/ 是 three-question-engine 的快照，引擎改進要手動 re-sync 回來。
- **找資料品質結論**：權威源優先 PDF + pdftotext（比 agentic 爬取可靠）；opencode 爬動態站瓶頸在 harness 權限（headless 要預先 allow bash/python，否則卡死）。
- **改 JS/CSS 必 `?v=` cache-bust**；Firebase 路徑變更三方同步（見 AI100 deploy/firebase skill）。
- **部署慣例**：每個學習站自帶引擎 copy（S100 模式），不共用 three-question-engine。

## 相關位置（AI100 namespace = 本規劃來源）

- 引擎源 + s100/ai100 參考範例：`/Users/user/Desktop/AI100講/three-question-engine/`
  - ⚠️ `examples/wellap/` 是本 session 的 staging，**已被本專案取代**，可刪（避免雙份 content.js 飄移）
- AI100 memory：`project_three-question-engine.md`、`project_s100-ipas-learn.md`、`reference_course-onboard.md`、`reference_deploy-paths.md`
- Hermes 自動執行系統 SDD（同 session 另一條線，若 WELL 資料要做自動 ingestion 可參考）：SecondBrain `tech/agent/2026-06-01-Hermes-執行管線-SDD.md`
