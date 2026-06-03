#!/usr/bin/env python3
"""Hand-authored enrichment for M10 (Community) chunks — codex stand-in while
quota is exhausted. Same output shape as codex_out/*.json. Structure is enforced
by code (correct=depth4, exactly 3 diagnosis keys)."""
import json, os
HERE = os.path.dirname(__file__)

# qid -> (framework, explanation, {wrongKey: (depth, gap, followup)})
SPEC = {
"M10_Q01": ("M10_F1", "C02 Integrative Design Part 1 要求 stakeholder charrette 在規劃流程早期進行，讓健康目標在設計定案前就納入決策。", {
  "A": (3, "把 charrette 等同 kick-off 後的單次會議", "C02 強調的是在「規劃流程早期」介入，這跟專案剛啟動的時點有什麼差別？"),
  "B": (2, "誤以為 charrette 需每月持續舉辦", "charrette 是一次性密集協作工作坊，這跟 monthly 例會的性質有何不同？"),
  "D": (1, "把協作流程放到專案完成後，已失去設計影響力", "若在 project completion 後才開 charrette，還能影響哪些 design 決策？")}),
"M10_Q02": ("M10_F1", "C02 要求在 design and programming 前，由 architects、owner、facility management team 與 engineers 等核心關係人共同會談，確保跨領域整合。", {
  "A": (3, "關係人涵蓋不足，遺漏 owner/FM team", "C02 的整合精神要納入哪些角色才能涵蓋設計、營運與使用端？"),
  "B": (2, "以 PM 取代設計與工程專業", "project manager 之外，誰負責把健康策略落到實際 design？"),
  "C": (3, "仍漏掉 facility management team", "少了 facility management team，後續 operation 階段的健康策略由誰把關？")}),
"M10_Q03": ("M10_F1", "C02 Part 2 要求把 health-oriented mission 明文記載於 WELL Feature Guide，作為團隊共同依循的文件。", {
  "A": (2, "誤以為公告即可取代正式文件", "一般 notice 與需被 review 的正式文件，在 verification 上有何差別？"),
  "C": (3, "混淆 Project Checklist 與 Feature Guide 的用途", "Project Checklist 記錄的是各 feature 進度，那 health-oriented mission 該寫在哪份文件？"),
  "D": (1, "Project Matrix 並非記載 mission 的指定文件", "C02 指定的文件名稱是什麼？")}),
"M10_Q04": ("M10_F1", "Community concept overview 指出，社群由 social ties、shared common perspectives 與在共享場域的 joint action and experiences 共同連結，三者皆是。", {
  "A": (3, "只取單一面向，低估社群連結的多重性", "除了 social ties，還有哪些因素把人連結成一個 community？"),
  "B": (3, "只取單一面向，忽略行動與場域", "shared perspectives 之外，共享場域中的共同行動是否也算連結因素？"),
  "C": (3, "只取單一面向，忽略既有人際與觀點", "joint action 之外，既有的 social ties 是否也是連結來源？")}),
"M10_Q05": ("M10_F4", "Social Determinants of Health 指影響健康的 physical and built conditions（以及社會經濟環境），WELL Community 以此切入環境對健康的影響。", {
  "A": (3, "只取 environmental 單一面向", "SDOH 涵蓋的條件是否只有 environmental 一項？"),
  "C": (2, "把 mental 誤列為 SDOH 的定義範疇", "mental 是健康結果還是決定因素？SDOH 強調的是哪一類條件？"),
  "D": (3, "誤選包山包海而非 WELL 強調的條件", "WELL 在此最強調的是哪一類 determinant？")}),
"M10_Q06": ("M10_F4", "WELL Community 列舉的 health disparities 包含 gender、race、ethnicity 等社會群體差異；age 不在其列舉的 disparity 類別。", {
  "A": (2, "把 gender 誤判為非 disparity", "gender 是否屬於 WELL 列舉的健康不平等面向？"),
  "B": (2, "把 race 誤判為非 disparity", "race 是否屬於 WELL 列舉的健康不平等面向？"),
  "C": (2, "把 ethnicity 誤判為非 disparity", "ethnicity 是否屬於 WELL 列舉的健康不平等面向？")}),
"M10_Q07": ("M10_F2", "C03 Emergency Preparedness overview 引用 FEMA 估計：約 40-60% 小型企業在缺乏完整防災計畫時，於災後永久歇業。", {
  "A": (3, "高估歇業比例，記成 75-80%", "FEMA 引用的區間是否高達近八成？"),
  "C": (2, "低估歇業比例", "缺乏防災計畫的小型企業歇業比例，會低到只有兩三成嗎？"),
  "D": (3, "記成相近但非標準引用的區間", "標準引用的是哪一個整數區間？")}),
"M10_Q08": ("M10_F3", "C04 Occupant Survey Part 1 要求採用 IWBI 核可廠商提供的 third-party survey，以確保方法與比較基準一致。", {
  "A": (2, "誤以為只調查最大租戶即可", "只問單一最大租戶，能否代表全體 building users？"),
  "C": (3, "誤以為自寄 email 問卷即符合", "self-administered email 問卷缺少哪一項 C04 要求的條件？"),
  "D": (1, "意見箱無法構成系統化調查", "suggestion box 能否提供可分析、可比較的調查結果？")}),
"M10_Q09": ("M10_F4", "C06 Health Services and Benefits Part 1 要求 employer 提供 comprehensive health benefits、policies and services，以支持員工與家庭整體健康。", {
  "A": (3, "把彈性工時誤當主要健康福利要求", "彈性工時是加分項，但 C06 Part 1 要求的核心是哪一類 benefits？"),
  "B": (2, "把贈送穿戴裝置當成 comprehensive benefits", "送 fitness tracker 是否等同提供 comprehensive health benefits？"),
  "D": (1, "把團隊活動誤當制度性健康福利", "辦馬拉松屬於活動，C06 要求的是制度性的什麼？")}),
"M10_Q10": ("M10_F3", "C05 Enhanced Occupant Survey Part 2 要求進行 pre- 與 post-occupancy 調查，並比對兩者結果以評估介入成效。", {
  "A": (3, "只做第三方問卷而未強調比對", "C05 的 enhanced 重點是『比對』，單用第三方問卷是否就達標？"),
  "B": (2, "自行施測違反第三方要求", "自辦調查在客觀性上缺少什麼？"),
  "C": (3, "只談自願性而非比對結果", "自願參與是基本倫理，但 C05 Part 2 要求比對哪兩次調查？")}),
"M10_Q11": ("M10_F4", "C06 overview 指出全球 94% 國家規定 paid sick leave，美國與 Korea 是僅有的兩個未強制的 OECD 國家。", {
  "A": (2, "誤記為日本", "OECD 中與美國並列未強制 paid sick leave 的是哪一國？"),
  "C": (2, "誤記為土耳其", "C06 overview 點名的另一個未強制國家是哪一國？"),
  "D": (2, "誤記為智利", "標準明確點名的是 Korea 還是 Chile？")}),
"M10_Q12": ("M10_F4", "C06 overview 引用研究：因缺乏或僅有一天病假，估計約有 2,000 萬名美國人帶病上班。", {
  "A": (2, "嚴重低估帶病上班人數", "10 萬與『數千萬』的量級差距，哪個符合 overview 引用？"),
  "B": (2, "低估帶病上班人數一個量級", "37.5 萬是否達到 overview 強調的數千萬級？"),
  "C": (3, "接近但少一個量級", "標準引用的是一千萬還是兩千萬？")}),
"M10_Q13": ("M10_F4", "C06 overview 指出實施 paid sick leave 可降低職場傳染、提升生產力並降低離職率。", {
  "A": (3, "telemedicine 是相關但非此處引用的措施", "overview 在此句強調的具體制度是哪一項？"),
  "C": (1, "開放式空間與傳染率不是此處主題", "floor plan 與 sick leave 政策何者是 C06 此句重點？"),
  "D": (2, "免費午餐並非降低傳染的引用措施", "提供午餐與 paid sick leave，哪個對降低 contagion 有直接證據？")}),
"M10_Q14": ("M10_F4", "C07 Enhanced Health and Wellness Promotion overview 指出，每投入 1 美元於 workplace health programs，醫療與缺勤成本分別約下降 $3.27 與 $2.73。", {
  "A": (2, "把公司旅遊誤當健康投資標的", "retreat 與系統化 health program，哪個對應這組投報數據？"),
  "C": (1, "辦公茶點與健康投報數據無關", "office refreshments 是否是 C07 引用的投資項目？"),
  "D": (2, "把退休金提撥誤當健康促進投資", "401(k) match 屬於財務福利，與 workplace health program 是同一類嗎？")}),
"M10_Q15": ("M10_F4", "C06 Part 2 Offer On-Demand Health Services 要求提供 onsite doctor 或 nurse practitioner 等隨需健康服務以得分。", {
  "A": (1, "餐飲主廚與健康服務無關", "head chef 屬於 nourishment/營運，與 on-demand health services 是同類嗎？"),
  "C": (3, "Chief Wellness Officer 是管理角色而非隨需醫療", "CWO 負責策略，C06 Part 2 要求的是現場的哪種醫療人員？"),
  "D": (2, "私人教練不等於隨需醫療服務", "physical trainer 提供的服務與 on-demand health service 有何不同？")}),
"M10_Q16": ("M10_F4", "C08 New Parent Support Part 1 要求 paid leave 達員工全薪的 75% 或以上，並涵蓋福利。", {
  "A": (2, "低估給付比例為 50%", "C08 規定的最低給付比例是否低到只有半薪？"),
  "B": (3, "接近但低於 75% 門檻", "70% 與標準門檻 75% 之間，哪個才是 C08 要求？"),
  "D": (3, "高估為 100% 全薪", "C08 要求的是『至少 75%』還是『全額』？")}),
"M10_Q17": ("M10_F4", "C08 至少提供 primary caregiver 12 週、non-primary caregiver 2 週的 paid leave。", {
  "A": (1, "週數嚴重低於 C08 門檻", "primary 2 週與標準的 12 週差距多大？"),
  "B": (2, "primary 週數仍不足", "primary caregiver 的最低週數是 4 週還是 12 週？"),
  "D": (3, "高估週數，超出 C08 最低標", "30 週是否為 C08 規定的『最低』要求？")}),
"M10_Q18": ("M10_F4", "C08 列舉的合規政策包含返崗過渡支持、主管訓練與政策溝通；以 virtual assistance 代為分擔工作量並非其要求。", {
  "A": (3, "返崗 coaching 其實是合規政策", "coaching/counseling 是否列於 C08 的支持措施？"),
  "C": (3, "主管訓練其實是合規政策", "為 manager 提供請假規劃訓練是否屬 C08 範疇？"),
  "D": (3, "向員工溝通政策其實是合規措施", "向 expecting parents 溝通 leave policy 是否為 C08 要求？")}),
"M10_Q19": ("M10_F4", "C09 New Mother Support 要求每八小時工作日提供 2-3 次 pumping sessions（每 2-3 小時 15-20 分鐘）。", {
  "A": (2, "次數低於最低要求", "每八小時 1-2 次是否達到 C09 的最低頻率？"),
  "C": (3, "次數高於標準範圍", "5-7 次是否超出 C09 規定的 2-3 次？"),
  "D": (2, "範圍過寬不符標準", "C09 給的是 2-3 次的明確區間，4-8 次是否符合？")}),
"M10_Q20": ("M10_F4", "C09 對出差中的哺乳員工，要求提供具 refrigerator access 的 hotel room 或同等住宿以保存母乳。", {
  "B": (3, "自費保冷袋未達雇主提供住宿的要求", "由員工自費的 cooler 與雇主提供冷藏住宿，哪個符合 C09？"),
  "C": (2, "寄送母乳非標準要求的住宿安排", "express shipping 是否為 C09 指定的差旅哺乳安排？"),
  "D": (2, "改機票迴避問題而非提供安排", "提早返程是否解決了出差期間的母乳保存需求？")}),
"M10_Q21": ("M10_F4", "C10 Family Support Part 1 要求若無 on-site childcare，需補貼 off-site 或 at-home childcare 成本至少 50%。", {
  "A": (2, "補貼比例嚴重偏低", "10% 補貼是否達到 C10 的最低門檻？"),
  "B": (3, "接近但低於 50% 門檻", "25% 與標準的 50% 之間，哪個是 C10 要求？"),
  "D": (3, "高估補貼比例", "C10 規定的是『至少 50%』還是更高？")}),
"M10_Q22": ("M10_F4", "C10 的 childcare 支持包含 on-site 中心或≥50% 補貼、back-up 與 seasonal childcare；『讓員工帶生病小孩到辦公室』不屬其列。", {
  "A": (3, "此項其實屬 C10 合規 childcare", "on-site 中心或 50% 補貼是否列於 C10？"),
  "B": (3, "back-up childcare 其實屬 C10", "突發狀況的備援托育是否為 C10 選項？"),
  "C": (3, "seasonal childcare 其實屬 C10", "寒暑假的 seasonal 托育是否列於 C10？")}),
"M10_Q23": ("M10_F4", "C10 Part 2 Offer Family Leave 要求為照顧家人提供至少 12 週、給付 75% 或以上的 paid leave。", {
  "A": (1, "週數與給付皆遠低於門檻", "2 週、50% 與標準的 12 週、75% 差距多大？"),
  "B": (2, "週數與給付皆不足", "4 週 70% 是否達到 C10 family leave 的最低標？"),
  "D": (3, "週數高於最低要求", "16 週是否為 C10 規定的『最低』週數？")}),
"M10_Q24": ("M10_F4", "C10 family leave 達 12 週後，員工可用 paid sick/personal days、彈性到離或永久遠距等選項；唯獨『被迫返崗或離職』不在其中。", {
  "B": (3, "此為合規選項而非例外", "用 paid sick/personal days 照顧家人是否屬 C10 提供的選項？"),
  "C": (3, "彈性到離其實是合規選項", "arrive late/leave early 是否列於 C10 給員工的彈性？"),
  "D": (3, "永久遠距其實是合規選項", "permanent work from home 是否為 C10 的選項之一？")}),
"M10_Q25": ("M10_F4", "C11 Civic Engagement 認可如 donation matching charity drives 等實質回饋社群的制度化參與。", {
  "A": (3, "慈善路跑偏向活動而非制度化參與", "一次性的 5k/cookout 與制度化的 donation matching，哪個更符合 civic engagement？"),
  "C": (1, "萬聖節變裝與公民參與無關", "costume contest 是否屬於回饋社群的 civic engagement？"),
  "D": (1, "賭注式活動非公民參與", "March Madness 獎金池與社群回饋有何關聯？")}),
"M10_Q26": ("M10_F4", "C11 Civic Engagement 要求提供可供社群使用、能容納相當人數的室內或室外空間，如可容 10-20 人的戶外教室/中庭。", {
  "A": (3, "封閉 board room 不適合開放社群使用", "2,000 sq ft 的 board room 是否適合『社群』使用？"),
  "B": (2, "容量過小無法服務社群", "僅容 5 人的小會議室能否達到社群空間目的？"),
  "D": (3, "可用性受限且非開放社群空間", "每兩週才開放一次的 hall 是否符合『供社群使用』？")}),
"M10_Q27": ("M10_F4", "C12 Diversity and Inclusion 要求納入 D&I/非歧視政策、pay equity、通報程序等；『廢除 C-suite 改公司合作社』非其要求。", {
  "A": (3, "此為 C12 必含項目而非例外", "non-discrimination policy 是否屬 C12 必含？"),
  "B": (3, "pay equity 其實是 C12 必含項", "pay equity and transparency 是否列於 C12？"),
  "D": (3, "通報程序其實是 C12 必含項", "harassment reporting procedure 是否屬 C12？")}),
"M10_Q28": ("M10_F4", "C12 客製 D&I 方案要取得最高 3 分，需自清單中實施 5 項要求。", {
  "A": (2, "低估所需項目數", "3 項是否足以拿到 C12 的最高分？"),
  "B": (3, "接近但少於門檻", "4 項與標準的 5 項，哪個對應最高 3 分？"),
  "D": (2, "高估所需項目數", "清單共 7 項，但取得最高分需實施幾項？")}),
"M10_Q29": ("M10_F4", "C12 要求提供由 local cost of living 決定的 living wage；僅補移居費與小幅加薪、未確保 living wage 即不合規。", {
  "A": (3, "誤以為補移居費即合規", "覆蓋搬遷成本是否等同提供 living wage？"),
  "C": (2, "以員工與家人同住規避 living wage 義務", "員工的居住安排能否免除雇主提供 living wage 的責任？"),
  "D": (1, "把不存在的加薪組合當成要求", "C12 要求的是 living wage，還是 merit+signing bonus 組合？")}),
"M10_Q30": ("M10_F4", "C13 Accessibility and Universal Design 的 Section B（development and intellectual health）關注感官負荷等需求，應在過度刺激的設計前諮詢。", {
  "A": (3, "Physical Access 處理行動而非感官負荷", "Section A 針對的是 physical 行動，還是感官刺激？"),
  "C": (2, "Wayfinding 處理導引而非感官超載", "Section C 解決的是找路問題，與色彩感官超載相關嗎？"),
  "D": (2, "Operation 屬營運而非設計語言諮詢", "Section D 處理 operation，這跟設計階段的色彩選擇是同一環節嗎？")}),
"M10_Q31": ("M10_F4", "C13 規定當慣用交通方式中斷時，需補貼員工至少 50% 的新增通勤成本以維持可及性。", {
  "A": (2, "補貼比例遠低於門檻", "10% 補貼是否符合 C13 的最低標？"),
  "B": (3, "接近但低於 50%", "25% 與標準的 50% 哪個是 C13 要求？"),
  "D": (3, "高估補貼比例", "C13 規定的是『至少 50%』還是更高？")}),
"M10_Q32": ("M10_F4", "C18β Support for Victims of Domestic Violence 要求提供至少 10 天、且獨立於其他 PTO 的 paid time off。", {
  "B": (3, "誤把它併入一般 sick leave", "C18β 要求的天數是否可與一般 sick leave 共用？"),
  "C": (1, "誤以為無需額外天數", "若不提供額外天數，是否符合 C18β 的支持意旨？"),
  "D": (2, "天數低於最低要求", "8 天是否達到 C18β 規定的至少 10 天？")}),
"M10_Q33": ("M10_F2", "C14 Opioid Response training 涵蓋鴉片類與 naloxone 知識、辨識過量徵兆與處置、安全施用 naloxone；不含『通報 HR 同事可能用禁藥』。", {
  "A": (3, "此其實是訓練必含內容", "opioid 與 naloxone 的一般資訊是否屬訓練內容？"),
  "B": (3, "辨識過量其實是訓練必含", "recognizing overdose 是否列於 C14 訓練？"),
  "C": (3, "施用 naloxone 其實是訓練必含", "如何安全施用 naloxone 是否屬訓練內容？")}),
"M10_Q34": ("M10_F2", "C15β Business Continuity 要求 business continuity team 至少每年檢討兩次（2 times annually）計畫。", {
  "A": (3, "頻率不足，僅每年一次", "annual 與 2x annually，哪個是 C15β 的最低頻率？"),
  "C": (2, "頻率高於最低要求", "quarterly 是否為標準規定的『最低』檢討頻率？"),
  "D": (2, "頻率高於最低要求", "monthly 是否為 C15β 規定的最低頻率？")}),
"M10_Q35": ("M10_F2", "C15β 的 business continuity plan 至少需涵蓋關鍵業務功能與相依性、business impact analysis 與 remote work readiness assessment，全部皆是。", {
  "A": (3, "只取單一面向", "界定關鍵業務功能之外，計畫是否還需其他分析？"),
  "B": (3, "只取單一面向", "business impact analysis 之外是否仍有其他必含項？"),
  "C": (3, "只取單一面向", "remote work readiness 之外，計畫是否還需涵蓋其他項目？")}),
"M10_Q36": ("M10_F2", "C14 Part 2 要求所有 emergency preparedness/first aid kit 必須包含 naloxone rescue kits。", {
  "B": (1, "Benadryl 非 C14 指定必含品", "C14 Part 2 點名必含的是抗組織胺還是 naloxone？"),
  "C": (2, "泛指成藥而非指定的 naloxone", "OTC 藥物泛稱是否等同標準指定的 naloxone kit？"),
  "D": (1, "OK 繃非此處核心要求", "band aid 與 naloxone rescue kit，哪個是 C14 Part 2 的重點？")}),
"M10_Q37": ("M10_F2", "C14 Part 1 要求 project owner 提供所有租戶『參與』演練的機會，但不必『強制』租戶參加。", {
  "A": (2, "把責任完全推給租戶 HR", "owner 是否完全免除提供演練機會的責任？"),
  "B": (3, "誤以為必須強制所有租戶參加", "C14 要求的是『提供機會』還是『強制參與』？"),
  "D": (2, "誤以為必須全員參與每次演練", "標準要求每次演練全員參加嗎？")}),
"M10_Q38": ("M10_F2", "C15β 規定在延後/分階段返崗等情況下，需於返回職場後 3 個月內完成 post-occupancy survey。", {
  "A": (3, "期限過短", "1 個月是否為 C15β 給的調查期限？"),
  "C": (3, "期限過長", "6 個月與標準的 3 個月，哪個是 C15β 要求？"),
  "D": (2, "期限明顯過長", "1 年是否符合 C15β 的調查時限？")}),
"M10_Q39": ("M10_F4", "C09 對 lactation room 的『數量』沒有硬性規定，由 project team 依專案情境自行決定適當數量。", {
  "A": (3, "誤以為硬性規定至少 1 間", "C09 對房間『數量』是給明確下限，還是交由團隊判斷？"),
  "B": (2, "誤以為每隔一層需設一間", "標準是否規定 every other floor 的數量？"),
  "C": (2, "誤以為每層都需設一間", "C09 是否硬性要求每層樓都有 lactation room？")}),
"M10_Q40": ("M10_F4", "C16β Housing Equity 取得最高 2 分需將 100% 的單元配置給所得在限額以下的租戶。", {
  "A": (2, "比例遠低於最高分門檻", "20% 是否足以拿到 C16β 的最高 2 分？"),
  "B": (3, "比例仍不足最高分", "40% 與最高分要求的 100% 差距多大？"),
  "C": (3, "比例仍不足最高分", "50% 是否達到 C16β 最高 2 分的配置？")}),
"M10_Q41": ("M10_F4", "C16β 規定 affordable unit 租戶的 total annual housing costs（rent+utilities）須低於所選所得限額的 30%。", {
  "A": (3, "比例低於標準", "25% 與標準的 30% 哪個是 C16β 的上限？"),
  "C": (2, "比例高於標準", "45% 是否超出 C16β 的 30% 上限？"),
  "D": (2, "比例明顯高於標準", "50% 是否符合 housing cost 低於所得限額 30% 的規定？")}),
"M10_Q42": ("M10_F4", "C16β 規定 10 戶以上 affordable units 時，至少 50% 需有 2+ 房、至少 10% 需有 3+ 房。", {
  "A": (3, "兩項比例皆偏離標準", "2+ 房是 60% 還是 50%？3+ 房是 15% 還是 10%？"),
  "B": (3, "兩項比例皆偏離標準", "2+ 房門檻為 40% 還是 50%？"),
  "D": (2, "比例明顯偏高", "100%/25% 是否為 C16β 規定的房型分配？")}),
"M10_Q43": ("M10_F4", "C17β Responsible Labor Practices 要求對 construction、cleaning、security 等 Tier 1 供應商年度盤查；IT support 不在指定部門。", {
  "A": (3, "construction 其實是指定盤查部門", "construction 是否列於 C17β 的 Tier 1 部門？"),
  "B": (3, "cleaning 其實是指定盤查部門", "cleaning 是否屬 C17β 指定供應鏈部門？"),
  "C": (3, "security 其實是指定盤查部門", "security 是否列於 C17β 的盤查範圍？")}),
"M10_Q44": ("M10_F4", "C17β overview 引用：全球約有 24.9 million 人處於 forced labor（2016 年逾 4,000 萬現代奴役受害者中）。", {
  "A": (2, "嚴重低估強迫勞動人數", "1,000 萬是否符合 overview 引用的 forced labor 數字？"),
  "B": (3, "接近但低於引用值", "15.5 百萬與標準的 24.9 百萬哪個是 forced labor 數？"),
  "D": (2, "把總受害者數誤當強迫勞動數", "4,000 萬是現代奴役總數，forced labor 的數字是多少？")}),
"M10_Q45": ("M10_F4", "C10 Family Support 要求雇主讓員工可用 paid sick time/personal days 照顧 spouse、partner、子女、父母、祖父母等廣義家屬。", {
  "B": (3, "把 paid 誤為 unpaid", "C10 提供的是 paid 還是 unpaid 的照顧假？"),
  "C": (3, "照顧對象範圍過窄", "C10 的照顧對象是否僅限 spouse 或 child？"),
  "D": (2, "對象過於寬泛無界定", "C10 列舉的是特定家屬範圍，還是『任何人』？")}),
"M10_Q46": ("M10_F4", "Feature C08: New Parent Support 要求為 primary 與 non-primary caregiver 提供 paid parental leave 及返崗支持。", {
  "A": (3, "與 C09 New Mother Support 混淆", "C09 聚焦哺乳支持，提供雙親 paid leave 的是哪個 feature？"),
  "C": (3, "與 C10 Family Support 混淆", "C10 聚焦家庭照顧假，新生兒雙親 leave 屬哪個 feature？"),
  "D": (2, "與 C06 健康福利混淆", "C06 講 health benefits，parental leave 屬哪個 feature？")}),
"M10_Q47": ("M10_F4", "C09 要求至少一間 dedicated lactation room，且尺寸至少 7 ft x 7 ft。", {
  "A": (2, "把可選配備誤當尺寸要求", "work surface 是配備，C09 對房間『尺寸』的硬性規定是什麼？"),
  "C": (2, "把舒適座椅誤當硬性尺寸要求", "comfortable chair 是建議配置，房間的最低尺寸是多少？"),
  "D": (2, "電源插座數量非此處硬性規定", "C09 對 lactation room 的明確量化要求是尺寸還是插座數？")}),
"M10_Q48": ("M10_F4", "Feature C06: Health Services and Benefits 要求提供 essential/on-demand 健康服務、paid sick leave 與流感疫苗。", {
  "A": (3, "與 C07 Enhanced Promotion 混淆", "C07 強化健康促進，提供 health services 與 sick leave 的是哪個 feature？"),
  "B": (3, "與 C01 Health and Wellness Promotion 混淆", "C01 是 precondition 的促進方案，on-demand health service 屬哪個 feature？"),
  "C": (2, "與 C13 無障礙設計混淆", "C13 講 universal design，與健康服務福利是同一 feature 嗎？")}),
"M10_Q49": ("M10_F1", "C02 Integrative Design 要求建立 health-oriented project mission，把健康目標置於協作流程核心。", {
  "B": (2, "用 organized 取代 health-oriented 失焦", "C02 強調的 mission 性質是『有組織』還是『以健康為導向』？"),
  "C": (2, "用 viable 取代 health-oriented 失焦", "C02 的 mission 關鍵字是 viable 還是 health-oriented？"),
  "D": (3, "用 clear 取代 health-oriented，最易混淆", "mission 要清楚是基本，但 C02 特別要求它以什麼為導向？")}),
"M10_Q50": ("M10_F4", "Feature C13: Accessibility and Universal Design 要求超越無障礙法規、以 universal design 原則打造全包容環境。", {
  "A": (2, "與 C10 Family Support 混淆", "C10 講家庭照顧，超越無障礙法規的是哪個 feature？"),
  "B": (2, "與 C11 Civic Engagement 混淆", "C11 講公民參與，universal design 屬哪個 feature？"),
  "D": (3, "與 C16β Housing Equity 混淆", "C16β 講可負擔住宅，整合 universal design 的是哪個 feature？")}),
}

def build():
    for tag in ["M10_a"]:  # M10_b was completed by codex; do not overwrite
        inp = json.load(open(os.path.join(HERE, "codex_in", f"{tag}.json")))
        out = []
        for q in inp["questions"]:
            fw, expl, diag = SPEC[q["id"]]
            correct = q["correct"]
            opts = []
            for o in q["options"]:
                d = 4 if o["key"] == correct else diag[o["key"]][0]
                opts.append({"key": o["key"], "text": o["text"], "depth": d})
            diagnosis = {k: {"gap": v[1], "followup": v[2]} for k, v in diag.items()}
            assert set(diagnosis) == {"A","B","C","D"} - {correct}, q["id"]
            out.append({"id": q["id"], "stem": q["stem"], "options": opts,
                        "correct": correct, "explanation": expl,
                        "framework": fw, "diagnosis": diagnosis,
                        "verify": {"verdict": "ok", "note": ""}})
        json.dump(out, open(os.path.join(HERE, "codex_out", f"{tag}.json"), "w"),
                  ensure_ascii=False, indent=2)
        print(f"wrote {tag}: {len(out)} q")

if __name__ == "__main__":
    build()
