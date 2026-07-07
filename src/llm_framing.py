from __future__ import annotations

from pathlib import Path
import json
import re
import socket
import time
import urllib.error
import urllib.request

import pandas as pd

from text_utils import split_sentences


CANONICAL_LABELS = [
    'Innovation-oriented',
    'Risk-oriented',
    'Mixed',
    'Neutral',
    'Unsure',
]

MODEL_LABEL_ALIASES = {
    'ai-friendly': 'Innovation-oriented',
    'friendly': 'Innovation-oriented',
    'innovation': 'Innovation-oriented',
    'innovation-oriented': 'Innovation-oriented',
    'innovation oriented': 'Innovation-oriented',
    'pro-innovation': 'Innovation-oriented',
    'ai-cautious': 'Risk-oriented',
    'cautious': 'Risk-oriented',
    'risk': 'Risk-oriented',
    'risk-oriented': 'Risk-oriented',
    'risk oriented': 'Risk-oriented',
    'restriction/risk-oriented': 'Risk-oriented',
    'mixed': 'Mixed',
    'neutral': 'Neutral',
    'unsure': 'Unsure',
    'uncertain': 'Unsure',
}

FRAMING_SCORE = {
    'Innovation-oriented': 1.0,
    'Risk-oriented': -1.0,
    'Mixed': 0.0,
    'Neutral': 0.0,
    'Unsure': 0.0,
}


def normalize_label(label) -> str:
    """Normalize model and human labels to one canonical label scheme."""
    if pd.isna(label):
        return 'Unsure'
    text = str(label).strip()
    if text in CANONICAL_LABELS:
        return text
    key = re.sub(r'\s+', ' ', text.lower().strip())
    return MODEL_LABEL_ALIASES.get(key, 'Unsure')


def sentence_key(sentence: str) -> str:
    """Return a stable sentence key for joining model and human labels."""
    return re.sub(r'\s+', ' ', str(sentence)).strip().casefold()


def load_gold_labels(
    path: Path | str,
    excluded_labels: list[str] | tuple[str, ...] | None = ('Unsure',),
) -> pd.DataFrame:
    """Load human gold labels used to calibrate or override LLM labels.

    By default, human consensus labels of ``Unsure`` are excluded because they
    mark ambiguous or fragmentary sentences rather than substantive framing.
    """
    df = pd.read_csv(path).copy()
    required = {'country', 'sentence', 'majority_label'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'{path} is missing required columns: {sorted(missing)}')
    df['gold_label'] = df['majority_label'].map(normalize_label)
    df['sentence_key'] = df['sentence'].map(sentence_key)
    if excluded_labels:
        excluded = {normalize_label(label) for label in excluded_labels}
        df = df[~df['gold_label'].isin(excluded)].copy()
    return df


def load_policy_sentences(
    extracted_dir: Path | str,
    countries: list[str] | None = None,
    min_chars: int = 35,
) -> pd.DataFrame:
    """Load sentence-level English analysis corpus from extracted policy text files."""
    extracted_dir = Path(extracted_dir)
    rows = []
    for path in sorted(extracted_dir.glob('*_analysis_english.txt')):
        country = path.name.removesuffix('_analysis_english.txt')
        if countries is not None and country not in countries:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        for idx, sentence in enumerate(split_sentences(text), start=1):
            if len(sentence) < min_chars:
                continue
            rows.append({
                'country': country,
                'sentence_id': f'{country}_{idx:05d}',
                'sentence': sentence,
                'sentence_key': sentence_key(sentence),
            })
    return pd.DataFrame(rows)


def make_few_shot_examples(
    gold: pd.DataFrame,
    max_examples_per_label: int = 3,
    random_state: int = 42,
) -> list[dict[str, str]]:
    """Build balanced few-shot examples from the human gold set."""
    examples = []
    for label in CANONICAL_LABELS:
        sub = gold[gold['gold_label'] == label]
        if sub.empty:
            continue
        sub = sub.sample(
            n=min(max_examples_per_label, len(sub)),
            random_state=random_state,
        )
        for _, row in sub.iterrows():
            examples.append({
                'sentence': row['sentence'],
                'label': row['gold_label'],
            })
    return examples


def build_framing_prompt(sentence: str, examples: list[dict[str, str]] | None = None) -> str:
    """Create a strict sentence-level framing prompt for local LLM classification."""
    examples = examples or []
    example_lines = []
    for example in examples:
        payload = {
            'sentence': example['sentence'],
            'label': example['label'],
        }
        example_lines.append(json.dumps(payload, ensure_ascii=False))

    examples_text = '\n'.join(example_lines) if example_lines else 'No examples provided.'
    labels = ', '.join(CANONICAL_LABELS)
    return f"""You are coding one sentence from a government AI policy document.

Choose exactly one label from this list:
{labels}

Definitions:
- Innovation-oriented: enables innovation, adoption, investment, productivity, competitiveness, flexible governance, sandboxes, open ecosystems, or faster deployment.
- Risk-oriented: emphasizes risk, safety, harms, restrictions, oversight, compliance, accountability, privacy, human rights, bias, fairness, or precaution.
- Mixed: the same sentence clearly contains both innovation-oriented and risk-oriented framing.
- Neutral: descriptive or administrative text with no clear innovation-oriented or risk-oriented framing.
- Unsure: use only when the sentence is too fragmentary or ambiguous to classify.

Human-coded examples:
{examples_text}

Return only valid JSON with this schema:
{{"label": "one label", "confidence": 0.0, "reason": "short reason"}}

Sentence:
{sentence}
"""


def call_ollama_generate(
    prompt: str,
    model: str = 'deepseek-r1:14b',
    host: str = 'http://localhost:11434',
    temperature: float = 0.0,
    timeout: int = 180,
) -> str:
    """Call a local Ollama model through the generate API."""
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': temperature},
    }
    request = urllib.request.Request(
        f'{host.rstrip("/")}/api/generate',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
    except socket.timeout as exc:
        raise TimeoutError(
            f'Ollama timed out after {timeout} seconds for model `{model}`.'
        ) from exc
    except urllib.error.URLError as exc:
        raise ConnectionError(
            'Could not reach Ollama. Start it with `ollama serve` and make sure '
            f'the model `{model}` is available.'
        ) from exc
    return data.get('response', '')


def parse_label_response(response: str) -> dict[str, object]:
    """Parse a model response into label, confidence, and reason fields."""
    text = response.strip()
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    parsed = {}
    if match:
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            parsed = {}

    label = normalize_label(parsed.get('label') if parsed else text)
    confidence = parsed.get('confidence') if parsed else pd.NA
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = pd.NA
    return {
        'model_label': label,
        'model_confidence': confidence,
        'model_reason': parsed.get('reason', '') if parsed else '',
        'raw_response': response,
    }


def classify_sentences_with_ollama(
    sentences: pd.DataFrame,
    model: str = 'deepseek-r1:14b',
    examples: list[dict[str, str]] | None = None,
    host: str = 'http://localhost:11434',
    limit: int | None = None,
    sleep_seconds: float = 0.0,
    checkpoint_path: Path | str | None = None,
    resume: bool = True,
    timeout: int = 300,
    max_retries: int = 1,
    save_errors_as_unsure: bool = True,
) -> pd.DataFrame:
    """Classify a sentence DataFrame with a local Ollama model.

    When ``checkpoint_path`` is provided, results are saved after each sentence.
    Re-running with ``resume=True`` skips sentence IDs already present in that
    checkpoint, so interrupted full-corpus runs can continue.
    """
    work = sentences.head(limit).copy() if limit else sentences.copy()
    checkpoint_path = Path(checkpoint_path) if checkpoint_path else None

    rows = []
    completed_ids = set()
    if checkpoint_path and resume and checkpoint_path.exists():
        existing = pd.read_csv(checkpoint_path)
        rows = existing.to_dict('records')
        if 'sentence_id' in existing.columns:
            completed_ids = set(existing['sentence_id'].dropna().astype(str))
        print(f'loaded checkpoint with {len(completed_ids)} completed sentences')

    remaining = work[~work['sentence_id'].astype(str).isin(completed_ids)].copy()
    total = len(work)
    done = len(completed_ids)
    print(f'classifying {len(remaining)} remaining sentences ({done}/{total} already done)')

    for i, (_, row) in enumerate(remaining.iterrows(), start=done + 1):
        prompt = build_framing_prompt(row['sentence'], examples=examples)
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                response = call_ollama_generate(prompt, model=model, host=host, timeout=timeout)
                parsed = parse_label_response(response)
                break
            except (TimeoutError, ConnectionError) as exc:
                last_error = exc
                print(f'warning: {row["sentence_id"]} failed on attempt {attempt + 1}: {exc}')
                if attempt < max_retries:
                    time.sleep(2)
        else:
            if not save_errors_as_unsure:
                raise last_error
            parsed = {
                'model_label': 'Unsure',
                'model_confidence': pd.NA,
                'model_reason': f'LLM call failed after {max_retries + 1} attempts: {last_error}',
                'raw_response': '',
            }
        rows.append({**row.to_dict(), **parsed})
        if checkpoint_path:
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(rows).to_csv(checkpoint_path, index=False)
        if sleep_seconds:
            time.sleep(sleep_seconds)
        if i % 25 == 0 or i == total:
            print(f'classified {i}/{total} sentences')
    return pd.DataFrame(rows)


def apply_human_gold_correction(
    model_labels: pd.DataFrame,
    gold: pd.DataFrame,
) -> pd.DataFrame:
    """Override exact gold-set sentences with human labels and flag corrected rows."""
    df = model_labels.copy()
    if 'sentence_key' not in df.columns:
        df['sentence_key'] = df['sentence'].map(sentence_key)
    gold_cols = ['country', 'sentence_key', 'gold_label']
    merged = df.merge(gold[gold_cols], on=['country', 'sentence_key'], how='left')
    merged['corrected_label'] = merged['gold_label'].fillna(merged['model_label'])
    merged['human_gold_override'] = merged['gold_label'].notna()
    merged['label_changed_by_human_gold'] = (
        merged['human_gold_override'] & (merged['corrected_label'] != merged['model_label'])
    )
    return merged


def evaluate_against_gold(corrected_labels: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Evaluate raw and corrected model labels on rows that have human gold labels."""
    gold_rows = corrected_labels[corrected_labels['human_gold_override']].copy()
    if gold_rows.empty:
        return {
            'metrics': pd.DataFrame(),
            'confusion': pd.DataFrame(),
        }

    raw_accuracy = (gold_rows['model_label'] == gold_rows['gold_label']).mean()
    corrected_accuracy = (gold_rows['corrected_label'] == gold_rows['gold_label']).mean()
    metrics = pd.DataFrame([
        {
            'gold_sentences': len(gold_rows),
            'raw_model_accuracy': raw_accuracy,
            'corrected_accuracy': corrected_accuracy,
            'human_overrides': int(gold_rows['label_changed_by_human_gold'].sum()),
        }
    ])
    confusion = pd.crosstab(
        gold_rows['gold_label'],
        gold_rows['model_label'],
        rownames=['gold_label'],
        colnames=['raw_model_label'],
        dropna=False,
    )
    return {'metrics': metrics, 'confusion': confusion.reset_index()}


def summarize_country_framing(labels: pd.DataFrame, label_col: str = 'corrected_label') -> pd.DataFrame:
    """Summarize corrected framing labels by country."""
    df = labels.copy()
    df['framing_score'] = df[label_col].map(FRAMING_SCORE).fillna(0.0)
    counts = (
        df.groupby(['country', label_col])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for label in CANONICAL_LABELS:
        if label not in counts.columns:
            counts[label] = 0
    totals = (
        df.groupby('country')
        .agg(
            total_sentences=('sentence', 'size'),
            net_framing_score=('framing_score', 'sum'),
            mean_framing_score=('framing_score', 'mean'),
        )
        .reset_index()
    )
    summary = counts.merge(totals, on='country', how='left')
    summary['innovation_to_risk_ratio'] = (
        (summary['Innovation-oriented'] + 0.5) / (summary['Risk-oriented'] + 0.5)
    )
    return summary.sort_values('country').reset_index(drop=True)
