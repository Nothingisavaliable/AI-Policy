from collections import Counter
from html import escape
from pathlib import Path
import re
import unicodedata


def extract_pdf_text(path: Path) -> str:
    import pdfplumber

    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or '')
    return unicodedata.normalize('NFKC', '\n'.join(pages))


def word_tokenize(text: str) -> list:
    """Lowercase Latin tokens plus CJK character tokens for multilingual normalization."""
    latin_tokens = re.findall(r"[a-zA-Zà-ÿÀ-ÝäöüÄÖÜß']{3,}", text.lower())
    cjk_tokens = re.findall(r'[\u4e00-\u9fff]', text)
    return latin_tokens + cjk_tokens


def cjk_ratio(text: str) -> float:
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    latin = len(re.findall(r'[A-Za-z]', text))
    return cjk / max(cjk + latin, 1)


def split_translation_units(text: str, max_chars: int = 700) -> list:
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n|(?<=[。！？])', text) if p.strip()]
    units = []
    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            units.append(paragraph)
            continue
        for start in range(0, len(paragraph), max_chars):
            units.append(paragraph[start:start + max_chars])
    return units


def load_nllb(model_name: str, source_lang: str):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch

    tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=source_lang)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = model.to(device)
    return tokenizer, model, device


def translate_units_nllb(
    units,
    tokenizer,
    model,
    device,
    target_lang: str,
    cjk_ratio_threshold: float = 0.20,
    max_new_tokens: int = 512,
):
    translated = []
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_lang)

    for i, unit in enumerate(units, start=1):
        if cjk_ratio(unit) < cjk_ratio_threshold:
            translated.append(unit)
            continue

        inputs = tokenizer(unit, return_tensors='pt', truncation=True, max_length=1024).to(device)
        generated = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_new_tokens=max_new_tokens,
            num_beams=4,
        )
        translated.append(tokenizer.batch_decode(generated, skip_special_tokens=True)[0])

        if i % 10 == 0:
            print(f'  translated {i}/{len(units)} units')

    return translated


def top_words(text: str, stopwords, n: int = 25):
    tokens = [token for token in word_tokenize(text) if token not in stopwords]
    return Counter(tokens).most_common(n)


def count_theme(text: str, keywords) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(keyword) for keyword in keywords)


def count_exact_keyword(text: str, keyword: str) -> int:
    """Count case-insensitive whole-word Latin keywords and exact CJK phrases."""
    if re.search(r'[\u4e00-\u9fff]', keyword):
        return text.count(keyword)
    pattern = rf'\b{re.escape(keyword.lower())}\b'
    return len(re.findall(pattern, text.lower()))


def split_sentences(text: str) -> list:
    cleaned = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?。！？])\s+', cleaned)
    return [sentence.strip() for sentence in sentences if len(sentence.strip()) > 20]


def highlight_keyword(sentence: str, keyword: str) -> str:
    escaped_sentence = escape(sentence)
    pattern = re.compile(rf'\b({re.escape(keyword)})\b', flags=re.IGNORECASE)
    return pattern.sub(r'<mark>\1</mark>', escaped_sentence)


def keyword_sentence_table_html(rows) -> str:
    table_rows = []
    for _, row in rows.iterrows():
        highlighted = highlight_keyword(row['Sentence'], row['Keyword'])
        table_rows.append(
            '<tr>'
            f'<td>{escape(row["Country"])}</td>'
            f'<td>{escape(row["Framing"])}</td>'
            f'<td>{escape(row["Keyword"])}</td>'
            f'<td>{highlighted}</td>'
            '</tr>'
        )

    return f"""
    <style>
      .sentence-table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
      .sentence-table th, .sentence-table td {{ border: 1px solid #ddd; padding: 7px; vertical-align: top; }}
      .sentence-table th {{ background: #f3f4f6; text-align: left; }}
      .sentence-table mark {{ background: #fff3a3; padding: 0 2px; }}
    </style>
    <table class="sentence-table">
      <thead><tr><th>Country</th><th>Framing</th><th>Keyword</th><th>Sentence</th></tr></thead>
      <tbody>{''.join(table_rows)}</tbody>
    </table>
    """


def filter_keyword_sentences(matches, country='All', framing='All', keyword='All', max_results=25):
    df = matches.copy()
    if country != 'All':
        df = df[df['Country'] == country]
    if framing != 'All':
        df = df[df['Framing'] == framing]
    if keyword != 'All':
        df = df[df['Keyword'] == keyword]
    return df.head(max_results).reset_index(drop=True)
