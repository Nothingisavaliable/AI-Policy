# AI-Policy

## Team Members
- Hayden Hubbard (@hatori27)
- Wu Cheng (@Nothingisavaliable)
- Daria (@complicatic)
- Sheena (@sheenapham1)
- Stephen (@St-ep-hen)

---

<!-- ## Research Question
How could the future of AI evolve? Much of this depends on if it is viewed as an opportunity or a danger. One perspective that has not been explored is the relationship between economic freedom and how AI is viewed and discussed. In more economically free countries, is AI innovation encouraged in glowing terms for the sake of the economy? On the other hand, in less economically free countries,  is more cautious terminology utilized to encourage confidence in a watchful government? Our research seeks to answer this question: __what relationship, if any, exists between economic freedom and AI regulatory rhetoric?__


---

## Data Sources


| Source | Description | URL |
|---|---|---|
| Google Drive source folder | National AI strategy PDF documents used for text analysis | [AI Policy PDFs](https://drive.google.com/drive/folders/1CCiBmppafwtXLRVTpnryIY8Y9PLvxwvG) |
| The Heritage Foundation | Economic Freedom Index scores and rankings across countries | [Economic Freedom Index](https://economicfreedom.heritage.org/pages/all-country-scores) |
| Freedom House | Global indicators of political rights and civil liberties | [Freedom in the World](https://freedomhouse.org/report/freedom-world) |
| V-Dem Institute | Democracy and institutional quality metrics | [V-Dem Dataset](https://www.v-dem.net/data/the-v-dem-dataset/) |
| Comparative Agendas Project (CAP) | Legislative and policy agenda datasets related to technology and AI regulation | [Comparative Agendas Project](https://www.comparativeagendas.net/) |

---

## Data Sources Details

- The Google Drive source folder provides the national AI strategy PDFs used for text extraction and framing analysis.
- The Heritage Foundation Index of Economic Freedom offers standardized measures of market openness and government intervention.
- Freedom House and V-Dem help control for political systems, institutional quality, and civil liberties.
- CAP provides legislative text and policy agenda information relevant to technology governance.

---

## Methodology

To investigate the relationship between economic freedom and AI regulatory rhetoric, this project will:

- Collect AI-related policy documents from the Google Drive source folder and obtain economic freedom indicators from the Heritage Foundation Index of Economic Freedom.

- Use OCR and natural language processing (NLP) techniques to extract and analyze AI policy rhetoric within G7 countries’ official policy documents.

- Identify recurring themes, sentiment, and regulatory framing regarding artificial intelligence.

- Compare differences in rhetoric across countries with varying levels of economic freedom.

- Analyze the relationship between Economic Freedom Index scores and AI policy rhetoric using:
  - Qualitative analysis (written interpretation, thematic analysis, and mind maps)
  - Quantitative analysis (correlation analysis and statistical comparison)

--- -->



## Background

Existing research has examined AI governance through various lenses; however, the relationship between economic freedom and AI-related policy discourse remains underexplored. This research seeks to address that gap by investigating whether a country’s level of economic freedom shapes how governments frame the development and regulation of AI within national strategy documents.

In particular, this study compares the G7 countries and China to analyze how different economic and political environments influence AI regulatory narratives, policy priorities, and governance orientations.

---

# Research Question

> How do variations in economic freedom and AI vibrancy  shape the dominant framing embedded in national discourse, and how do these relationships vary across G7 countries and  China?

---

# Hypotheses

## H1 — AI Vibrancy and Innovation-Oriented Rhetoric

Countries with higher Stanford AI Vibrancy scores will exhibit more innovation-enabling rhetoric in their national policy documents.

### Rationale
Countries with more developed AI ecosystems are expected to have stronger industry stakeholders and innovation-oriented policy agendas, encouraging governments to frame AI regulation in enabling rather than restrictive terms.

---

## H2 — AI Vibrancy and Risk-Oriented Rhetoric

Countries with lower Stanford AI Vibrancy scores will exhibit more risk-enabling rhetoric in their national policy documents.

### Rationale
Countries with less developed AI ecosystems are expected to have weaker industry stakeholders and risk-oriented policy agendas, encouraging governments to frame AI regulation in restrictive rather than enabling terms.

---

## H3 — Economic Freedom and Positive Regulatory Framing

Countries whose AI regulatory discourse is more positive and innovation-oriented will exhibit higher economic freedom scores.

### Rationale
Positive regulatory framing may reflect broader ideological commitments toward market liberalism and economic openness, which are captured by economic freedom indicators.

---

## H4 — Economic Freedom and Negative Regulatory Framing

Countries whose AI regulatory discourse is more negative and risk-oriented will exhibit lower economic freedom scores.

### Rationale
Negative regulatory framing may reflect broader ideological commitments away from market liberalism and economic openness, which are captured by economic freedom indicators.

---

# Methodology

## AI Vibrancy

AI vibrancy is measured using the Stanford AI Index country-level AI Vibrancy scores for the G7 countries and China. The main country-level predictor is the **Total Score**, renamed in the analysis as `AI Vibrancy Score`. Component dimensions such as R&D, Responsible AI, Economy, Talent, Policy and Governance, Public Opinion, and Infrastructure are retained for descriptive analysis.

## Economic Freedom

Economic freedom is measured using the Heritage Foundation Index of Economic Freedom panel. The correlation study uses the latest available year in the local panel, currently **2026**, and uses `Overall Score` as `IEF Overall Score`.

## Text Analysis

National AI strategy and regulatory documents from G7 countries, China, and the European Union are analyzed using sentence-level AI regulatory framing. English documents are used directly. Chinese-heavy texts are translated into English with `facebook/nllb-200-distilled-600M` or analyzed through an existing English analysis corpus where available.

The current text-analysis workflow uses **DeepSeek R1 14B through Ollama** for local sentence classification. Each sentence is classified independently into one of five labels:

| Label | Meaning |
|---|---|
| Innovation-oriented | Emphasizes innovation, investment, adoption, competitiveness, productivity, and flexible regulation |
| Risk-oriented | Emphasizes risk, safety, accountability, privacy, fairness, human rights, and regulatory obligations |
| Mixed | A single sentence contains both innovation and risk framing |
| Neutral | Descriptive, administrative, or procedural sentences |
| Unsure | Unclear residual category; excluded from the no-unsure human-gold calibration set |

The model prompt includes the project codebook and human-annotated gold examples. The model returns structured JSON with a label, confidence score, and reason. Both the raw model label and the final corrected label are retained for auditing.

## Human Calibration and Correction

The LLM labeling workflow is calibrated with human expert annotations rather than treated as a fully automatic black box. A sample of 40 sentences was independently annotated by multiple human annotators. Annotator 1 showed lower annotation stability, so the final calibration workflow uses the Daria + Stephen consensus labels.

Daria and Stephen agreed on 23 sentences. For the current `daria_stephen_no_unsure_full` run, human-gold `Unsure` labels are excluded, leaving **16 substantive gold labels** for few-shot examples, exact sentence overrides, and model evaluation. Raw DeepSeek accuracy on this usable gold set is **75%**; after exact human-gold overrides, corrected accuracy is **100%**. The full run applies **4 human overrides**.

Correction logic:

```text
corrected_label =
    human_gold_label, if the sentence is present in the usable human gold set
    model_label, otherwise
```

Country/entity framing summaries are computed from corrected labels. Innovation-oriented sentences score `+1`, risk-oriented sentences score `-1`, and mixed, neutral, and unsure sentences score `0` for the net framing measure. The main aggregate variables are `Innovation Share`, `Risk Share`, `Mean Framing Score`, and the smoothed `Innovation-to-Risk Ratio`.

---

# Correlation Analysis

Correlation analysis is conducted in `notebooks/Correlation Study/correlation_study.ipynb` to examine relationships between:

- Stanford AI Vibrancy scores and innovation-oriented framing
- Stanford AI Vibrancy scores and risk-oriented framing
- Economic Freedom scores and innovation-oriented framing
- Risk-oriented framing and Economic Freedom scores
- Combined AI Vibrancy + Economic Freedom predictors and the log innovation-to-risk framing ratio

The current notebook uses the corrected DeepSeek framing output by default: `outputs/deepseek_ai_framing_summary_corrected_daria_stephen_no_unsure_full.csv`. The European Union is included in descriptive framing summaries but excluded from the G7 + China correlation sample because comparable AI Vibrancy and IEF country scores are not used for it in this study.

Because the merged country-level sample has only eight observations, all correlation coefficients, regressions, and mediation diagnostics are interpreted as exploratory and directional rather than confirmatory.

---

# Expected Contribution

This research contributes to the emerging literature on AI governance by connecting political-economic structure with regulatory discourse.

Rather than treating AI policy solely as a technical or legal issue, this study examines how broader economic ideology may shape national narratives surrounding AI development and regulation.

---

# Core Analytical Logic

```text
AI Vibrancy
      ↓
Regulatory Framing
      ↓
Economic Freedom Orientation
```

This framework explores whether AI ecosystem maturity influences regulatory rhetoric, and whether that rhetoric reflects broader economic and ideological preferences.

# Preliminary Results

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

## Descriptive Statistics — Key Numeric Variables

To address the feedback, the project now explicitly reports standard descriptive statistics for the main numeric variables. The tables below report count, mean, median, standard deviation, minimum, and maximum for the Heritage Index of Economic Freedom scores and Stanford AI Vibrancy metrics.

**Index of Economic Freedom**

| Variable | count | mean | median | stdev | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| Overall Score | 256 | 68.48 | 70.3 | 8.49 | 48.0 | 81.2 |
| Property Rights | 256 | 77.09 | 85.95 | 20.04 | 20.0 | 96.2 |
| Government Integrity | 256 | 70.47 | 76.0 | 17.9 | 22.0 | 95.1 |
| Judicial Effectiveness | 80 | 76.22 | 76.8 | 14.36 | 37.4 | 97.9 |
| Tax Burden | 256 | 61.41 | 62.35 | 10.62 | 33.2 | 80.0 |
| Government Spending | 256 | 43.14 | 43.95 | 22.77 | 0.0 | 95.9 |
| Fiscal Health | 80 | 48.77 | 54.55 | 30.69 | 0.0 | 92.9 |
| Business Freedom | 256 | 79.47 | 83.5 | 11.59 | 43.1 | 100.0 |
| Labor Freedom | 176 | 67.27 | 68.05 | 14.97 | 39.9 | 98.5 |
| Monetary Freedom | 256 | 81.03 | 81.5 | 5.96 | 61.5 | 94.3 |
| Trade Freedom | 256 | 79.42 | 80.8 | 9.94 | 20.0 | 88.8 |
| Investment Freedom | 256 | 66.19 | 70.0 | 18.3 | 20.0 | 90.0 |
| Financial Freedom | 256 | 63.12 | 70.0 | 17.72 | 20.0 | 90.0 |

**Stanford AI Vibrancy**

| Variable | count | mean | median | stdev | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| Total Score | 8 | 26.04 | 17.16 | 22.12 | 12.35 | 77.85 |
| R&D | 8 | 2.99 | 0.9 | 4.08 | 0.41 | 9.61 |
| Responsible AI | 8 | 3.26 | 1.3 | 4.77 | 0.49 | 14.29 |
| Economy | 8 | 2.35 | 0.57 | 4.84 | 0.15 | 14.29 |
| Talent | 8 | 4.94 | 4.63 | 1.46 | 3.35 | 7.72 |
| Policy and Governance | 8 | 3.31 | 2.29 | 3.24 | 0.53 | 9.71 |
| Public Opinion | 8 | 4.18 | 3.22 | 2.73 | 0.61 | 8.44 |
| Infrastructure | 8 | 5.01 | 4.03 | 3.89 | 1.67 | 13.85 |

The CSV versions are saved in `outputs/descriptive_statistics_ief.csv`, `outputs/descriptive_statistics_ai_vibrancy.csv`, and `outputs/descriptive_statistics_key_numeric_variables.csv`.

## DeepSeek Corrected Innovation vs. Risk Framing

The corrected DeepSeek sentence-level classifier labels each policy sentence as innovation-oriented, risk-oriented, mixed, neutral, or unsure. Innovation-oriented sentences emphasize adoption, investment, productivity, competitiveness, regulatory flexibility, and deployment. Risk-oriented sentences emphasize safety, accountability, privacy, fairness, rights protection, regulatory obligations, and precaution.

The current corrected full run contains **3,730 sentences** across nine countries/entities, including the European Union for descriptive framing analysis. The strongest positive mean framing scores are France (`0.577`), the United Kingdom (`0.575`), and China (`0.598`). Canada (`0.088`) and the United States (`0.173`) show the lowest mean framing scores in the corrected summary.

![DeepSeek Corrected Country Framing Summary](outputs/deepseek_ai_framing_country_summary_corrected_daria_stephen_no_unsure_full.png)

Outputs are saved in `outputs/deepseek_ai_framing_sentence_labels_raw_daria_stephen_no_unsure_full.csv`, `outputs/deepseek_ai_framing_sentence_labels_corrected_daria_stephen_no_unsure_full.csv`, `outputs/deepseek_ai_framing_summary_corrected_daria_stephen_no_unsure_full.csv`, `outputs/deepseek_ai_framing_gold_metrics_daria_stephen_no_unsure_full.csv`, and `outputs/deepseek_ai_framing_gold_confusion_daria_stephen_no_unsure_full.csv`.

These corrected outputs provide the empirical anchor for H1-H4 by translating sentence-level regulatory discourse into country/entity-level innovation and risk framing measures.

## Correlation Study — Vibrancy, Economic Freedom, and Framing

The correlation study combines Stanford AI Vibrancy scores, 2026 Heritage Index of Economic Freedom scores, and corrected DeepSeek framing results for the same G7 + China country set. The main hypothesis tests use `Innovation Share` and `Risk Share`; robustness checks use `Mean Framing Score` and the log smoothed innovation-to-risk ratio.

![Correlation Study Scatter](outputs/correlation_study_scatter_deepseek_corrected_daria_stephen_no_unsure_full.png)

![Correlation Study Matrix](outputs/correlation_study_matrix_deepseek_corrected_daria_stephen_no_unsure_full.png)

**Current exploratory results using corrected DeepSeek framing**:
- H1 expects AI Vibrancy to be positively associated with `Innovation Share`, but the current Pearson correlation is near zero and slightly negative (`r = -0.030`, `p = 0.9429`). Directional support is not observed.
- H2 expects lower AI Vibrancy to be associated with higher `Risk Share`, but the observed AI Vibrancy to Risk Share correlation is positive (`r = 0.407`, `p = 0.3172`). Directional support is not observed.
- H3 expects higher IEF scores to be associated with higher `Innovation Share`, but the observed relationship is negative (`r = -0.689`, `p = 0.0589`). Directional support is not observed.
- H4 expects `Risk Share` to be negatively associated with IEF, but the observed relationship is positive (`r = 0.534`, `p = 0.1728`). Directional support is not observed.
- Robustness checks using the log innovation-to-risk ratio also do not support the expected positive relationships with AI Vibrancy (`r = -0.264`, `p = 0.5280`) or IEF (`r = -0.478`, `p = 0.2312`).
- The combined model predicting log innovation-to-risk ratio from AI Vibrancy and IEF has `R2 = 0.298`, but with only eight observations it should be interpreted as a descriptive diagnostic.
- The mediation diagnostic is retained as a mechanism check, not a formal causal test.

Key outputs are saved in `outputs/correlation_study_dataset_deepseek_corrected_daria_stephen_no_unsure_full.csv`, `outputs/correlation_study_correlations_deepseek_corrected_daria_stephen_no_unsure_full.csv`, `outputs/correlation_study_regression_models_deepseek_corrected_daria_stephen_no_unsure_full.csv`, and `outputs/correlation_study_mediation_deepseek_corrected_daria_stephen_no_unsure_full.csv`.

---

## Folder Structure

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
│           ├── CA_National_AI_Strategy.pdf
│           ├── CA_National_AI_Strategy_ocr.pdf
│           ├── CN_National_AI_Strategy.pdf
│           ├── DE_National_AI_Strategy.pdf
│           ├── EU_AI_Strategy.pdf
│           ├── FR__National_AI_Strategy.pdf
│           ├── IT_National_AI_Strategy.pdf
│           ├── JP_National_AI_Strategy.pdf
│           ├── JP_National_AI_Strategy_ocr.pdf
│           ├── UK_National_AI_Strategy.pdf
│           ├── UK_National_AI_Strategy_ocr.pdf
│           ├── US_National_AI_Strategy.pdf
│           ├── 国务院关于深入实施“人工智能+”行动的意见.pdf
│           ├── _extracted/
│           │   ├── *.txt                 # Extracted strategy text by country/entity
│           │   ├── document_sources.csv
│           │   ├── document_stats.csv
│           │   ├── theme_counts_raw.csv
│           │   ├── theme_per_1000_words.csv
│           │   ├── framing_keyword_counts.csv
│           │   ├── framing_category_counts.csv
│           │   ├── framing_scores_per_1000_words.csv
│           │   ├── framing_share_of_mentions.csv
│           │   ├── keyword_sentence_matches.csv
│           │   └── similarity_matrix.csv
│           └── _translated_nllb/
│               ├── China.txt             # NLLB English translation for Chinese-heavy policy text
│               └── translation_stats.csv
│
├── notebooks/
│   ├── AI Development/
│   │   ├── ai_vibrancy_tool.ipynb
│   │   ├── ai_dev_index_v2.ipynb
│   │   └── select_g7_china_data.ipynb
│   ├── Correlation Study/
│   │   └── correlation_study.ipynb
│   ├── Economic Freedom/
│   │   └── ief_g7_china_analysis.ipynb
│   └── Text Analysis/
│       ├── national_ai_strategy_nllb_translation.ipynb
│       ├── human_expert_framing_labels_analysis.ipynb
│       └── LLM_based_text_framing_analysis.ipynb
│
├── outputs/
│   ├── stanford_AI_Vibrancy.png
│   ├── stanford_AI_Vibrancy_component_radar.png
│   ├── IEF_score.png
│   ├── IEF_score_by_year.png
│   ├── deepseek_ai_framing_summary_corrected_daria_stephen_no_unsure_full.csv
│   ├── deepseek_ai_framing_sentence_labels_corrected_daria_stephen_no_unsure_full.csv
│   ├── deepseek_ai_framing_gold_metrics_daria_stephen_no_unsure_full.csv
│   ├── deepseek_ai_framing_country_summary_corrected_daria_stephen_no_unsure_full.png
│   ├── correlation_study_dataset_deepseek_corrected_daria_stephen_no_unsure_full.csv
│   ├── correlation_study_correlations_deepseek_corrected_daria_stephen_no_unsure_full.csv
│   ├── correlation_study_regression_models_deepseek_corrected_daria_stephen_no_unsure_full.csv
│   ├── correlation_study_mediation_deepseek_corrected_daria_stephen_no_unsure_full.csv
│   ├── correlation_study_scatter_deepseek_corrected_daria_stephen_no_unsure_full.png
│   └── correlation_study_matrix_deepseek_corrected_daria_stephen_no_unsure_full.png
│
├── README.md
├── README.pdf
└── LICENSE
```
