const WELLAP_CONTENT = {
  "id": "wellap",
  "name": "WELL AP 健康建築認證專家",
  "brandMark": "WA",
  "description": "以 WELL v2 與 WELL AP 考試藍圖建立健康建築認證的核心概念學習路徑。",
  "hero": {
    "title": "用<em>三個問題</em>，把 WELL<br>從條文變成你的設計直覺。",
    "lede": "核心概念（What / Why / How）→ 爭議（設計取捨辯證）→ 鑑別（高鑑別考題）。不背 WELL v2 條文，而是能上考場、上專案會議的理解。"
  },
  "moduleListIntro": "依 WELL AP 11 個 Knowledge Domains 整理，每個模組都以三問法拆解 WELL v2 核心概念。",
  "levels": [
    {
      "id": "ap",
      "name": "WELL AP",
      "requiresLogin": false,
      "description": "100 題單選，約 2 小時"
    }
  ],
  "apiProxy": "https://api.cooperation.tw",
  "teacherEmail": "alan.chen75@gmail.com",
  "theme": {
    "primary": "#008F7A",
    "primaryLt": "#E4F5F1",
    "navy": "#0B3F35"
  },
  "terminology": {
    "framework": "核心概念",
    "exam": "模擬考",
    "practice": "弱項練習",
    "level1": "基礎概念",
    "level2": "雙概念混合",
    "level3": "實務情境",
    "level4": "陷阱題"
  },
  "questionStyle": {
    "optionLength": [38, 55],
    "diffMax": 8,
    "stemMin": 60
  },
  "examInfo": {
    "name": "WELL AP",
    "duration": "約 120 分鐘",
    "questions": 100,
    "passScore": 170,
    "trends": [
      "11 個 Knowledge Domains 對應 WELL v2 Concepts 與 certification process，配重最高的是 WELL Certification and WELL Portfolio 12 題與 Air 11 題。",
      "題型涵蓋 Recall Questions、Application Questions 與 Analysis Questions，會要求把 WELL feature 原則套入新情境。",
      "考試會測試 Performance Verification、documentation、AAP/equivalencies、precertification、recertification 與 point thresholds。",
      "WELL AP 必須能解讀現場監測與 laboratory testing 結果，並提出 corrective actions。",
      "考試參考 WELL Building Standard v2 with Q4 2020 addenda、WELL Certification Guidebook 與 WELL Portfolio Guidebook。"
    ]
  },
  "modules": [
    {
      "id": "M01",
      "name": "空氣 Air",
      "level": "ap",
      "frameworks": [
        {
          "id": "M01_F1",
          "name": "室內空氣品質門檻",
          "desc": "掌握 indoor air contaminants 的來源、健康影響與 A01 Air Quality 的 performance threshold，例如 PM2.5: 15 µg/m³ or lower、PM10: 50 µg/m³ or lower。",
          "analogy": "像先確認飲用水是否乾淨，空氣策略也要先用可量測指標定義基本安全線。",
          "covers": ["A01 Air Quality", "PM2.5: 15 µg/m³ or lower", "PM10: 50 µg/m³ or lower", "VOCs", "carbon monoxide"]
        },
        {
          "id": "M01_F2",
          "name": "通風稀釋與新風設計",
          "desc": "理解 A03 Ventilation Design 與 A06 Enhanced Ventilation Design 如何用 mechanical ventilation、natural ventilation 與 ASHRAE 62.1 稀釋人員與產品產生的污染物。",
          "covers": ["A03 Ventilation Design", "A06 Enhanced Ventilation Design", "mechanical ventilation", "natural ventilation", "ASHRAE 62.1-2010"]
        },
        {
          "id": "M01_F3",
          "name": "污染源控制與隔離",
          "desc": "把 A02 Smoke-Free Environment、A04 Construction Pollution Management、A10 Combustion Minimization 與 A11 Source Separation 視為源頭移除、施工期管理與高污染空間隔離的組合。",
          "covers": ["A02 Smoke-Free Environment", "A04 Construction Pollution Management", "A10 Combustion Minimization", "A11 Source Separation", "secondhand smoke"]
        },
        {
          "id": "M01_F4",
          "name": "監測過濾與微生物風險",
          "desc": "A08 Air Quality Monitoring and Awareness、A12 Air Filtration、A13 Enhanced Supply Air 與 A14 Microbe and Mold Control 要把監測、過濾、non-recirculated or treated supply air、UVGI 與 mold control 串成運維閉環。",
          "covers": ["A08 Air Quality Monitoring and Awareness", "A12 Air Filtration", "A13 Enhanced Supply Air", "A14 Microbe and Mold Control", "UVGI"]
        }
      ],
      "debates": [
        {
          "id": "M01_D1",
          "title": "自然通風 vs 機械通風",
          "scenario": "一棟辦公樓希望提高新風量並增加可開窗體驗，但基地外部 PM2.5 與交通污染偏高，設計團隊要在 A07 Operable Windows 與 A03/A06 通風策略之間取捨。",
          "sideA": {
            "label": "優先自然通風與可開窗",
            "args": ["可增加 occupant control、連結戶外環境，並在合適天氣下提高新鮮空氣供應。", "對低污染、溫和氣候基地，可降低對機械系統的完全依賴。"]
          },
          "sideB": {
            "label": "優先機械通風與過濾",
            "args": ["當 outdoor PM2.5 或交通污染偏高，機械通風可搭配 filtration 與 monitoring 控制進氣品質。", "ASHRAE 62.1 路徑與性能測試較容易形成可驗證的合規證據。"]
          },
          "insight": "WELL 的取捨不是自然或機械二選一，而是根據 outdoor air quality、thermal comfort 與可驗證資料決定何時開放、何時過濾、何時限制。",
          "framework": "M01_F2"
        },
        {
          "id": "M01_D2",
          "title": "施工期污染管理 vs 趕工成本",
          "scenario": "租戶趕著入住，承包商想縮短 flush-out、材料保護與污染隔離流程，但 A04 Construction Pollution Management 要求降低施工污染導入室內的風險。",
          "sideA": {
            "label": "壓縮施工期管理",
            "args": ["可降低工期延誤與臨時設備成本。", "若後續再做清潔與測試，短期看似不影響交付。"]
          },
          "sideB": {
            "label": "維持施工污染控制",
            "args": ["PM10、VOCs 與濕氣污染一旦進入材料或風管，後續 remediation 成本可能更高。", "A04 的重點是生命週期前段預防，而不只是交屋前補救。"]
          },
          "insight": "施工期策略是 IAQ 的前置保險；越晚處理，越容易把可控風險變成性能驗證失敗與入住後抱怨。",
          "framework": "M01_F3"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M02",
      "name": "水 Water",
      "level": "ap",
      "frameworks": [
        {
          "id": "M02_F1",
          "name": "飲用水與接觸水指標",
          "desc": "W01 Water Quality Indicators 與 W02 Drinking Water Quality 分別處理 turbidity、coliforms 與 chemical composition 等水質門檻，W01 要求 Turbidity is less than or equal to 1.0 NTU, FTU or FNU。",
          "covers": ["W01 Water Quality Indicators", "W02 Drinking Water Quality", "Turbidity <= 1.0 NTU", "coliforms", "chemical composition"]
        },
        {
          "id": "M02_F2",
          "name": "Legionella 與水安全管理",
          "desc": "W03 Basic Water Management 要透過 testing、monitoring 與 Legionella management plan 降低水質劣化與 Legionella colonization 風險。",
          "covers": ["W03 Basic Water Management", "Legionella management plan", "recirculating hot water systems", "water safety and management plans"]
        },
        {
          "id": "M02_F3",
          "name": "飲水可近性與補水行為",
          "desc": "W04 Enhanced Water Quality、W05 Drinking Water Quality Management 與 W06 Drinking Water Promotion 將 treatment、display、dispensers 與 hydration promotion 連成從水質到行為的策略。",
          "analogy": "水質合格像是食材新鮮，飲水機位置與維護才決定大家會不會真的喝。",
          "covers": ["W04 Enhanced Water Quality", "W05 Drinking Water Quality Management", "W06 Drinking Water Promotion", "drinking water dispensers", "hydration"]
        },
        {
          "id": "M02_F4",
          "name": "濕氣管理與衛生支援",
          "desc": "W07 Moisture Management 與 W08 Hygiene Support 對應 moisture infiltration、condensation、bathrooms、hand washing stations 與 hygiene amenities。",
          "covers": ["W07 Moisture Management", "W08 Hygiene Support", "moisture management", "bathroom accommodations", "hand washing stations"]
        }
      ],
      "debates": [
        {
          "id": "M02_D1",
          "title": "一次性水質改善 vs 持續監測",
          "scenario": "專案前測發現部分水質參數接近 W02 threshold，業主傾向裝設 treatment 後只在 Performance Verification 前再測一次。",
          "sideA": {
            "label": "一次改善後驗證",
            "args": ["資本支出明確，對短期認證排程較容易管理。", "若污染源固定，處理設備可能足以把參數壓回門檻內。"]
          },
          "sideB": {
            "label": "建立持續監測與管理",
            "args": ["水質會受停滯、管線、溫度與運維影響，W03/W05 強調 protocols 與 ongoing management。", "接近門檻的參數需要 corrective actions 與文件化紀錄。"]
          },
          "insight": "WELL 的水策略不只看測試通過，而是能否證明水質風險被持續辨識、處理與回報。",
          "framework": "M02_F2"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M03",
      "name": "飲食 Nourishment",
      "level": "ap",
      "frameworks": [
        {
          "id": "M03_F1",
          "name": "健康食物可得性",
          "desc": "N01 Fruits and Vegetables 與 N13 Local Food Environment 關注健康食物、在地新鮮蔬果與環境可近性；考試會要求把 food access 與健康結果連結。",
          "covers": ["N01 Fruits and Vegetables", "N13 Local Food Environment", "healthy food access", "fruits and vegetables"]
        },
        {
          "id": "M03_F2",
          "name": "營養透明與食物素養",
          "desc": "N02 Nutritional Transparency 與 N07 Nutrition Education 要用 nutritional labeling、allergy information、calorie labeling 與 food literacy 幫助使用者做 informed food choices。",
          "covers": ["N02 Nutritional Transparency", "N07 Nutrition Education", "nutritional labeling", "allergy information", "food literacy"]
        },
        {
          "id": "M03_F3",
          "name": "避免過度攝取與不良成分",
          "desc": "N03 Refined Ingredients、N05 Artificial Ingredients 與 N06 Portion Sizes 分別處理 sugar/refined grains、artificial colors/flavors/sweeteners/preservatives 與 portion size。",
          "covers": ["N03 Refined Ingredients", "N05 Artificial Ingredients", "N06 Portion Sizes", "refined grains", "artificial ingredients"]
        },
        {
          "id": "M03_F4",
          "name": "飲食包容與負責任採購",
          "desc": "N09 Special Diets、N10 Food Preparation、N11 Responsible Food Sourcing 與 N12 Food Production 涵蓋 diverse dietary needs、meal preparation、certified organic、certified sustainable foods 與 on-site food production。",
          "covers": ["N09 Special Diets", "N10 Food Preparation", "N11 Responsible Food Sourcing", "N12 Food Production", "certified organic and certified sustainable foods"]
        }
      ],
      "debates": [
        {
          "id": "M03_D1",
          "title": "標示資訊 vs 選擇架構",
          "scenario": "員工餐廳已提供 calorie labeling 與 allergen labeling，但健康餐點仍很少被選，營運團隊考慮把健康選項放在動線前段並限制不健康廣告。",
          "sideA": {
            "label": "強化標示即可",
            "args": ["N02/N07 可提升 informed choice 與 food literacy。", "保留選擇自由，較不容易引發員工反感。"]
          },
          "sideB": {
            "label": "改變陳列與廣告",
            "args": ["N04 Food Advertising 與 N08 Mindful Eating 關注 design、messaging 與 eating environment。", "真實行為常受預設位置、視覺提示與環境干擾影響。"]
          },
          "insight": "營養資訊是必要但不充分；WELL Nourishment 把知識、可近性、份量與環境提示視為同一套行為設計。",
          "framework": "M03_F2"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M04",
      "name": "光 Light",
      "level": "ap",
      "frameworks": [
        {
          "id": "M04_F1",
          "name": "日夜節律與光曝露",
          "desc": "L01 Light Exposure 與 L03 Circadian Lighting Design 對應 circadian photoentrainment、daylight、electric light 與 Equivalent Melanopic Lux，目標是降低 circadian phase disruption。",
          "covers": ["L01 Light Exposure", "L03 Circadian Lighting Design", "circadian photoentrainment", "Equivalent Melanopic Lux", "M-EDI(D65)"]
        },
        {
          "id": "M04_F2",
          "name": "視覺照明與工作面需求",
          "desc": "L02 Visual Lighting Design 要依 space types、activities 與 work planes 提供適當 illuminance，支援 visual comfort 與 visual acuity。",
          "covers": ["L02 Visual Lighting Design", "illuminance", "work planes", "visual acuity", "lighting guidelines"]
        },
        {
          "id": "M04_F3",
          "name": "眩光、平衡與電光品質",
          "desc": "L04 Electric Light Glare Control、L07 Visual Balance 與 L08 Electric Light Quality 關注 glare、visual balance、color rendering 與 flicker。",
          "covers": ["L04 Electric Light Glare Control", "L07 Visual Balance", "L08 Electric Light Quality", "color rendering", "flicker"]
        },
        {
          "id": "M04_F4",
          "name": "日光設計與模擬決策",
          "desc": "L05 Daylight Design Strategies、L06 Daylight Simulation 與 L09 Occupant Lighting Control 要把 daylight access、simulation reports、outdoor views 與 occupant preferences 納入設計判斷。",
          "covers": ["L05 Daylight Design Strategies", "L06 Daylight Simulation", "L09 Occupant Lighting Control", "daylight simulation", "outdoor views"]
        }
      ],
      "debates": [
        {
          "id": "M04_D1",
          "title": "高日光曝露 vs 眩光控制",
          "scenario": "設計團隊希望用大面積玻璃提高 daylight access 與 views，但使用者抱怨下午 glare 影響工作，照明顧問需要同時回應 L05/L06 與 L04。",
          "sideA": {
            "label": "提高日光與視野",
            "args": ["日光與 views 可支援 circadian and psychological health。", "daylight simulation 可展示較高的室內日光覆蓋。"]
          },
          "sideB": {
            "label": "控制眩光與視覺舒適",
            "args": ["眩光會破壞 visual comfort，可能導致使用者長期拉上遮陽而抵消日光效益。", "L04/L07 要求照明環境平衡，而不只是更多光。"]
          },
          "insight": "Light 的核心是適時、適量、可控制；高日光不是目的，能被持續使用且不造成 glare 才是 WELL 專案的設計重點。",
          "framework": "M04_F4"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M05",
      "name": "運動 Movement",
      "level": "ap",
      "frameworks": [
        {
          "id": "M05_F1",
          "name": "主動建築與動線設計",
          "desc": "V01 Active Buildings and Communities、V03 Circulation Network 與 V05 Site Planning and Selection 用 staircase visibility、walkability、site amenities 促進日常 movement。",
          "covers": ["V01 Active Buildings and Communities", "V03 Circulation Network", "V05 Site Planning and Selection", "stair use", "walkability"]
        },
        {
          "id": "M05_F2",
          "name": "人體工學工作站",
          "desc": "V02 Ergonomic Workstation Design 要降低 physical strain，WELL v2 範例提到 V02 Part 1 requires adjustable height workstations for at least 25% of all workstations。",
          "covers": ["V02 Ergonomic Workstation Design", "adjustable height workstations", "at least 25% of all workstations", "neutral posture", "ergonomics"]
        },
        {
          "id": "M05_F3",
          "name": "主動通勤與活動設施",
          "desc": "V04 Facilities for Active Occupants、V08 Physical Activity Spaces and Equipment 與 V06 Physical Activity Opportunities 用 bike storage、showers、activity spaces 與 no-cost activity opportunities 支援 active occupants。",
          "covers": ["V04 Facilities for Active Occupants", "V06 Physical Activity Opportunities", "V08 Physical Activity Spaces and Equipment", "bike storage", "showers"]
        },
        {
          "id": "M05_F4",
          "name": "久坐中斷與行為回饋",
          "desc": "V07 Active Furnishings、V09 Physical Activity Promotion 與 V10 Self-Monitoring 對應 sit-stand furnishings、physical activity incentives 與 wearable technology。",
          "covers": ["V07 Active Furnishings", "V09 Physical Activity Promotion", "V10 Self-Monitoring", "sit-stand workstation", "wearable technology"]
        }
      ],
      "debates": [
        {
          "id": "M05_D1",
          "title": "設備投資 vs 行為方案",
          "scenario": "公司預算有限，只能優先做一類 Movement 策略：採購 active furnishings，或長期推動 activity incentives 與 no-cost programs。",
          "sideA": {
            "label": "先買設備",
            "args": ["V02/V07 的工作站與 active furnishings 可直接改變久坐姿勢與工作環境。", "硬體改善較容易在 documentation 中被盤點。"]
          },
          "sideB": {
            "label": "先做行為方案",
            "args": ["V06/V09 可用活動機會、誘因與監測推動習慣改變。", "沒有文化與使用支持，設備可能閒置。"]
          },
          "insight": "Movement 要同時處理環境可行性與行為維持；硬體降低阻力，政策與方案提高使用率。",
          "framework": "M05_F4"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M06",
      "name": "熱舒適 Thermal Comfort",
      "level": "ap",
      "frameworks": [
        {
          "id": "M06_F1",
          "name": "熱舒適參數與基準",
          "desc": "T01 Thermal Performance 以 mechanically conditioned 與 naturally conditioned spaces 的 thermal comfort 條件為基礎，並引用 ASHRAE 55-2013 等 thermal comfort standards。",
          "covers": ["T01 Thermal Performance", "ASHRAE 55-2013", "adaptive thermal comfort", "air temperature", "mean radiant temperature"]
        },
        {
          "id": "M06_F2",
          "name": "驗證、分區與個人控制",
          "desc": "T02 Verified Thermal Comfort、T03 Thermal Zoning 與 T04 Individual Thermal Control 要用 occupant satisfaction、thermal zoning、personal thermal comfort devices 與 flexible dress codes 提升舒適。",
          "covers": ["T02 Verified Thermal Comfort", "T03 Thermal Zoning", "T04 Individual Thermal Control", "personal thermal comfort devices", "flexible dress codes"]
        },
        {
          "id": "M06_F3",
          "name": "輻射系統與濕度控制",
          "desc": "T05 Radiant Thermal Comfort 與 T07 Humidity Control 關注 radiant systems、independently controlled ventilation、relative humidity、off-gassing 與 pathogen growth。",
          "covers": ["T05 Radiant Thermal Comfort", "T07 Humidity Control", "radiant systems", "relative humidity", "pathogen growth"]
        },
        {
          "id": "M06_F4",
          "name": "熱舒適監測與回饋",
          "desc": "T06 Thermal Comfort Monitoring 要用 sensors 與 displays 持續監測 thermal comfort parameters，讓管理者與使用者能辨識偏差並回應。",
          "covers": ["T06 Thermal Comfort Monitoring", "sensors", "displays", "Performance Verification Guidebook", "thermal comfort parameters"]
        }
      ],
      "debates": [
        {
          "id": "M06_D1",
          "title": "統一設定點 vs 個人控制",
          "scenario": "物業團隊希望用單一空調設定點維持能源效率，但 occupants 對冷熱感差異很大，抱怨集中在靠窗與內區座位。",
          "sideA": {
            "label": "維持統一設定點",
            "args": ["運維簡單，能源模型與設備控制較穩定。", "若符合 T01 基本條件，可先達到多數人可接受的熱環境。"]
          },
          "sideB": {
            "label": "增加分區與個人控制",
            "args": ["T03/T04 承認 thermal preferences 高度個人化。", "熱舒適不只空氣溫度，還受 clothing、metabolism、radiant temperature 與 air speed 影響。"]
          },
          "insight": "Thermal Comfort 的考點常在 interdependencies；合格設定點不是終點，分區、控制與監測才是降低不滿意度的工具。",
          "framework": "M06_F2"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M07",
      "name": "聲音 Sound",
      "level": "ap",
      "frameworks": [
        {
          "id": "M07_F1",
          "name": "聲學分區與聲音地圖",
          "desc": "S01 Sound Mapping 要識別 noise sources、quiet zones、mixed zones 與 acoustic zone labels，作為後續隔音、吸音與背景聲策略的基礎。",
          "covers": ["S01 Sound Mapping", "acoustical plan", "acoustic zone labels", "quiet zones", "mixed zones"]
        },
        {
          "id": "M07_F2",
          "name": "背景噪音與聲音干擾",
          "desc": "S02 Maximum Noise Levels 與 S06 Minimum Background Sound 分別處理 ambient background noise 的上限與 speech privacy 所需的 dedicated artificial sound。",
          "covers": ["S02 Maximum Noise Levels", "S06 Minimum Background Sound", "ambient background noise", "speech privacy", "background sound"]
        },
        {
          "id": "M07_F3",
          "name": "隔音與語音私密",
          "desc": "S03 Sound Barriers 關注 enclosed spaces 之間的 sound isolation 與 speech privacy，牆與門需達到最低 acoustic separation。",
          "covers": ["S03 Sound Barriers", "sound isolation", "speech privacy", "Sound Transmission Class", "STC"]
        },
        {
          "id": "M07_F4",
          "name": "混響與吸音材料",
          "desc": "S04 Reverberation Time 與 S05 Sound Reducing Surfaces 要用 reverberation time thresholds、sound reducing surfaces 與 acoustic materials 支援 speech intelligibility。",
          "covers": ["S04 Reverberation Time", "S05 Sound Reducing Surfaces", "reverberation time thresholds", "speech intelligibility", "acoustic materials"]
        }
      ],
      "debates": [
        {
          "id": "M07_D1",
          "title": "安靜環境 vs 語音私密",
          "scenario": "開放辦公室降低 HVAC 噪音後，背景聲變得很低，員工反而更容易聽到鄰近會議與電話內容。",
          "sideA": {
            "label": "追求最低背景噪音",
            "args": ["過高背景噪音會干擾專注、滿意度與健康。", "S02 要控制 HVAC、外部侵入與其他噪音源。"]
          },
          "sideB": {
            "label": "導入最低背景聲",
            "args": ["S06 認為穩定 background sound 可改善 signal-to-noise ratio 與 speech privacy。", "過低的背景聲會讓語音更容易被理解。"]
          },
          "insight": "Sound 不是越安靜越好；不同 zone 需要不同 acoustic target，安靜、私密與語音清晰度要一起設計。",
          "framework": "M07_F2"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M08",
      "name": "材料 Materials",
      "level": "ap",
      "frameworks": [
        {
          "id": "M08_F1",
          "name": "限制高風險材料",
          "desc": "X01 Material Restrictions 限制 asbestos、mercury、lead 等已知 hazardous ingredients；例如部分產品類別不可含超過 1,000 ppm asbestos，mercury 不超過 0.1% (1000 ppm) by weight。",
          "covers": ["X01 Material Restrictions", "asbestos", "mercury", "lead", "1000 ppm"]
        },
        {
          "id": "M08_F2",
          "name": "既有危害與場址風險管理",
          "desc": "X02 Interior Hazardous Materials Management、X03 CCA and Lead Management 與 X04 Site Remediation 要處理既有建築 asbestos、lead、PCBs、CCA 與 contaminated sites。",
          "covers": ["X02 Interior Hazardous Materials Management", "X03 CCA and Lead Management", "X04 Site Remediation", "PCBs", "CCA"]
        },
        {
          "id": "M08_F3",
          "name": "VOCs 與材料透明",
          "desc": "X05 Enhanced Material Restrictions、X06 VOC Restrictions、X07 Materials Transparency 與 X08 Materials Optimization 把 product documentation、ingredient transparency、emission thresholds 與第三方評估串在一起。",
          "covers": ["X05 Enhanced Material Restrictions", "X06 VOC Restrictions", "X07 Materials Transparency", "X08 Materials Optimization", "VOCs"]
        },
        {
          "id": "M08_F4",
          "name": "廢棄物、害蟲與清潔政策",
          "desc": "X09 Waste Management、X10 Pest Management and Pesticide Use 與 X11 Cleaning Products and Protocols 對應 hazardous waste、IPM、pesticides、cleaning products 與 maintenance practices。",
          "covers": ["X09 Waste Management", "X10 Pest Management and Pesticide Use", "X11 Cleaning Products and Protocols", "integrated pest management", "cleaning protocols"]
        }
      ],
      "debates": [
        {
          "id": "M08_D1",
          "title": "產品透明度 vs 採購彈性",
          "scenario": "室內裝修趕工時，採購團隊想使用交期較短但文件不足的材料，顧問則要求符合 X06/X07/X08 的 product documentation 與 transparency。",
          "sideA": {
            "label": "保留採購彈性",
            "args": ["可降低缺料與延誤風險。", "若材料看似常規產品，短期文件蒐集成本可能超過專案預算。"]
          },
          "sideB": {
            "label": "堅持透明與限制",
            "args": ["Materials 考點重視 hazardous ingredients、VOCs 與供應鏈文件。", "缺文件會讓 compliance assessment 與第三方審查失去依據。"]
          },
          "insight": "材料策略的核心不是只買低毒產品，而是讓產品成分、排放與第三方評估可被查核。",
          "framework": "M08_F3"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M09",
      "name": "心理 Mind",
      "level": "ap",
      "frameworks": [
        {
          "id": "M09_F1",
          "name": "心理健康政策與服務",
          "desc": "M01 Mental Health Promotion、M03 Mental Health Services 與 M04 Mental Health Education 透過 supportive programs、policies、resources、training 與 services 支援 mental well-being。",
          "covers": ["M01 Mental Health Promotion", "M03 Mental Health Services", "M04 Mental Health Education", "mental well-being", "mental health training"]
        },
        {
          "id": "M09_F2",
          "name": "自然、地方感與美感",
          "desc": "M02 Nature and Place 與 M09 Enhanced Access to Nature 要把 natural environment、culture、place、art、beauty 與 access to nature 整合到專案。",
          "covers": ["M02 Nature and Place", "M09 Enhanced Access to Nature", "biophilia", "culture", "place"]
        },
        {
          "id": "M09_F3",
          "name": "壓力管理與恢復",
          "desc": "M05 Stress Management、M06 Restorative Opportunities、M07 Restorative Spaces 與 M08 Restorative Programming 針對 stress sources、restoration、quiet zones 與 restorative programming。",
          "covers": ["M05 Stress Management", "M06 Restorative Opportunities", "M07 Restorative Spaces", "M08 Restorative Programming", "stress management"]
        },
        {
          "id": "M09_F4",
          "name": "成癮與物質使用介入",
          "desc": "M10 Tobacco Cessation 與 M11 Substance Use Services 關注 tobacco cessation、substance abuse and addiction support services、workplace policies 與 access to resources。",
          "covers": ["M10 Tobacco Cessation", "M11 Substance Use Services", "tobacco cessation", "substance use services", "addiction support"]
        }
      ],
      "debates": [
        {
          "id": "M09_D1",
          "title": "空間療癒 vs 組織政策",
          "scenario": "企業想用植栽、藝術牆與安靜室改善心理健康，但員工調查顯示壓力主因來自工作負荷與缺乏服務資源。",
          "sideA": {
            "label": "先改善空間",
            "args": ["M02/M07 可透過 nature、place 與 restorative spaces 降低 mental fatigue。", "空間改善可見度高，容易讓 occupants 感受到改變。"]
          },
          "sideB": {
            "label": "先補政策與服務",
            "args": ["M01/M03/M05 要求 programs、policies、resources 與 stress management plan。", "若壓力源來自制度，單靠美化空間無法處理根因。"]
          },
          "insight": "Mind 的實務答案通常是空間與政策並行；自然與恢復空間提供緩衝，心理健康服務與壓力計畫處理根因。",
          "framework": "M09_F3"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M10",
      "name": "社區 Community",
      "level": "ap",
      "frameworks": [
        {
          "id": "M10_F1",
          "name": "健康促進與協作流程",
          "desc": "C01 Health and Wellness Promotion 與 C02 Integrative Design 要提供 WELL Feature Guide、health-oriented mission，並促進 collaborative planning process。",
          "covers": ["C01 Health and Wellness Promotion", "C02 Integrative Design", "WELL Feature Guide", "health-oriented mission", "collaborative project process"]
        },
        {
          "id": "M10_F2",
          "name": "緊急準備與韌性資源",
          "desc": "C03 Emergency Preparedness 與 C14 Emergency Resources 要求 risk assessment、emergency management plan、first aid kits、AED 與相關訓練資源。",
          "covers": ["C03 Emergency Preparedness", "C14 Emergency Resources", "risk assessment", "emergency management plan", "automated external defibrillators"]
        },
        {
          "id": "M10_F3",
          "name": "使用者調查與回饋",
          "desc": "C04 Occupant Survey 與 C05 Enhanced Occupant Survey 用第三方或 custom survey 評估 building users 的 experience、self-reported health and well-being。",
          "covers": ["C04 Occupant Survey", "C05 Enhanced Occupant Survey", "occupant surveys", "self-reported health", "custom survey"]
        },
        {
          "id": "M10_F4",
          "name": "包容、家庭與公共健康政策",
          "desc": "C06 Health Services and Benefits、C08 New Parent Support、C09 New Mother Support、C10 Family Support、C12 Diversity and Inclusion 與 C13 Accessibility and Universal Design 將 health benefits、family policies、equity 與 universal design 納入社區健康。",
          "covers": ["C06 Health Services and Benefits", "C08 New Parent Support", "C12 Diversity and Inclusion", "C13 Accessibility and Universal Design", "universal design"]
        }
      ],
      "debates": [
        {
          "id": "M10_D1",
          "title": "標準化政策 vs 在地需求",
          "scenario": "跨國公司想把同一套健康福利與 emergency plan 複製到所有據點，但各地 occupants 的家庭照護、無障礙需求與風險情境不同。",
          "sideA": {
            "label": "採用全球一致政策",
            "args": ["一致格式便於 documentation、治理與內部稽核。", "核心福利與基本 emergency preparedness 可快速展開。"]
          },
          "sideB": {
            "label": "依使用者與在地風險調整",
            "args": ["C04/C05 occupant surveys 可揭露不同族群的真實需求。", "C12/C13 強調 diversity、inclusion 與 universal design，不能只靠總部模板。"]
          },
          "insight": "Community 的重點是把政策落到人群差異；標準化可以建立底線，但調查與包容設計決定是否真的有效。",
          "framework": "M10_F3"
        }
      ],
      "questions": [],
      "reinforcement": []
    },
    {
      "id": "M11",
      "name": "WELL 認證與 Portfolio",
      "level": "ap",
      "frameworks": [
        {
          "id": "M11_F1",
          "name": "認證流程與角色分工",
          "desc": "掌握 WELL Certification 的 registration process、eligibility criteria、timeline、WELL project administrator、owner、WELL AP 與 WELL Coaching support team 的角色責任。",
          "covers": ["WELL Certification", "registration process", "eligibility criteria", "WELL project administrator", "WELL Coaching support team"]
        },
        {
          "id": "M11_F2",
          "name": "計分等級與必備門檻",
          "desc": "WELL v2 是 points-based system，每個 project scorecard 有 110 points available；certification levels 包含 WELL Bronze 40 pts、WELL Silver 50 pts、WELL Gold 60 pts、WELL Platinum 80 pts。",
          "covers": ["110 points available", "WELL Bronze 40 pts", "WELL Silver 50 pts", "WELL Gold 60 pts", "WELL Platinum 80 pts"]
        },
        {
          "id": "M11_F3",
          "name": "文件、Performance Verification 與補救",
          "desc": "認證管理要能處理 WELL digital platform submissions、Performance Verification、non-passing performance verification results 與 corrective actions。",
          "covers": ["WELL digital platform", "Performance Verification", "WELL Performance Testing Agent", "corrective actions", "documentation process"]
        },
        {
          "id": "M11_F4",
          "name": "AAP、等同性與 Innovation",
          "desc": "考試會測 Alternative Adherence Paths (AAP)、equivalencies、precertification、recertification 及 Innovation；WELL v2 另可在 Innovation concept 追求 additional ten points，I01-I05 包含 Innovate WELL 與 WELL AP。",
          "covers": ["Alternative Adherence Paths", "equivalencies", "precertification", "recertification", "I01 Innovate WELL", "I02 WELL Accredited Professional"]
        },
        {
          "id": "M11_F5",
          "name": "WELL Portfolio 範疇與評分",
          "desc": "WELL Portfolio Program 要理解 portfolio scope、eligibility requirements、scales of documentation、review process 與 factors that influence the WELL Portfolio score。",
          "covers": ["WELL Portfolio", "portfolio scope", "eligibility requirements", "scales of documentation", "WELL Portfolio score"]
        }
      ],
      "debates": [
        {
          "id": "M11_D1",
          "title": "單案認證 vs Portfolio 管理",
          "scenario": "企業有多個辦公據點，第一個據點已接近 WELL Silver，管理層正在評估應繼續衝單案高等級，還是改用 WELL Portfolio 擴大到更多據點。",
          "sideA": {
            "label": "追求單案高等級",
            "args": ["單案 WELL Gold 或 WELL Platinum 具明確示範效果。", "資源集中，documentation 與 Performance Verification 較容易控管。"]
          },
          "sideB": {
            "label": "轉向 Portfolio 擴散",
            "args": ["Portfolio 可把策略、文件尺度與 review process 擴展到多資產。", "對企業健康策略，覆蓋更多 occupants 可能比單案分數更有價值。"]
          },
          "insight": "Certification and Portfolio 的考點在策略配適：單案追求深度與示範，Portfolio 追求規模、治理與一致化改善。",
          "framework": "M11_F5"
        },
        {
          "id": "M11_D2",
          "title": "標準路徑 vs AAP",
          "scenario": "專案所在地法規與產品市場不同，部分 WELL feature 的標準文件難以取得，團隊考慮使用 AAP 或 equivalency。",
          "sideA": {
            "label": "堅持標準路徑",
            "args": ["審查邏輯清楚，與既有 feature language 對齊。", "可降低額外解釋與審查往返風險。"]
          },
          "sideB": {
            "label": "提出 AAP/equivalency",
            "args": ["AAP 可回應在地法規、產品與運維條件差異。", "若能證明 intent 與 health outcome 等同，可能比硬套標準更合理。"]
          },
          "insight": "AAP 不是降低標準，而是用替代證據證明同等意圖；考試常會測你能否判斷何時需要替代路徑，以及如何管理文件風險。",
          "framework": "M11_F4"
        }
      ],
      "questions": [],
      "reinforcement": []
    }
  ]
};
