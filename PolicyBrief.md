# AI Policy Brief

---

## Introduction
**Contributors: Hayden and Stephen**

### Context
- Review of existing research
- Importance and relevance of the topic
- Why this matters to stakeholders

### Research Framework
This brief examines the relationship between AI ecosystem vibrancy and economic policy environments, using:
- **Stanford AI Vibrancy Index** – measures the health and dynamism of AI ecosystems
- **Economic Freedom Scores** – indicators of regulatory openness and market-based policies

### Executive Summary
- [Stephen to add 5 key bullet points here]

---

## Research Hypotheses

**H1:** Countries with higher Stanford AI Vibrancy scores will exhibit more innovation-enabling rhetoric in their national policy documents.

**H2:** Countries with less developed AI ecosystems are expected to have weaker industry stakeholders and risk-oriented policy agendas, encouraging governments to frame AI regulation in restrictive rather than innovation-focused terms.

**H3:** Countries whose AI regulatory discourse is more positive and innovation-oriented will exhibit higher economic freedom scores.

**H4:** Countries whose AI regulatory discourse is more negative and risk-oriented will exhibit lower economic freedom scores.

---

## Methodology
**Lead: Cheng**

### Data Sources
This project combines three types of evidence: country-level AI ecosystem indicators, economic freedom indicators, and sentence-level AI policy discourse.

1. **AI Vibrancy**  
   AI ecosystem strength is measured using Stanford AI Index AI Vibrancy country scores for the G7 countries and China. The main variable is the overall **AI Vibrancy Score**, with component dimensions such as R&D, Responsible AI, Economy, Talent, Policy and Governance, Public Opinion, and Infrastructure retained for descriptive analysis.

2. **Economic Freedom**  
   Economic freedom is measured using the Heritage Foundation Index of Economic Freedom. The analysis uses the latest year available in the project panel, **2026**, and focuses on the **IEF Overall Score**.

3. **National AI Policy Texts**  
   The text corpus includes national AI strategy and AI policy documents from the G7 countries and China. The European Union is also included in the descriptive framing analysis as an influential regulatory benchmark, but it is excluded from the correlation analysis because the main predictors are country-level AI Vibrancy and IEF scores.

4. **Human Expert Labels**  
   Human annotation is used to calibrate and audit the LLM labels. Daria and Stephen agreed on 23 sampled sentences. After excluding human-gold `Unsure` labels, the current workflow uses **16 substantive human gold labels** for few-shot prompting, exact-match correction, and evaluation.

### Analysis Techniques
- **Sentence-Level Framing Analysis**  
  The unit of analysis is the sentence. Each policy sentence is classified into one of five framing labels:
  - **Innovation-oriented**: emphasizes innovation, adoption, investment, competitiveness, productivity, or flexible regulation.
  - **Risk-oriented**: emphasizes risk, safety, accountability, privacy, fairness, human rights, or regulatory obligations.
  - **Mixed**: contains both innovation and risk framing in the same sentence.
  - **Neutral**: descriptive, administrative, or procedural.
  - **Unsure**: unclear residual category.

- **LLM Labeling and Human Correction**  
  Sentence labels are generated locally using **DeepSeek R1 14B via Ollama**. The prompt includes the project codebook and human-annotated examples. The model returns structured JSON containing the label, confidence score, and reason. The workflow retains both raw model labels and corrected labels.

  Correction rule:

  ```text
  corrected_label =
      human_gold_label, if the sentence is present in the usable human gold set
      model_label, otherwise
  ```

  In the current run, raw DeepSeek accuracy on the usable human gold set is **75%**. After exact human-gold overrides, corrected accuracy is **100%**, with **4 human overrides** applied.

- **Country-Level Framing Measures**  
  Corrected sentence labels are aggregated by country. Innovation-oriented sentences receive `+1`, risk-oriented sentences receive `-1`, and mixed, neutral, and unsure sentences receive `0` in the net framing score. The main country-level measures are:
  - **Innovation Share**
  - **Risk Share**
  - **Mean Framing Score**
  - **Innovation-to-Risk Ratio**
  - **Log Innovation-to-Risk Ratio**

- **Correlation Analysis**  
  The correlation study merges Stanford AI Vibrancy scores, 2026 IEF scores, and corrected DeepSeek framing measures for the G7 countries plus China. Because the country-level sample contains only **8 observations**, the analysis is exploratory. Pearson and Spearman correlations, OLS regressions, and an exploratory mediation diagnostic are interpreted as directional evidence rather than confirmatory causal estimates.

---

## Results
**Lead Contributors: Sheena, Daria, and Cheng**

### Key Findings
**Headline findings**
- The full G7 + China sample does not support H1-H4: AI Vibrancy and Economic Freedom do not map cleanly onto innovation- or risk-oriented AI policy rhetoric.
- Outlier sensitivity checks reveal two theoretically important cases: the United States is a high-vibrancy but risk-conscious case, while China is a low-IEF but strongly innovation-oriented case.
- Removing the United States substantially changes the AI Vibrancy relationship: H1 becomes strongly positive and H2 flips into the expected direction. Removing China weakens H3 but does not rescue the economic freedom hypotheses.
- The main interpretation is not that outliers should be removed, but that AI governance discourse reflects different national governance models, not only macro-level AI capacity or economic openness.

1. **The corrected framing model identifies meaningful variation across countries, but most countries are more innovation-oriented than risk-oriented.**  
   Across the full corrected framing run, the model labeled **3,730 sentences** across 9 countries/entities. China, France, and the United Kingdom have the highest mean framing scores, indicating strongly innovation-oriented policy language. Canada and the United States have the lowest mean framing scores among the analyzed cases, reflecting a more balanced or risk-conscious discourse.

   ![Corrected DeepSeek framing summary](outputs/deepseek_ai_framing_country_summary_corrected_daria_stephen_no_unsure_full.png)

   | Country/entity | Total sentences | Innovation-oriented | Risk-oriented | Mean framing score | Innovation-to-risk ratio |
   |---|---:|---:|---:|---:|---:|
   | China | 241 | 167 | 23 | 0.598 | 7.128 |
   | France | 215 | 130 | 6 | 0.577 | 20.077 |
   | United Kingdom | 372 | 233 | 19 | 0.575 | 11.974 |
   | Japan | 176 | 96 | 35 | 0.347 | 2.718 |
   | Germany | 462 | 215 | 79 | 0.294 | 2.711 |
   | Italy | 440 | 190 | 60 | 0.295 | 3.149 |
   | United States | 381 | 167 | 101 | 0.173 | 1.650 |
   | Canada | 306 | 105 | 78 | 0.088 | 1.344 |

   The correlation figures below summarize the G7 + China hypothesis tests, the outlier-excluded sensitivity checks, and pairwise relationships among the merged quantitative variables.

   ![Correlation study scatter plots](outputs/correlation_study_scatter_deepseek_corrected_daria_stephen_no_unsure_full.png)

   ![Outlier-excluded correlation study scatter plots](outputs/correlation_study_scatter_outlier_excluded_deepseek_corrected_daria_stephen_no_unsure_full.png)

   ![Correlation study matrix](outputs/correlation_study_matrix_deepseek_corrected_daria_stephen_no_unsure_full.png)

   ![Outlier sensitivity check](outputs/correlation_study_outlier_sensitivity_plot_deepseek_corrected_daria_stephen_no_unsure_full.png)

2. **In the full sample, AI Vibrancy does not predict more innovation-oriented rhetoric.**  
   H1 expected countries with higher AI Vibrancy scores to show more innovation-oriented language. The observed Pearson correlation between AI Vibrancy and Innovation Share is almost zero and slightly negative (`r = -0.030`, `p = 0.9429`). This means the current G7 + China sample does **not** support H1.

3. **In the full sample, lower AI Vibrancy does not predict more risk-oriented rhetoric.**  
   H2 expected lower AI Vibrancy to correspond to higher Risk Share. The observed relationship moves in the opposite direction: AI Vibrancy and Risk Share are positively correlated (`r = 0.407`, `p = 0.3172`). This does **not** support H2.

4. **Economic freedom is not associated with more innovation-oriented framing in the expected direction.**  
   H3 expected higher IEF scores to align with higher Innovation Share. Instead, the observed correlation is negative (`r = -0.689`, `p = 0.0589`). Although this is not treated as confirmatory evidence because `N = 8`, it clearly does **not** support the expected positive direction.

5. **Risk-oriented framing is not associated with lower economic freedom in this sample.**  
   H4 expected countries with more risk-oriented AI discourse to have lower IEF scores. The observed correlation between Risk Share and IEF is positive (`r = 0.534`, `p = 0.1728`), so H4 is **not supported**.

6. **Robustness checks using the log innovation-to-risk ratio reach the same overall conclusion.**  
   The log innovation-to-risk ratio is negatively associated with both AI Vibrancy (`r = -0.264`, `p = 0.5280`) and IEF (`r = -0.478`, `p = 0.2312`). The combined OLS model using AI Vibrancy and IEF explains some variation descriptively (`R2 = 0.298`), but the sample is too small for strong inference.

7. **Outlier sensitivity checks reveal two theoretically important cases: the United States and China.**  
   The United States is treated as a sensitivity case for H1/H2 because it is by far the highest-AI-vibrancy country but has comparatively risk-conscious policy framing. China is treated as a sensitivity case for H3/H4 because it has the lowest IEF score but one of the strongest innovation-oriented framing profiles. These exclusions are diagnostic, not replacements for the full-sample results.

   | Test | Full sample result | Outlier-excluded result | Interpretation |
   |---|---:|---:|---|
   | H1: AI Vibrancy -> Innovation Share | `r = -0.030` | Excluding U.S.: `r = 0.737` | H1 becomes strongly positive once the high-vibrancy, risk-conscious U.S. case is removed |
   | H2: AI Vibrancy -> Risk Share | `r = 0.407` | Excluding U.S.: `r = -0.326` | Direction flips to the expected negative relationship, but remains weak |
   | H3: IEF -> Innovation Share | `r = -0.689` | Excluding China: `r = -0.430` | Negative relationship weakens but still does not support H3 |
   | H4: Risk Share -> IEF | `r = 0.534` | Excluding China: `r = 0.687` | Relationship remains opposite to H4 and becomes stronger |

   The outlier results suggest that the U.S. and China are not merely statistical noise. They represent substantively different AI governance models: the United States combines high AI capacity with risk-conscious discourse, while China combines low economic freedom with state-led innovation framing.

### Hypothesis Summary

| Hypothesis | Expected relationship | Result |
|---|---|---|
| H1 | Higher AI Vibrancy -> more innovation-oriented rhetoric | Not supported |
| H2 | Lower AI Vibrancy -> more risk-oriented rhetoric | Not supported |
| H3 | Higher Economic Freedom -> more innovation-oriented rhetoric | Not supported |
| H4 | More risk-oriented rhetoric -> lower Economic Freedom | Not supported |

Outlier sensitivity changes the interpretation of H1 most clearly: excluding the United States produces a strong positive AI Vibrancy-to-Innovation Share relationship. However, because this is a seven-country diagnostic after removing a theoretically unusual case, the full-sample result remains the main finding.

### Interpretation of Results

The current results suggest that national AI policy rhetoric is not simply a reflection of AI ecosystem strength or market-oriented economic policy. Countries with high AI Vibrancy, such as the United States, can still use relatively risk-conscious language. Countries with lower economic freedom, such as China, can still frame AI policy in strongly innovation-oriented terms. The outlier sensitivity checks sharpen this point: the U.S. and China are precisely the cases that complicate simple linear expectations.

Substantively, this implies that AI policy discourse may be shaped by strategic state priorities, institutional governance traditions, geopolitical competition, and document purpose, rather than by economic freedom or AI ecosystem maturity alone.

The most important policy takeaway is therefore negative but informative: **AI governance rhetoric should not be assumed to map neatly onto economic openness or AI development capacity.** Policymakers and analysts should examine the content and institutional context of AI policy documents directly rather than inferring regulatory orientation from macro-level indicators alone.

---

## Discussion
**Lead Contributors: Daria and Sheena**

### Interpretation
- What do these results reveal about AI policy landscapes?
- Implications for understanding the vibrancy-policy relationship

### Limitations
- [Research constraints and caveats]
- [Data limitations]
- [Methodological considerations]

---

## Conclusion & Future Directions
**Lead: Stephen (with contributions from team)**

### Key Takeaways
- [Main findings summary]

### Policy Implications
- [What policymakers should consider]

### Future Research Directions
- [Open questions and next steps]

---

*Document prepared by: Hayden, Stephen, Cheng, Sheena, and Daria*
