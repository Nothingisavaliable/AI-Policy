# AI Framing Annotation Codebook

You are coding sentences from national AI strategy documents. Assign **exactly one**
label to each sentence in the `gold_label` column of your `annotator_N.csv` file.

Allowed labels (type them exactly):

- `AI-friendly` — frames AI development or governance as enabling innovation,
  adoption, investment, productivity, competitiveness, flexible/light-touch
  governance, reduced regulatory burden, sandboxes, open ecosystems, or faster
  deployment.
- `AI-cautious` — frames AI governance around risk, safety, harms, restrictions,
  mandatory oversight, compliance, accountability, privacy, human rights, bias,
  fairness, or precaution.
- `mixed` — the same sentence materially contains BOTH AI-friendly and
  AI-cautious framing.
- `neutral` — descriptive or administrative text without clear AI-friendly or
  AI-cautious framing.

## Rules

1. Judge each sentence on its own, based only on what the sentence says.
2. Pick the single best label. Use `mixed` only when both framings are clearly
   present in the same sentence, not when you are unsure between two.
3. Use `neutral` for definitions, procedural notes, dates, references, and
   descriptive statements with no evaluative framing.
4. **Annotate independently.** Do not discuss with other annotators and do not
   look at any model output while coding. Your file intentionally does not show
   the model's label.
5. The sentence order is shuffled per annotator on purpose; `item_id` is the
   stable identifier used to align everyone's answers afterward.

## After everyone finishes

Put all six completed files back in this folder, keeping the names
`annotator_1.csv` … `annotator_6.csv`, then run:

```
python3 summarize_gold_annotation.py
```

It reports inter-annotator agreement (Fleiss' kappa) and writes a
majority-vote consensus gold set to `outputs/qwen_gold_labels.csv`, which the
metrics pipeline picks up automatically.
