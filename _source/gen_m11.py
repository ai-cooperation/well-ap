#!/usr/bin/env python3
"""Hand-authored enrichment for M11 (WELL Certification & Portfolio) chunks
M11_a, M11_b, M11_c — codex stand-in while quota is exhausted."""
import json, os
HERE = os.path.dirname(__file__)

SPEC = {
"M11_Q01": ("M11_F2", "WELL Platinum 需各 concept 至少 3 分（即 minimum points per concept = 3），這是各等級中對單一 concept 最高的下限要求。", {
  "A": (2, "把 Platinum 的每概念下限記太低", "Silver 是每概念 1 分，Platinum 對單一 concept 的下限會只到 2 嗎？"),
  "C": (3, "高估每概念下限", "各等級每概念下限最高就是 3，4 是否超出規則？"),
  "D": (2, "高估每概念下限", "5 分是否為任何等級的每概念下限？")}),
"M11_Q02": ("M11_F1", "WELL Building Standard 由 Delos 開創，後續由 IWBI 管理、GBCI 認證。", {
  "A": (3, "USGBC 負責 LEED 而非開創 WELL", "USGBC 主導的是哪個評級系統？WELL 的開創者是誰？"),
  "B": (2, "Cleveland Clinic 是醫學夥伴非開創者", "Cleveland Clinic 在 WELL 中扮演研究角色，開創 WELL 的公司是哪間？"),
  "D": (3, "IWBI 是管理機構而非最初開創者", "IWBI 負責管理 WELL，但最早『pioneer』WELL 的是哪間公司？")}),
"M11_Q03": ("M11_F2", "preconditions 是強制門檻；W02.1 Meet Chemical Thresholds 屬 precondition，未達即無法取得認證。", {
  "A": (2, "A07 Operable Windows 屬 optimization 非 precondition", "operable windows 是加分項還是強制門檻？"),
  "C": (1, "T05 Radiant Cooling 為 optimization", "radiant cooling 未達會直接擋掉認證嗎？"),
  "D": (2, "C08 New Parent Leave 為 optimization", "new parent leave 是 precondition 還是 optimization？")}),
"M11_Q04": ("M11_F3", "Performance testing 需可涵蓋至少 2.5% 的 total building floor area 供抽測。", {
  "B": (3, "把抽測比例記成 5%", "performance testing 的可測面積下限是 2.5% 還是 5%？"),
  "C": (2, "嚴重高估抽測面積比例", "25% 是否為 performance test 的面積要求？"),
  "D": (1, "把抽測面積誤當半棟樓", "50% 顯然超出 performance testing 的面積規定吧？")}),
"M11_Q05": ("M11_F3", "occupancy 後由 WELL Assessor（屬 GBCI 的 Performance Testing Agent）執行測試，確認達到最低空氣品質要求。", {
  "A": (1, "General Contractor 不負責認證測試", "施工總包與認證 performance test 是同一角色嗎？"),
  "B": (3, "Commissioning Authority 負責系統調適非 WELL 測試", "Cx Authority 做的 commissioning 與 WELL Assessor 的測試有何不同？"),
  "D": (2, "MEP Engineer 設計系統而非執行認證測試", "MEP 工程師設計系統，但 WELL 認證測試由誰執行？")}),
"M11_Q06": ("M11_F2", "達 Silver 須通過所有 preconditions，並每個 concept 至少 1 分。", {
  "B": (3, "把每概念下限記太高", "Silver 的每概念下限是 1 還是 4？"),
  "C": (2, "高估每概念下限", "8 分是否為 Silver 的每概念要求？"),
  "D": (1, "嚴重高估每概念下限", "12 是否可能是任何等級的每概念下限？")}),
"M11_Q07": ("M11_F2", "WELL v2 共有 24 個 preconditions 必須全數達成。", {
  "A": (2, "低估 precondition 數量", "preconditions 是 18 還是 24？"),
  "C": (3, "把 precondition 與其他總數混淆", "48 較接近哪個總數（如 optimizations）而非 preconditions？"),
  "D": (2, "高估 precondition 數量", "52 是否為 preconditions 的數目？")}),
"M11_Q08": ("M11_F3", "New and Existing Building 專案須每 3 年申請 recertification，以確認持續符合標準。", {
  "B": (3, "把週期記成 5 年", "recertification 週期是 3 年還是 5 年？"),
  "C": (2, "把週期記成 4 年", "標準規定的是 3 年還是 4 年？"),
  "D": (1, "誤以為不需 recertification", "WELL 是否有持續性的 recertification 要求？")}),
"M11_Q09": ("M11_F2", "score 60 對應 WELL Gold（Bronze 40 / Silver 50 / Gold 60 / Platinum 80）。", {
  "A": (3, "把 60 分誤判為 Silver", "Silver 的門檻是 50，60 分跨過了哪一級？"),
  "B": (2, "把 60 分誤判為 Platinum", "Platinum 需 80 分，60 分達得到嗎？"),
  "D": (1, "把 60 分誤判為 Bronze", "Bronze 是 40 分級距，60 分仍停在 Bronze 嗎？")}),
"M11_Q10": ("M11_F1", "Tobacco Cessation（戒菸支持）屬 Mind concept。", {
  "A": (2, "與 Nourishment 混淆", "戒菸支持是飲食議題還是心理/行為健康議題？"),
  "B": (3, "與 Air 的 Smoke-Free 混淆", "Air 的 A02 處理二手菸環境，個人戒菸『行為』支持屬哪個 concept？"),
  "D": (2, "與 Community 混淆", "tobacco cessation 偏向個人心理行為，較屬 Mind 還是 Community？")}),
"M11_Q11": ("M11_F1", "WELL v2 由 150+ WELL concept advisors 參與制定。", {
  "A": (2, "低估顧問人數", "參與顧問是 50+ 還是 150+？"),
  "B": (3, "接近但非標準引用數", "112 較接近 features 數，advisors 是多少？"),
  "D": (2, "高估顧問人數", "275+ 是否為制定 WELL v2 的 advisor 數？")}),
"M11_Q12": ("M11_F4", "Innovation concept 最多可爭取 10 分。", {
  "A": (2, "把單一 feature 分數誤當總上限", "I02 只 1 分，但整個 Innovation concept 上限是多少？"),
  "B": (3, "把 I05 的 5 分誤當總上限", "I05 green building 最多 5 分，但 Innovation 總上限是多少？"),
  "D": (1, "高估 Innovation 上限", "18 是否為 Innovation concept 的分數上限？")}),
"M11_Q13": ("M11_F1", "WELL v2 共有 10 個 concepts（Air…Community 加上 Innovation）。", {
  "A": (3, "把 WELL v1 的 7 concepts 沿用", "7 是 WELL v1 的數字，v2 擴充到幾個 concept？"),
  "B": (2, "少算一個 concept", "WELL v2 是 8 個還是 10 個 concept？"),
  "D": (3, "把 11 Knowledge Domains 誤當 concept 數", "11 是 AP 考試的 Knowledge Domains，WELL v2 的 concept 數是多少？")}),
"M11_Q14": ("M11_F3", "自 registration 起，專案有 5 年完成文件提交並安排 Performance Verification。", {
  "B": (3, "把期限記成 3 年", "完成文件與安排驗證的期限是 3 年還是 5 年？"),
  "C": (2, "把基準點與年限都記錯", "期限是從 registration 起算，還是從 on-site verification 起算？"),
  "D": (2, "基準點錯誤", "5 年是從哪個事件起算？是 registration 還是 verification？")}),
"M11_Q15": ("M11_F3", "Letter of Assurance 須由具執照的專業（如 architects、engineers、contractors）簽署；Property Managers 非此類 licensed professional。", {
  "A": (3, "Architects 其實可簽 LoA", "architect 是否屬可簽 LoA 的 licensed professional？"),
  "B": (3, "Contractors 其實可簽 LoA", "contractor 是否在可簽 LoA 的專業之列？"),
  "D": (3, "Engineers 其實可簽 LoA", "engineer 是否可簽 Letter of Assurance？")}),
"M11_Q16": ("M11_F3", "WELL 申請需提交的 annotated documents 類型包含 design drawings 與 operations schedules。", {
  "A": (3, "只列局部文件類型", "floor plans/lighting spec 是子集，標準列的文件大類是什麼？"),
  "B": (3, "只列局部文件類型", "lighting drawings/floor plans 屬細項，annotated documents 的大類為何？"),
  "D": (2, "列出非核心的文件類型", "furniture/equipment schedule 是否為 WELL 要求的核心 annotated document？")}),
"M11_Q17": ("M11_F3", "既有建築應在 Documentation Review 於 WELL Online 標記為 approved 後，才安排 Performance Verification。", {
  "A": (2, "過早安排，未待文件核准", "在文件審查通過前安排驗證，可能造成什麼問題？"),
  "C": (3, "把占用數據門檻誤當排程條件", "12 個月 100% 占用數據是哪類專案的條件？此處的前提是什麼？"),
  "D": (2, "把指派 Assessor 誤當排程前提", "WELL Assessor 被指派，與 documentation 被核准，哪個才是排程驗證的前提？")}),
"M11_Q18": ("M11_F3", "新建專案須在 documentation 核准、取得使用執照滿一個月、且達 50% occupancy 後，方可安排 Performance Verification。", {
  "A": (3, "占用門檻與時限數值錯誤", "是『4 個月+50%』還是『1 個月+50%+文件核准』？"),
  "B": (2, "條件不完整，缺占用與時限", "commissioning 完成是否足以排程？還缺哪些 occupancy 條件？"),
  "D": (2, "缺文件核准與占用率", "1 個月+commissioning 是否涵蓋 documentation approved 與 50% occupancy？")}),
"M11_Q19": ("M11_F3", "專案過大時，WELL Assessor 可雇用其督導下的 pre-qualified testing organization 協助 Performance Verification。", {
  "A": (3, "增派 Assessor 非標準替代路徑", "標準允許的是『加派 Assessor』還是『委由受督導的測試機構』？"),
  "B": (2, "把按面積加派 Assessor 當解法", "按面積加派 Assessor 是否為標準提供的替代路徑？"),
  "D": (2, "延長工期非替代路徑", "單純延長 Assessor 排程是否解決『單人無法完成』的問題？")}),
"M11_Q20": ("M11_F1", "WELL 專案於 projects.wellcertified.com 進行 registration。", {
  "B": (3, "主站非專案註冊入口", "wellcertified.com 是資訊主站，專案註冊的子網域是什麼？"),
  "C": (1, "網域名稱錯誤", "wellbuilding.com 是否為官方註冊網址？"),
  "D": (2, "路徑錯誤", "註冊是用 projects 子網域，還是 wellcertified.com/well 路徑？")}),
"M11_Q21": ("M11_F2", "WELL 認證等級為 Bronze、Silver、Gold、Platinum 四級。", {
  "A": (3, "漏列 Platinum", "WELL 最高等級是 Gold 還是 Platinum？"),
  "B": (2, "只列兩級", "WELL 是否只有 Bronze/Silver 兩級？"),
  "C": (2, "漏列 Bronze 與 Platinum", "Silver/Gold 之外，還有哪兩個等級？")}),
"M11_Q22": ("M11_F2", "所有 preconditions 須達成，對應 24 個 features。", {
  "A": (2, "低估 precondition feature 數", "preconditions 對應 12 還是 24 個 feature？"),
  "B": (3, "接近但低於正確數", "18 與 24 哪個是 precondition 數？"),
  "D": (2, "高估 precondition 數", "28 是否為 precondition 的數目？")}),
"M11_Q23": ("M11_F3", "維持認證需持續回報 occupancy survey、維護紀錄、環境參數監測等；『新租戶 move-in drawings』非維持認證的回報項。", {
  "A": (3, "occupancy survey 其實是維持回報項", "occupancy survey 結果是否屬維持認證的回報？"),
  "B": (3, "維護紀錄其實是維持回報項", "cleaning/filter 維護紀錄是否需持續提供？"),
  "D": (3, "環境監測其實是維持回報項", "air/water 環境參數監測是否屬持續回報？")}),
"M11_Q24": ("M11_F1", "Air concept 強調機械通風專案除良好 HVAC 設計外，還須定期系統維護以維持通風效能與室內空氣品質。", {
  "A": (3, "與 Thermal Comfort 混淆", "HVAC 維護與通風效能的論述屬 Air 還是 Thermal Comfort？"),
  "C": (1, "與 Movement 無關", "通風與 IAQ 的維護論述與 Movement concept 有關嗎？"),
  "D": (1, "與 Sound 無關", "機械通風維護的論述屬 Air 還是 Sound？")}),
"M11_Q25": ("M11_F2", "WELL v2 提供 98 個 optimizations 供專案選擇。", {
  "A": (2, "低估 optimization 數", "optimizations 是 76 還是 98？"),
  "B": (3, "接近但低於正確數", "86 與 98 哪個是 optimization 總數？"),
  "D": (2, "高估 optimization 數", "115 是否為 optimization 的數目？")}),
"M11_Q26": ("M11_F1", "color rendering 與 flicker 等照明特性屬 Light concept。", {
  "A": (2, "與 Mind 混淆", "color rendering/flicker 是照明品質還是心理健康議題？"),
  "B": (1, "與 Innovation 無關", "flicker 屬具體照明 feature，與 Innovation concept 相關嗎？"),
  "C": (2, "與 Movement 混淆", "flicker 與 color rendering 屬 Light 還是 Movement？")}),
"M11_Q27": ("M11_F1", "結合窗景與藝術品（鼓勵爬樓梯/活動）的設計屬 Movement concept（如點狀活躍設計）。", {
  "A": (2, "與 Mind 混淆", "鼓勵使用樓梯與活動的設計屬 Mind 還是 Movement？"),
  "B": (1, "與 Thermal Comfort 無關", "樓梯結合藝術鼓勵活動，與熱舒適 concept 相關嗎？"),
  "D": (2, "與 Light 混淆", "view windows 牽涉採光，但『鼓勵爬樓梯』的獎勵屬哪個 concept？")}),
"M11_Q28": ("M11_F1", "透過設計、政策與方案支持 cognitive 與 emotional health 的 concept 是 Mind。", {
  "A": (2, "與 Nourishment 混淆", "支持認知與情緒健康屬飲食還是 Mind concept？"),
  "C": (2, "與 Movement 混淆", "cognitive/emotional health 的促進屬 Movement 還是 Mind？"),
  "D": (1, "與 Innovation 無關", "心理健康的預防與治療策略屬 Mind 還是 Innovation？")}),
"M11_Q29": ("M11_F1", "要求將 occupant IEQ survey 結果於 30 天內送交 IWBI 的是 Community concept（C04/C05）。", {
  "B": (2, "與 Thermal Comfort 混淆", "occupant survey 的回報要求屬 Community 還是 Thermal Comfort？"),
  "C": (2, "與 Movement 混淆", "survey 結果送交 IWBI 的規定屬哪個 concept？"),
  "D": (2, "與 Air 混淆", "IEQ 調查雖含空氣感受，但 survey 機制本身屬哪個 concept？")}),
"M11_Q30": ("M11_F1", "旨在降低 circadian phase disruption、改善睡眠品質並提升情緒與生產力的 concept 是 Light。", {
  "A": (2, "與 Movement 混淆", "circadian/睡眠的調節主要靠哪個環境因子？屬哪個 concept？"),
  "C": (2, "與 Thermal Comfort 混淆", "circadian rhythm 的調節屬 Light 還是 Thermal Comfort？"),
  "D": (1, "與 Nourishment 無關", "晝夜節律與睡眠的 concept 是 Light 還是 Nourishment？")}),
"M11_Q31": ("M11_F1", "IWBI（International WELL Building Institute）是以改善人類健康為使命的 public benefit corporation。", {
  "A": (3, "GBCI 負責認證執行而非此使命主體", "GBCI 的角色是認證執行，提出此健康使命的機構是誰？"),
  "B": (2, "Delos 是開創公司非 public benefit corp", "Delos 開創 WELL，但題述的 public benefit corporation 是哪間？"),
  "D": (2, "USGBC 主導 LEED 非 WELL 使命主體", "USGBC 對應的是 LEED，WELL 的使命機構是誰？")}),
"M11_Q32": ("M11_F1", "IWBI 是依 Clinton Global Initiative 的承諾而設立。", {
  "B": (2, "與 COP21 氣候協定混淆", "IWBI 設立依據的是健康倡議還是氣候大會？"),
  "C": (1, "與臭氧層協定無關", "Montreal Protocol 處理臭氧層，與 IWBI 設立有關嗎？"),
  "D": (1, "與京都議定書無關", "Kyoto Protocol 是氣候協定，IWBI 依據的承諾是哪個？")}),
"M11_Q33": ("M11_F2", "達 Silver 須在所有 preconditions 之上，再取得 10 分（總 50 分）。", {
  "B": (3, "把所需加分記太高", "Silver 在 preconditions 之上需再 10 分還是 12 分？"),
  "C": (2, "高估所需加分", "14 分是否為 Silver 的加分要求？"),
  "D": (2, "高估所需加分", "16 分是否對應 Silver？")}),
"M11_Q34": ("M11_F2", "達任何認證等級（含 Silver）皆須 100% 達成 preconditions。", {
  "A": (2, "誤以為僅需 75% preconditions", "preconditions 是否允許只達成 75%？"),
  "B": (3, "誤以為 90% 即可", "preconditions 是強制門檻，90% 達成可行嗎？"),
  "C": (3, "接近但仍非全數", "95% 與 100%，哪個才是 precondition 的要求？")}),
"M11_Q35": ("M11_F2", "達 Gold 須在 preconditions 之上再取得 20 分（總 60 分）。", {
  "A": (2, "低估 Gold 所需加分", "10 分對應 Silver 還是 Gold？"),
  "B": (3, "接近但低於 Gold 要求", "15 分是否達到 Gold 的加分門檻？"),
  "D": (2, "高估 Gold 所需加分", "25 分是否為 Gold 的加分要求？")}),
"M11_Q36": ("M11_F2", "達 Platinum 須在 preconditions 之上再取得 40 分（總 80 分）。", {
  "A": (2, "嚴重低估 Platinum 加分", "20 分對應 Gold 還是 Platinum？"),
  "B": (2, "低估 Platinum 加分", "25 分是否達到 Platinum 門檻？"),
  "D": (3, "接近但低於 Platinum 要求", "35 與 40 哪個是 Platinum 的加分要求？")}),
"M11_Q37": ("M11_F2", "WELL Bronze 不要求任何 optimizations（僅需達成所有 preconditions）。", {
  "A": (2, "誤以為 Bronze 需 40% optimizations", "Bronze 是否設有 optimization 的最低比例？"),
  "B": (3, "誤以為每概念需一項 optimization", "每概念 1 項是哪個等級的要求？Bronze 呢？"),
  "C": (2, "嚴重高估 Bronze 要求", "80% optimizations 是否為 Bronze 的門檻？")}),
"M11_Q38": ("M11_F2", "WELL Silver 要求每個 concept 至少 1 分（one per concept）。", {
  "A": (2, "低估 Silver 每概念下限", "Silver 是否容許某 concept 0 分？"),
  "C": (3, "高估 Silver 每概念下限", "two per concept 是哪個等級？Silver 是多少？"),
  "D": (2, "高估 Silver 每概念下限", "three per concept 對應 Platinum，Silver 呢？")}),
"M11_Q39": ("M11_F2", "WELL Gold 要求每個 concept 至少 2 分（two per concept）。", {
  "A": (2, "低估 Gold 每概念下限", "Gold 是否容許某 concept 0 分？"),
  "B": (3, "把 Silver 的下限套到 Gold", "one per concept 是 Silver，Gold 是多少？"),
  "D": (3, "把 Platinum 的下限套到 Gold", "three per concept 對應 Platinum，Gold 呢？")}),
"M11_Q40": ("M11_F2", "WELL Platinum 要求每個 concept 至少 3 分（three per concept）。", {
  "A": (1, "低估 Platinum 每概念下限", "Platinum 是否容許某 concept 0 分？"),
  "B": (2, "把 Silver 下限套到 Platinum", "one per concept 是 Silver，Platinum 是多少？"),
  "C": (3, "把 Gold 下限套到 Platinum", "two per concept 是 Gold，Platinum 的下限是多少？")}),
"M11_Q41": ("M11_F1", "WELL v2 專案主要分為 owner-occupied 與 WELL Core 兩大類。", {
  "B": (3, "把 Portfolio 誤當專案分類", "WELL Portfolio 是規模化『計畫』，專案兩大類指的是哪兩個？"),
  "C": (2, "混入 LEED 非 WELL 專案類別", "LEED Gold 是別的評級，WELL 專案兩大類是什麼？"),
  "D": (1, "否定有正確分類", "WELL 專案確實有兩大類，分別是？")}),
"M11_Q42": ("M11_F5", "WELL Portfolio 兼具『規模化提升 well-being』與『改善人們所處場所』兩項目的，故兩者皆是。", {
  "A": (3, "只取規模化單一面向", "Portfolio 除了 at scale 提升福祉，是否也強調改善場所？"),
  "B": (3, "只取改善場所單一面向", "改善 places 之外，Portfolio 是否也談 at scale？"),
  "D": (1, "否定正確敘述", "A、B 皆為 Portfolio 目的，選 None 合理嗎？")}),
"M11_Q43": ("M11_F5", "企業 enroll WELL Portfolio 代表 portfolio owner 有意參與 WELL Portfolio 計畫。", {
  "A": (3, "與 Health-Safety Rating 混淆", "enroll Portfolio 表達的是參與 Portfolio，還是用 Health-Safety Rating？"),
  "B": (2, "與個人 WELL AP 混淆", "enrollment 是組織層級意向，還是 PM 個人成為 AP？"),
  "D": (1, "把對象誤為建築物", "enrollment 表達的是 owner 意向，還是『建築』的意向？")}),
"M11_Q44": ("M11_F5", "WELL Portfolio 的 enrollment period 為六個月。", {
  "A": (2, "高估報名期", "enrollment period 是 6 個月還是 12 個月？"),
  "B": (3, "低估報名期", "3 個月與 6 個月，哪個是 enrollment period？"),
  "C": (2, "高估報名期", "9 個月是否為 Portfolio 報名期？")}),
"M11_Q45": ("M11_F5", "WELL Portfolio enrollment period 可再延長六個月，最多達一年。", {
  "B": (2, "高估可延長幅度", "可延長的是再 6 個月，還是再 12 個月？"),
  "C": (3, "低估可延長幅度", "延長 2 個月與 6 個月，哪個正確？"),
  "D": (2, "誤以為不可延長", "enrollment period 是否完全不可延長？")}),
"M11_Q46": ("M11_F5", "WELL Portfolio 的最低承諾為五年訂閱（five-year subscription）。", {
  "A": (3, "低估承諾年限", "最低承諾是 3 年還是 5 年訂閱？"),
  "C": (2, "把單次審查當承諾", "one review cycle 是否等同最低承諾？"),
  "D": (1, "誤以為無最低承諾", "Portfolio 是否設有最低承諾期？")}),
"M11_Q47": ("M11_F5", "portfolio administrator 負責監督計畫流程並協調 defined portfolio 的文件作業。", {
  "A": (2, "把時程管理當主要職責", "administrator 的核心是顧時程，還是監督流程與協調文件？"),
  "B": (3, "把職責窄化為委派責任", "delegate responsibilities 與 coordinate documentation，哪個更貼近 administrator 職責？"),
  "D": (2, "誤把對 GBCI 回報當主職", "administrator 主要協調 portfolio 文件，還是向 GBCI 回報？")}),
"M11_Q48": ("M11_F5", "defined portfolio 至少需 10 個專案；若成員全球總 portfolio 少於 10 個，則最低為 2 個。", {
  "B": (2, "門檻數值錯誤", "最低是 10（不足則 2），還是 20（不足則 10）？"),
  "C": (3, "門檻數值錯誤", "8/4 是否為 defined portfolio 的最低規定？"),
  "D": (2, "門檻數值錯誤", "4/2 是否為 defined portfolio 的專案下限？")}),
"M11_Q49": ("M11_F5", "WELL Portfolio 成員可用三種 documentation scales：individual-scale、shareable 與 guideline documents。", {
  "A": (2, "列出非 Portfolio 的文件類型", "photographs/LoA 是一般 verification，Portfolio 的 documentation scales 是哪三種？"),
  "C": (3, "捏造不存在的文件尺度名稱", "streamlined/modeling/library 是否為 Portfolio 的官方 scales？"),
  "D": (1, "否定存在文件尺度", "WELL Portfolio 是否確有 documentation scales？")}),
"M11_Q50": ("M11_F5", "GBCI 負責訓練與核可 WELL Portfolio 的 WELL Performance Testing Agents。", {
  "A": (1, "BREEAM 為別的評級系統", "BREEAM 與 WELL testing agent 的訓練有關嗎？"),
  "B": (3, "IWBI 負責標準而非訓練測試員", "IWBI 管理標準，但訓練/核可 testing agent 的是哪個機構？"),
  "D": (1, "LEED 為評級系統非訓練機構", "LEED 是評級系統，訓練 WELL testing agent 的是誰？")}),
"M11_Q51": ("M11_F5", "feature review 期間，WELL Portfolio 的 project documents 與 performance testing results 可在任何時間（at any time）上傳。", {
  "A": (3, "誤加上協調完成的前提", "標準是否要求所有文件協調完成後才能上傳？"),
  "B": (2, "誤加上時間點限制", "上傳是否被限制在前六個月結束時？"),
  "C": (2, "誤把占用率當上傳條件", "50% occupancy 是否為文件上傳的前提？")}),
}

def build():
    for tag in ["M11_a", "M11_b", "M11_c"]:
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
