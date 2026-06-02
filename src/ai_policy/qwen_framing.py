from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from collections.abc import Iterable


DEFAULT_BASE_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
DEFAULT_MODEL = 'qwen-plus'
LABELS = ('AI-friendly', 'AI-cautious', 'mixed', 'neutral')

SYSTEM_PROMPT = """You are coding national AI policy discourse at sentence level.

Classify each sentence into exactly one framing label:
- AI-friendly: frames AI development or governance as enabling innovation, adoption, investment, productivity, competitiveness, flexible governance, reduced regulatory burden, sandboxes, open ecosystems, or faster deployment.
- AI-cautious: frames AI governance around risk, safety, harms, restrictions, mandatory oversight, compliance, accountability, privacy, human rights, bias, fairness, or precaution.
- mixed: the same sentence materially contains both AI-friendly and AI-cautious framing.
- neutral: descriptive or administrative text without clear AI-friendly or AI-cautious framing.

Return only valid JSON with this schema:
{"label":"AI-friendly|AI-cautious|mixed|neutral","confidence":0.0,"rationale":"brief reason"}
Confidence must be between 0 and 1. Keep rationale under 25 words."""


def parse_model_json(content: str) -> dict:
    text = content.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

    match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if not match:
        raise ValueError(f'No JSON object found in model response: {content[:200]}')

    parsed = json.loads(match.group(0))
    label = str(parsed.get('label', '')).strip()
    if label not in LABELS:
        raise ValueError(f'Unexpected label {label!r}')

    confidence = float(parsed.get('confidence', 0.0))
    confidence = max(0.0, min(confidence, 1.0))
    rationale = str(parsed.get('rationale', '')).strip()
    return {'label': label, 'confidence': confidence, 'rationale': rationale}


def classify_sentence(
    sentence: str,
    *,
    api_key: str,
    model: str = DEFAULT_MODEL,
    base_url: str = DEFAULT_BASE_URL,
    temperature: float = 0.0,
    max_retries: int = 3,
    timeout: int = 60,
) -> dict:
    url = base_url.rstrip('/') + '/chat/completions'
    payload = {
        'model': model,
        'temperature': temperature,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Sentence:\n{sentence}'},
        ],
    }
    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    for attempt in range(1, max_retries + 1):
        request = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode('utf-8')
            completion = json.loads(body)
            content = completion['choices'][0]['message']['content']
            return parse_model_json(content)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as error:
            if attempt == max_retries:
                raise RuntimeError(f'Qwen request failed after {max_retries} attempts: {error}') from error
            time.sleep(min(2 ** attempt, 10))

    raise RuntimeError('unreachable')


def sentence_score(label: str, confidence: float) -> tuple[float, float]:
    if label == 'AI-friendly':
        return confidence, 0.0
    if label == 'AI-cautious':
        return 0.0, confidence
    if label == 'mixed':
        return confidence * 0.5, confidence * 0.5
    return 0.0, 0.0


def summarize_labels(
    rows: Iterable[dict],
    *,
    country: str,
    sources: Iterable[str],
    word_count: int,
) -> dict:
    rows = list(rows)
    friendly_score = 0.0
    cautious_score = 0.0
    label_counts = {label: 0 for label in LABELS}

    for row in rows:
        label = row['Label']
        confidence = float(row['Confidence'])
        label_counts[label] += 1
        friendly, cautious = sentence_score(label, confidence)
        friendly_score += friendly
        cautious_score += cautious

    words = max(int(word_count), 1)
    friendly_per_1000 = friendly_score / words * 1000
    cautious_per_1000 = cautious_score / words * 1000
    total = friendly_score + cautious_score
    return {
        'Country': country,
        'Sources': '; '.join(sources),
        'Word count': words,
        'Sentence count': len(rows),
        'AI-friendly sentence count': label_counts['AI-friendly'],
        'AI-cautious sentence count': label_counts['AI-cautious'],
        'Mixed sentence count': label_counts['mixed'],
        'Neutral sentence count': label_counts['neutral'],
        'AI-friendly score': round(friendly_score, 3),
        'AI-cautious score': round(cautious_score, 3),
        'AI-friendly per 1000 words': round(friendly_per_1000, 3),
        'AI-cautious per 1000 words': round(cautious_per_1000, 3),
        'Net AI-friendly framing': round(friendly_per_1000 - cautious_per_1000, 3),
        'Net AI-cautious framing': round(cautious_per_1000 - friendly_per_1000, 3),
        'AI-friendly share': round(friendly_score / total, 3) if total else 0,
    }
