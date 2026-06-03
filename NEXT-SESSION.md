# WELL AP 學習站 — 維護指引（已上線）

> 專案在 `/Users/user/projects/wellap/`。**已上線**：https://wellap.cooperation.tw
> 開新 session 先讀本檔 + `engine/content-schema.json`（content pack 合約）。

## 貼這段給 Claude（新 session 開場）

```
WELL AP 學習站維護。專案 /Users/user/projects/wellap/，已上線 https://wellap.cooperation.tw。
架構＝three-question-engine（快照在 engine/）＋ WELL v2 content pack（content.js）＋ Firebase 後端。
先讀 NEXT-SESSION.md（本檔）。重點：題庫在 Firebase 不在 content.js；改 content.js 用 _source/content_io.py；改 JS 必 ?v= bump。
```

---

## 這是什麼

WELL AP（健康建築認證專家）考試學習站。
- **架構**：`three-question-engine`（通用三問法引擎，快照在 `engine/`）＋ WELL v2 content pack（`content.js`）＋ Firebase（登入 + 題庫 + 進度）＋ 獨立 `lectures/` 講義頁。
- **語言**：中文 UI + 英文術語保留（feature 名 / 門檻 / 標準引用用英文）。
- **存取模型**（核心設計）：
  - **講義（`lectures/`）= 公開**，匿名可讀。
  - **學習系統（三問法 / 題庫 / 測驗）= 必須 Google 登入**。
  - **題庫資料只在 Firebase**，`content.js` 不含任何題目；登入後才從 RTDB 抓。

## 目前狀態（2026-06-04）— 全部完成上線

| 項目 | 狀態 |
|---|---|
| content pack 結構 | ✅ 12 模組（M01-M12，含 M12 創新）+ frameworks + debates |
| 題庫 | ✅ **563 題**（第三方考古題補強）在 Firebase RTDB，content.js 內為空 |
| 標準講義 | ✅ 12 概念頁逐 feature（120 features）英文原文 + 中文重點 + 中英名稱對照 + hub |
| 引擎 | ✅ 答錯深連對應 feature 講義、登入牆、loadQuestionBank |
| Firebase | ✅ 專案 wellap-learn，RTDB asia-southeast1，rules 鎖定，Google 登入啟用 |
| 部署 | ✅ ai-cooperation/well-ap (public) → GitHub Pages → Cloudflare DNS → HTTPS Enforce |
| 驗證 | ✅ 自驗 + copilot 獨立交叉驗證 ALL PASS（匿名讀題庫 401） |

---

## 上線架構 / 維護 SOP

### Firebase（專案 `wellap-learn`，永久不可改）
- **RTDB**：`https://wellap-learn-default-rtdb.asia-southeast1.firebasedatabase.app`（asia-southeast1）
- **web config**：在 `content.js` 的 `firebase` 欄（apiKey 等，client 端公開安全，靠 rules 防護）
- **Auth**：Google provider 已啟用；Authorized domains 含 `wellap.cooperation.tw`
- **RTDB 路徑**（packId = `wellap`）：
  - `wellap/question_bank/<moduleId>/<qid>` — 題庫（登入才讀、禁客戶端寫）
  - `wellap/users_auth/<uid>/...` — 個人進度（限本人讀寫）
  - `wellap/analytics/...`、`wellap/question_pool/...` — 統計 / AI 題快取（登入讀寫）
- **Security rules**：原始檔 `_source/database.rules.json`。**RTDB 讀權限會向下繼承且子節點無法收回** → 不要在 `wellap` 層給 `.read`，要逐子路徑給（否則任一登入者能讀別人進度）。
  - 部署：`curl -X PUT "<DBURL>/.settings/rules.json" -H "Authorization: Bearer $(gcloud auth print-access-token)" --data-binary @_source/database.rules.json`
  - 管理 API 操作需 `-H "x-goog-user-project: wellap-learn"` + 先 `gcloud services enable firebasedatabase.googleapis.com`

### 登入閘架構（如何做到「題庫鎖登入」）
- `content.js` 出貨時所有 module 的 `questions: []`（題庫不在靜態檔）。
- `index.html` init：未登入 → `renderLoginGate()`（只給登入鈕 + 講義連結，不渲染 dashboard）。
- 登入後 → `ThreeQuestionEngine.loadQuestionBank()`（引擎方法，讀 `wellap/question_bank` 填回 `module.questions`）→ `renderEntry()`。
- 講義是獨立靜態頁（`lectures/`），不經引擎、不閘。

### 部署（GitHub Pages + Cloudflare）
- repo：`ai-cooperation/well-ap`（**public**，HTTPS remote，照 github-multi-account 規則）
- Pages：master root；`CNAME` 檔 = `wellap.cooperation.tw`；Enforce HTTPS 已開
- Cloudflare DNS：`CNAME wellap → ai-cooperation.github.io`，**DNS only（灰雲）**
- ⚠️ **憑證踩雷**：先開 Pages、DNS 後指過來 → GitHub 試簽一次失敗後不重試，cert state 卡 `None`（相同值 cname PUT 觸發不了）。**解法：移除 CNAME 檔 push（清 custom domain）→ 等 build → 重加 CNAME push** = 強制重簽，20 秒內 approved。

---

## 改題庫 / 重生流程（`_source/` pipeline）

> ⚠️ **題庫在 Firebase**，不在 content.js。改完題目務必重跑 `split_for_firebase.py` + 重新 upload 到 RTDB，否則線上不變。

考古題 → 上線題庫的腳本鏈（依序）：
1. `parse_quizzes.py` — 解 PDF 練習題 → `quizzes-parsed.json`
2. `transform_to_schema.py` — → `questions-skeleton.json`（機械 framework 對映）
3. codex 補強（`prep_codex_in.py` → `run_codex_batch.py` → `codex_out/`）→ `validate_enriched.py` 驗
4. `inject_questions.py` — 注入 content.js（+ `suspects-report.json` 待審清單）
5. `correct_and_shuffle.py` — 正解修正（4 題）+ 選項順序打散平衡（含位置型選項 All/None of the above 不洗）
6. `split_for_firebase.py` — 抽題到 `firebase-bank.json` + content.js 清空 + 寫 firebase config
7. upload：`curl -X PUT "<DBURL>/wellap/question_bank.json" -H "Authorization: Bearer $(gcloud auth print-access-token)" --data-binary @_source/firebase-bank.json`

講義腳本鏈：
- `extract_lectures.py` — 從 `wellv2-standard.txt` 抽 120 features → `lectures-data.json`（header 有 form-feed `\f`、β feature、P/O 換行等坑已處理）
- 中文：`zh_in/` → `run_zh_batch.py`（codex）→ `zh_out/` → `merge_zh.py`（含數值一致性校驗）
- `gen_lectures.py` — 產 `lectures/*.html` + hub + `lectures.css`
- `wire_lectures.py` — 每題從 stem 抽 feature code 存 `lectureRefs`（答錯深連用）

共用：`content_io.py`（load/save content.js，保 `const WELLAP_CONTENT = {...}` 包裝）。**改 content.js 一律用它 round-trip，不要手改。**

## 引擎改動（已分歧，需手動 re-sync 回 three-question-engine）

`engine/` 是快照，本專案改了：
- `learn-engine.js`：`getLectureLinks` 重寫（feature 深連 `lectures/<page>#<CODE>`）、新增 `loadQuestionBank`
- `learn-ui.js` / `learn-layer2.js`：答錯流程傳 q 給 getLectureLinks
- `index.html`：登入牆 + loadQuestionBank 串接

## 維護注意（踩雷教訓）

- **改 JS/CSS 必 `?v=` cache-bust**（index.html 的 script 標籤，目前 v=4）。
- **新域名上線必同步加 proxy CORS 白名單**：AI 追問引擎打 `api.cooperation.tw`（共用 Worker `ai-cooperation/learn-api-proxy`，本機 `~/Desktop/AI100講/learn-api-proxy/src/index.js`）。`ALLOWED_ORIGINS` 沒收域名 → 瀏覽器 POST 回 403 →「AI 暫時無法回應」。修：加 origin 進清單 → `wrangler deploy`（authed alan.chen75@）→ commit/push。2026-06-04 wellap 上線就踩過。
- **引擎硬編 level id `l1`/`l2`**（s100 慣例）：wellap level id 是 `ap`，原「開始學習」按鈕寫死 `practice-l1` → `_renderPracticeList` 找不到 level → 空白。已修成讀 `levels[0].id`（learn-ui.js 206/290）。新 content pack 的 level id 不叫 l1 時要注意這類硬編。
- **commit content.js 卡 secret hook**：含 Firebase web apiKey（`AIza...`）。Firebase web key 設計上公開、靠 rules 防護，**比照 s100 入庫**，需 `--no-verify`（hook 會重掃已 tracked 的 content.js，所以之後每次 commit 都要）。
- **content schema**（`engine/content-schema.json`）：question = `{id, stem(≥20), options[4]{key,text,depth:1-4}, correct, explanation, framework, diagnosis{3個非正解key:{gap,followup}}, lectureRefs[]}`。引擎對 depth/diagnosis/explanation 缺失有 fallback。
- **raw 來源不入庫**：`_source/` 的 zip / WELL_extracted / *.pdf / wellv2-standard.txt / wellap-handbook.txt 已 gitignore（版權 + 體積）。
- **38 個 suspect 題**（`_source/suspects-report.json`）：codex 對照標準抓到的源頭可疑題（多為題幹 feature 代碼標錯但答案對），已修正其中 4 題正解，其餘逐字保留待人工裁示。

## 相關位置

- 引擎源：`/Users/user/Desktop/AI100講/three-question-engine/`（`examples/wellap/` 已被本專案取代，可刪）
- AI100 memory：`project_three-question-engine.md`、`project_s100-ipas-learn.md`、`reference_deploy-paths.md`
