#!/usr/bin/env python3
"""Add M12 Innovation module to content.js. Frameworks grounded in WELL v2
Innovation concept (I01-I05, up to 10 points). Idempotent."""
from content_io import load, save

M12 = {
    "id": "M12",
    "name": "創新 Innovation",
    "level": "ap",
    "frameworks": [
        {
            "id": "M12_F1",
            "name": "創新提案路徑",
            "desc": "理解 Feature I01: Innovate WELL 如何讓專案提出 WELL v2 尚未涵蓋的新介入策略，提案須以 novel way 正向影響 occupants、有 scientific/medical/industry research 佐證，並符合法規與 leading practices。",
            "analogy": "像在既有規則之外提一個經審查的實驗性做法，必須拿得出證據才被 IWBI 接受。",
            "covers": ["I01 Innovate WELL", "Propose Innovations", "novel intervention", "scientific substantiation", "up to 10 points"]
        },
        {
            "id": "M12_F2",
            "name": "專業參與與教育推廣",
            "desc": "掌握 Feature I02: WELL Accredited Professional 與 Feature I03: Experience WELL Certification：專案團隊至少一人取得並維持 WELL AP 認證至 initial certification，並透過 public tours 與教育策略推廣 WELL。",
            "covers": ["I02 WELL Accredited Professional", "I03 Experience WELL Certification", "maintain accreditation", "public tours", "educational strategies"]
        },
        {
            "id": "M12_F3",
            "name": "既有計畫等同加分",
            "desc": "理解 Feature I04: Gateways to Wellness 與 Feature I05: Green Building Rating Systems：以三年內完成的 health and wellness program、或取得 IWBI 認可的 green building rating（如 LEED）換取創新分，I05 最多 5 分且不可疊加。",
            "covers": ["I04 Gateways to Wellness", "I05 Green Building Rating Systems", "health and wellness program", "green building certification", "5 point cap"]
        },
        {
            "id": "M12_F4",
            "name": "創新計分與驗證",
            "desc": "Innovation concept 全部為 optimization，專案最多取得 10 分；各 Innovation feature 的 verification method（technical document、letter of assurance 等）與計分上限是常見考點。",
            "covers": ["Innovation scoring", "optimization", "verification method", "10 point maximum", "pre-approved strategies"]
        }
    ],
    "debates": [
        {
            "id": "M12_D1",
            "title": "自提創新 vs 採用既有等同路徑",
            "scenario": "一個專案想提升 Innovation 得分，團隊在「用 I01 自提一個全新介入」與「直接走 I04/I05 既有等同計畫（如取得 LEED）」之間取捨。",
            "sideA": {
                "label": "走 I01 自提創新",
                "args": ["可針對專案獨特健康議題量身設計，建立差異化示範價值。", "若提案被 IWBI 接受，最多可貢獻 10 分。"]
            },
            "sideB": {
                "label": "採用 I04/I05 既有路徑",
                "args": ["green building rating 或 wellness program 多已在進行，文件成本低、結果可預期。", "不需經過 IWBI 提案審查的不確定性，落地風險小。"]
            },
            "insight": "Innovation 的考點在路徑配適：I01 追求原創與高上限但需 research 佐證與審查；I04/I05 以既有等同成果換確定但有限的分數。"
        },
        {
            "id": "M12_D2",
            "title": "WELL AP 參與是分數還是流程價值",
            "scenario": "業主質疑為了 Feature I02 的 1 分是否值得在團隊中配置 WELL AP，認為可由顧問代辦。",
            "sideA": {
                "label": "視為流程加速器",
                "args": ["WELL AP 熟悉 feature 門檻與 verification，能 streamline 認證流程、減少退件。", "1 分之外更大的價值在專案規劃階段的決策品質。"]
            },
            "sideB": {
                "label": "視為單純計分項",
                "args": ["若團隊已有充足 WELL 經驗，I02 的 1 分邊際效益有限。", "資源可投入分數更高的 optimization features。"]
            },
            "insight": "I02 的關鍵在 AP 需維持認證至 initial certification——它同時是 1 分的計分項，也反映團隊對流程治理的投入。",
            "framework": "M12_F2"
        }
    ],
    "questions": [],
    "reinforcement": []
}

def main():
    data, var = load()
    ids = [m["id"] for m in data["modules"]]
    if "M12" in ids:
        # replace existing (idempotent), keep its questions if any
        idx = ids.index("M12")
        existing_q = data["modules"][idx].get("questions", [])
        existing_r = data["modules"][idx].get("reinforcement", [])
        new = dict(M12)
        new["questions"] = existing_q or []
        new["reinforcement"] = existing_r or []
        data["modules"][idx] = new
        print("M12 replaced (preserved questions:", len(existing_q), ")")
    else:
        data["modules"].append(M12)
        print("M12 appended")
    save(data, var)
    print("modules now:", [m["id"] for m in data["modules"]])

if __name__ == "__main__":
    main()
