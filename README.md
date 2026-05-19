# 🌐 AI-Policy

## 👥 Team Members
- Hayden Hubbard (@hatori27) - Role/Responsibility
- Wu Cheng (@Nothingisavaliable) - Role/Responsibility
- Daria (@complicatic)- Role/Responsibility
- Sheena (@sheenapham1) - Role/Responsibility
- Stephen (@St-ep-hen) - Role/Responsibility

---

<!-- ## ❓ Research Question
How could the future of AI evolve? Much of this depends on if it is viewed as an opportunity or a danger. One perspective that has not been explored is the relationship between economic freedom and how AI is viewed and discussed. In more economically free countries, is AI innovation encouraged in glowing terms for the sake of the economy? On the other hand, in less economically free countries,  is more cautious terminology utilized to encourage confidence in a watchful government? Our research seeks to answer this question: __what relationship, if any, exists between economic freedom and AI regulatory rhetoric?__


---

## 🔗 Data Sources


| Source | Description | URL |
|---|---|---|
| OECD (Organisation for Economic Co-operation and Development) | National AI policy data, AI governance frameworks, and international policy indicators | [OECD AI Policy Observatory](https://oecd.ai/en/dashboards/national) |
| The Heritage Foundation | Economic Freedom Index scores and rankings across countries | [Economic Freedom Index](https://economicfreedom.heritage.org/pages/all-country-scores) |
| Freedom House | Global indicators of political rights and civil liberties | [Freedom in the World](https://freedomhouse.org/report/freedom-world) |
| V-Dem Institute | Democracy and institutional quality metrics | [V-Dem Dataset](https://www.v-dem.net/data/the-v-dem-dataset/) |
| Comparative Agendas Project (CAP) | Legislative and policy agenda datasets related to technology and AI regulation | [Comparative Agendas Project](https://www.comparativeagendas.net/) |

---

## 📄 Data Sources Details

- OECD AI policy data provides structured information about national AI strategies and regulatory approaches.
- The Economic Freedom Index offers standardized measures of market openness and government intervention.
- Freedom House and V-Dem help control for political systems, institutional quality, and civil liberties.
- CAP provides legislative text and policy agenda information relevant to technology governance.

---

## ⚙️ Methodology

To investigate the relationship between economic freedom and AI regulatory rhetoric, this project will:

- Collect AI-related policy documents from the OECD AI Policy Observatory and obtain economic freedom indicators from the Economic Freedom of the World Index.

- Use OCR and natural language processing (NLP) techniques to extract and analyze AI policy rhetoric within G7 countries’ official policy documents.

- Identify recurring themes, sentiment, and regulatory framing regarding artificial intelligence.

- Compare differences in rhetoric across countries with varying levels of economic freedom.

- Analyze the relationship between Economic Freedom Index scores and AI policy rhetoric using:
  - Qualitative analysis (written interpretation, thematic analysis, and mind maps)
  - Quantitative analysis (correlation analysis and statistical comparison)

--- -->



## 📖 Background

Existing research has examined AI governance through various lenses; however, the relationship between economic freedom and AI-related policy discourse remains underexplored. This research seeks to address that gap by investigating whether a country’s level of economic freedom shapes how governments frame the development and regulation of AI within national strategy documents.

In particular, this study compares the G7 countries and China to analyze how different economic and political environments influence AI regulatory narratives, policy priorities, and governance orientations.

---

# ❓ Research Question

## Primary Research Question

> How do variations in economic freedom across jurisdictions shape the dominant frames, justifications, and priorities embedded in national AI regulatory discourse for G7 countries, and how does this compare to China?

---

## Alternative Research Question

> To what extent do economic freedom and AI vibrancy predict the dominant frames embedded in national AI regulatory discourse, and how do these relationships vary across G7 countries and China?

---

# 🧩 Hypotheses

## 🟢 H1 — AI Vibrancy and Innovation-Oriented Rhetoric

Countries with higher Stanford AI Vibrancy scores will exhibit more innovation-enabling rhetoric in their national policy documents.

### Rationale
Countries with more developed AI ecosystems are expected to have stronger industry stakeholders and innovation-oriented policy agendas, encouraging governments to frame AI regulation in enabling rather than restrictive terms.

---

## 🟡 H2 — Economic Freedom and Positive Regulatory Framing

Countries whose AI regulatory discourse is more positive and innovation-oriented will exhibit higher economic freedom scores.

### Rationale
Positive regulatory framing may reflect broader ideological commitments toward market liberalism and economic openness, which are captured by economic freedom indicators.

---

## 🔵 H3 — Regulatory Framing as a Mediating Mechanism

The relationship between AI vibrancy and economic freedom is partially or fully mediated by the permissiveness of AI regulatory rhetoric.

### Rationale
Regulatory framing may function as an intermediate mechanism linking AI ecosystem maturity to broader economic ideology. In this view, AI vibrancy influences how governments discuss AI, while that discourse reflects and reinforces underlying economic values.

---

# 🛠️ Methodology

## 1️⃣ Text Analysis

National AI strategy and regulatory documents from G7 countries and China will be collected and analyzed using keyword-based text analysis.

The analysis examines the frequency and distribution of framing-related terms within each document to estimate the relative emphasis placed on innovation-oriented versus restriction-oriented discourse.

Each document receives framing scores based on keyword occurrence frequencies.

---

# 🏷️ Framing Categories and Keywords

| Framing Type | Keywords |
|---|---|
| 🚀 Innovation-oriented | "opportunity", "growth", "competitiveness", "innovation", "investment", "leadership", "acceleration" |
| ⚠️ Restriction / Risk-oriented | "risk", "safeguard", "restriction", "compliance", "constraint" |

---

# 📊 Correlation Analysis

Correlation analysis will be conducted to examine relationships between:

- 📈 Economic Freedom scores and regulatory framing scores
- 🤖 Stanford AI Vibrancy scores and regulatory framing scores

The analysis aims to identify whether countries with stronger economic freedom or AI capability exhibit systematically different AI governance narratives.

---

# 🎯 Expected Contribution

This research contributes to the emerging literature on AI governance by connecting political-economic structure with regulatory discourse.

Rather than treating AI policy solely as a technical or legal issue, this study examines how broader economic ideology may shape national narratives surrounding AI development and regulation.

---

# 🧠 Core Analytical Logic

```text
AI Vibrancy
      ↓
Regulatory Framing
      ↓
Economic Freedom Orientation
```

This framework explores whether AI ecosystem maturity influences regulatory rhetoric, and whether that rhetoric reflects broader economic and ideological preferences.

# 📊 Preliminary Results

## Stanford AI Vibrancy Tool — G7 + China

Cross-country comparison of AI vibrancy scores (Total Score and 7 sub-dimensions: R&D, Responsible AI, Economy, Talent, Policy and Governance, Public Opinion, Infrastructure).

![Stanford AI Vibrancy](outputs/stanford_AI_Vibrancy.png)

![Stanford AI Vibrancy Component Radar](outputs/stanford_AI_Vibrancy_component_radar.png)

**Key observations**:
- The United States leads overall (Total Score ≈ 77.85), driven primarily by Responsible AI, Economy, and Infrastructure.
- China ranks second (≈ 35.10) — its R&D score is essentially tied with the U.S., but it lags substantially in Responsible AI, Economy, and Policy & Governance.
- The remaining G7 countries cluster between 12 and 21, with no single G7 member dominating.
- The component radar chart highlights how each country’s AI vibrancy profile differs across R&D, Responsible AI, Economy, Talent, Policy and Governance, Public Opinion, and Infrastructure.

## Index of Economic Freedom — G7 + China

Heritage Foundation Economic Freedom scores for the same eight countries, used as the political-economic context for the framing analysis.

![Index of Economic Freedom](outputs/IEF_score.png)

![Index of Economic Freedom by Year](outputs/IEF_score_by_year.png)

**Key observations**:
- G7 economies generally cluster in the "Mostly Free" / "Moderately Free" range.
- China sits noticeably below the G7, providing a natural contrast for testing whether economic freedom levels relate to AI regulatory framing.
- The yearly trend chart shows how economic freedom scores change over time, providing temporal context for the cross-sectional comparison.

These two visualizations together provide the empirical anchor for the hypotheses (H1–H3): the variation in AI vibrancy and economic freedom across the eight jurisdictions is large enough to test whether either dimension predicts the framing of national AI strategies.

---

## 📁 Folder Structure

```text
AI-Policy/
├── data/
│   ├── AI vibrancy tool screen shot/
│   │   ├── ai_country_scores.csv
│   │   ├── ai_country_scores_long.csv
│   │   └── *.png                         # Stanford AI Vibrancy source screenshots
│   ├── Index of Economic Freedom/
│   │   ├── G7+China All Data
│   │   └── country-level IEF files
│   ├── number/
│   │   ├── ai_dev_index_g7_china.csv
│   │   ├── g7_china_datasets.csv
│   │   ├── ief_g7_china_panel.csv
│   │   └── PUBLIC DATA_ 2026 AI INDEX REPORT/
│   └── pdf/
│       └── AI Policy/
│           ├── CN_National_AI_Strategy.pdf
│           ├── DE_National_AI_Strategy.pdf
│           ├── FR__National_AI_Strategy.pdf
│           ├── IT_National_AI_Strategy.pdf
│           ├── US_National_AI_Strategy.pdf
│           └── _extracted/               # Extracted text and text-analysis outputs
│
├── notebooks/
│   ├── AI Development/
│   │   ├── ai_vibrancy_tool.ipynb
│   │   ├── ai_dev_index_v2.ipynb
│   │   └── select_g7_china_data.ipynb
│   ├── Economic Freedom/
│   │   └── ief_g7_china_analysis.ipynb
│   └── Text Analysis/
│       └── national_ai_strategy_text_analysis.ipynb
│
├── outputs/
│   ├── stanford_AI_Vibrancy.png
│   ├── stanford_AI_Vibrancy_component_radar.png
│   ├── IEF_score.png
│   └── IEF_score_by_year.png
│
├── README.md
├── README.pdf
└── LICENSE
```
