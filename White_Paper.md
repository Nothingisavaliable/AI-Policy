# White Paper: AI’s Relationship with Economic Freedom


## Executive Summary:


*This research finds no positive correlations between a nation’s AI policy discourse, its institutional environment, and its economic maturity. On the contrary, economically free countries are associated with more risk-oriented framing of AI risk governance, instead of innovation-friendly framing.* 

## Introduction
   Following generative AI’s rapid emergence in 2022, global governance has split between prioritizing innovation and investment versus safety and regulatory oversight. This exploratory study examines the determinants of these divergent approaches, evaluating whether a nation's AI policy discourse is shaped by its institutional environment (Economic Freedom) and ecosystem maturity (AI Vibrancy).

## Overview

   AI Vibrancy and Economic Freedom and serve as the independent variables in this analysis due to their reflection of two complementary dimensions of national AI ecosystems: overarching institutional orientation and technological capacity. First, AI Vibrancy represents the AI ecosystem present in each country. This variable reflects national progress in AI development, in areas including research output, talent, and capital.  First, Economic Freedom represents the institutional dimension. This represents whether a government inherently trusts market forces to guide innovation, likely resulting in regulatory frameworks acting as market referees, or whether it substitutes emphasizes state intervention, more likely correlating with restrictive, risk-averse policy postures. Meanwhile, our dependent variable is policy rhetoric, dividing into either innovation-oriented or risk-oriented rhetoric. All of these metrics are examined with quantitative methods, to ensure concrete, reproducible research.

## Research Question

How do variations in economic freedom and AI vibrancy shape the dominant framing embedded in national discourse, and how do these relationships vary across G7 countries and China? 

## Hypotheses

- **H1**: Countries with higher Stanford AI Vibrancy scores will exhibit more innovation-oriented rhetoric in their national policy documents.
- **H2**: Countries with lower Stanford AI Vibrancy scores will exhibit more risk-oriented rhetoric in their national policy documents.
- **H3**: Countries whose AI regulatory discourse is more positive and innovation-oriented will exhibit higher economic freedom scores.
- **H4**: Countries whose AI regulatory discourse is more negative and risk-oriented will exhibit lower economic freedom scores. 

## Methodology
   
	Using computational text analysis, this research evaluated national AI strategy documents from the G7 nations and China to quantify their reliance on innovation versus risk-oriented framing. These linguistic measures were then cross-checked against the Heritage Foundation Index of Economic Freedom and Stanford AI Vibrancy scores using correlation and regression analyses.
	
	Accordingly, we measured AI Vibrancy, Economic Freedom, and Rhetoric using concrete qualitative methods. First, AI Vibrancy, which was used to reflect the strength and maturity of each country’s AI ecosystem, was measured through the Stanford AI Index AI Vibrancy country scores. Second, Economic Freedom, the measure of state intervention, was measured with the Heritage Foundation Index of Economic Freedom. The analysis used the latest available index year in the project panel, which is 2026 in the current dataset. Third, in relation to Rhetoric, the authors conducted their own data analysis, treating AI regulatory discourse as a measurable policy signal. Policy documents from each of the G7 nations and China were chosen, with sentences assigned to one of five labels, reflecting degrees of innovation vs. risk-orientations.While the primary substantive contrast was tested between innovation-oriented and risk-oriented framing, the inclusion of mixed and neutral labels was done to prevent the model from forcing ambiguous or descriptive sentences into substantive categories.
	
	In relation to the workflow, DeepSeek through Ollama was utilized. The model classified each sentence independently, in order to reduce cross-sentence leakage, and make each label auditable at the sentence level. And, in order to enhance accuracy, human calibration was a central quality-control step, being designed to avoid blindly trusting LLM output. Human annotations were used both to guide the model through few-shot examples, and to correct exact matched sentences in the final output.

## Key Findings

	Initial findings seemed to disprove all of this study’s hypotheses, indicating no association between rhetoric and AI Vibrancy, and showing that Economic Freedom actually had an unexpected, moderate inverse relationship with innovation framing. However, upon further study, this rejection of the hypotheses has additional nuance.

	First, in relation to Hypotheses 1 and 2, which AI Vibrancy and Rhetoric, the results initially appeared to show no clear relationship. However, upon an outlier check, the United States was found to skew the data: excluding the U.S. showed a clear positive correlation between innovation-friendly rhetoric and AI Vibrancy, with the opposite true for risk-oriented. A possible explanation for the U.S. acting as an outlier is the rapid development of AI infrastructure: with public scrutiny and the threat of lawsuits encouraging the writing of more cautious policy language. Thus, Hypothesis 1 and 2 were supported with the exclusion of the United States.
	
	In relation to Hypothesis 3 and 4, for Economic Freedom and Rhetoric, our suppositions were not supported. Further, the opposite relationship appears to be true for innovation-oriented rhetoric: the more economically free a country, the more text it dedicates to risk-oriented rhetoric. This may be due to the role of governance in each country. For example, in countries with higher economic freedom scores, the government may act as a regulatory referee, allowing the private sector to innovate, and focusing its efforts on stipulating the “rules of the game.” Meanwhile, in countries with lower economic freedom scores, as the government is acting as the central innovative actor, it refrains from limiting its own actions, with policies acting as promotional, general blueprints. 
In sum, this study indicates that while AI Vibrancy and Rhetoric may have a positive, correlative relationship, Economic Freedom and Rhetoric may have an inverted, negative relationship. These patterns suggest that a government's communication strategy may be driven less by its underlying economic institutions and more by dominant strategic objectives, such as industrial policy and national development priorities.


## Limitations and Further Research

 	There are several possible limitations to our research, as well as areas that could be expanded upon by future researchers. 
	
	In relation to limitations, there are several points that may qualify the findings of this research. First, as the sample only includes eight countries (G7 +China) these results were highly sensitive to outliers, as discussed with the vibrancy finding. Second, our design is correlational, not causal: framing could shape vibrancy (or vice versa), or both could stem from a confounding variable, such as GDP, or a political system. Third, several G7 members also share EU/G7 governance frameworks, so their documents are not fully independent observations. Finally, "innovation" vs. "risk" coding involved interpretive judgment without inter-coder reliability checks, and index scores are single-year snapshots matched to multi-year spanning documents.
	
	In relation to future research, there are three main aspects which could be expanded. First, the sample could be expanded to include OECD or G20 countries, improving statistical weight, and for testing whether US/China patterns are genuine outliers. Second, a longitudinal design could be utilized to track framing changes over time alongside shifting vibrancy/freedom scores, enabling causal inference. Third, one could test the proposed mechanisms directly, by treating items such as litigation volume, public controversy, state industrial-policy activity as explicit variables. Fourth, there could be a strengthening of the text analysis, with multiple coders or a validated classifier applied to original-language documents. Alternatively, one could move beyond the innovation/risk binary to include the "capacity-building" framing for analysis.

## Conclusion

	This study demonstrates the utility of pairing computational text analysis with comparative policy indicators. While not all hypotheses were supported, the findings suggest that research into diverging global AI governance must move beyond traditional institutional metrics, explicitly incorporating geopolitical context, state capacity, and national security considerations.



