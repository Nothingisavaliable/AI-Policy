from __future__ import annotations

import csv
import html
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


COUNTRIES = [
    'United States',
    'China',
    'United Kingdom',
    'France',
    'Germany',
    'Italy',
    'Japan',
    'Canada',
]

PDF_SOURCES = {
    'Canada': ['CA_National_AI_Strategy_ocr.pdf'],
    'China': [],
    'United Kingdom': ['UK_National_AI_Strategy_ocr.pdf'],
    'France': ['FR__National_AI_Strategy.pdf', 'FR_National_AI_Strategy_2.pdf'],
    'Germany': ['DE_National_AI_Strategy.pdf'],
    'Italy': ['IT_National_AI_Strategy.pdf'],
    'Japan': ['JP_National_AI_Strategy_ocr.pdf'],
    'United States': ['US_National_AI_Strategy.pdf'],
}


@dataclass(frozen=True)
class Rule:
    category: str
    label: str
    pattern: str
    weight: float


FRIENDLY_RULES = [
    Rule(
        'deregulatory or flexible governance',
        'reduce regulatory burdens',
        r'\b(reduc(?:e|ing)|remov(?:e|ing)|lower(?:ing)?|cut(?:ting)?|eas(?:e|ing)|simplif(?:y|ying)|streamlin(?:e|ing)|eliminat(?:e|ing))\b.{0,80}\b(regulation|regulatory|rules?|barriers?|burdens?|red tape|compliance|constraints?)\b',
        2.5,
    ),
    Rule(
        'deregulatory or flexible governance',
        'anti-overregulation context',
        r'\b(onerous regulation|overregulation|over-regulation|burdensome regulation|red tape|restricting ai development|regulatory barriers?)\b.{0,120}\b(stifl(?:e|ing)|hinder(?:ing)?|paralyz(?:e|ing)|hold back|barrier|burden|benefit incumbents|slow(?:ing)?)\b',
        2.4,
    ),
    Rule(
        'deregulatory or flexible governance',
        'flexible/proportionate/risk-based regulation',
        r'\b(light-touch|proportionate|flexible|risk-based|innovation-friendly|pro-innovation|agile)\b.{0,80}\b(regulation|regulatory|governance|framework|approach)\b',
        2.0,
    ),
    Rule(
        'deregulatory or flexible governance',
        'regulatory sandbox',
        r'\b(regulatory sandbox|sandbox(?:es)?|testbed(?:s)?|experimentation space)\b',
        1.8,
    ),
    Rule(
        'innovation and adoption promotion',
        'promote AI innovation/adoption',
        r'\b(promot(?:e|ing)|support(?:ing)?|foster(?:ing)?|encourag(?:e|ing)|accelerat(?:e|ing)|facilitat(?:e|ing)|enable|enabling|stimulat(?:e|ing)|boost(?:ing)?)\b.{0,80}\b(ai|artificial intelligence|innovation|adoption|deployment|diffusion|uptake|commerciali[sz]ation)\b',
        2.0,
    ),
    Rule(
        'investment and competitiveness',
        'investment/competitiveness/growth',
        r'\b(invest(?:ment|ing)?|fund(?:ing)?|capital|competitiveness|competitive|growth|productivity|leadership|scale[- ]?up|startup|entrepreneurship)\b',
        1.0,
    ),
    Rule(
        'open ecosystem and market access',
        'open data/infrastructure/ecosystem',
        r'\b(open data|open source|interoperab(?:le|ility)|shared infrastructure|public-private partnership|ecosystem|market access|data sharing)\b',
        1.2,
    ),
]

CAUTIOUS_RULES = [
    Rule(
        'regulation as necessary',
        'regulation required or necessary',
        r'\b(need|needs|needed|necessary|essential|required|requires?|must|should|shall|obligation|obligatory)\b.{0,80}\b(regulation|regulatory|rules?|law|laws|governance|oversight|supervision|control|compliance)\b',
        2.5,
    ),
    Rule(
        'restrictive governance',
        'restrict/prohibit/control AI',
        r'\b(restrict(?:ion|ive|ed|ing)?|prohibit(?:ion|ed|ing)?|ban(?:ned|ning)?|limit(?:ation|ed|ing)?|control(?:led|ling)?|constrain(?:t|ed|ing)?)\b.{0,80}\b(ai|artificial intelligence|system|systems|use|deployment|application)\b',
        2.2,
    ),
    Rule(
        'mandatory accountability',
        'mandatory compliance/oversight',
        r'\b(mandatory|binding|strict|enforce(?:d|ment)?|certification|audit(?:ing)?|approval|licen[cs]ing)\b.{0,80}\b(compliance|oversight|accountability|transparency|assessment|requirements?|standards?|obligations?)\b',
        1.9,
    ),
    Rule(
        'risk and harm emphasis',
        'risk/safety/harm framing',
        r'\b(risk|risks|safety|safe|harm|harms|threat|threats|misuse|abuse|vulnerabilit(?:y|ies)|danger|dangerous)\b',
        1.0,
    ),
    Rule(
        'rights and protection emphasis',
        'rights/privacy/protection framing',
        r'\b(privacy|fundamental rights|human rights|data protection|consumer protection|rights protection|non-discrimination|bias|fairness|trustworthy|responsible ai)\b',
        1.1,
    ),
    Rule(
        'precautionary framing',
        'precaution before deployment',
        r'\b(precautionary|before deployment|prior authori[sz]ation|ex ante|high-risk|unacceptable risk)\b',
        1.6,
    ),
]


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / 'data').is_dir():
            return path
    raise FileNotFoundError('Could not find repository root containing data/')


def pdftotext(path: Path) -> str:
    result = subprocess.run(
        ['pdftotext', str(path), '-'],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors='replace',
    )
    return result.stdout


def load_country_text(repo_root: Path, country: str) -> tuple[str, list[str]]:
    pdf_dir = repo_root / 'data' / 'pdf' / 'AI Policy'
    extracted_dir = pdf_dir / '_extracted'

    if country == 'China':
        translated = extracted_dir / 'China_analysis_english.txt'
        if translated.exists():
            return translated.read_text(encoding='utf-8'), [translated.name]

    parts = []
    sources = []
    for pdf_name in PDF_SOURCES[country]:
        pdf_path = pdf_dir / pdf_name
        if not pdf_path.exists():
            continue
        try:
            text = pdftotext(pdf_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            fallback = extracted_dir / f'{country}_analysis_english.txt'
            if fallback.exists():
                text = fallback.read_text(encoding='utf-8')
            else:
                text = ''
        if text.strip():
            parts.append(f'\n\n--- Source: {pdf_name} ---\n\n{text}')
            sources.append(pdf_name)

    if parts:
        return '\n'.join(parts), sources

    fallback = extracted_dir / f'{country}_analysis_english.txt'
    if fallback.exists():
        return fallback.read_text(encoding='utf-8'), [fallback.name]

    raise FileNotFoundError(f'No text source found for {country}')


def split_sentences(text: str) -> list[str]:
    cleaned = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?。！？])\s+', cleaned)
    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 30 and '.....' not in sentence
    ]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", text))


def score_sentence(sentence: str, rules: list[Rule]) -> list[dict]:
    matches = []
    for rule in rules:
        for match in re.finditer(rule.pattern, sentence, flags=re.IGNORECASE):
            matches.append({
                'Category': rule.category,
                'Rule': rule.label,
                'Matched text': match.group(0)[:220],
                'Weight': rule.weight,
            })
    return matches


def analyze_country(country: str, text: str, sources: list[str]) -> tuple[dict, list[dict], dict[str, dict[str, float]]]:
    friendly_score = 0.0
    cautious_score = 0.0
    friendly_sentences = set()
    cautious_sentences = set()
    sentence_rows = []
    category_scores: dict[str, dict[str, float]] = {}

    for i, sentence in enumerate(split_sentences(text), start=1):
        friendly_matches = score_sentence(sentence, FRIENDLY_RULES)
        cautious_matches = score_sentence(sentence, CAUTIOUS_RULES)
        anti_overregulation = any(match['Rule'] == 'anti-overregulation context' for match in friendly_matches)
        if anti_overregulation:
            cautious_matches = [
                match for match in cautious_matches
                if match['Category'] not in {'restrictive governance', 'risk and harm emphasis'}
            ]

        for framing, matches in [('AI-friendly', friendly_matches), ('AI-cautious', cautious_matches)]:
            for match in matches:
                score = float(match['Weight'])
                if framing == 'AI-friendly':
                    friendly_score += score
                    friendly_sentences.add(i)
                else:
                    cautious_score += score
                    cautious_sentences.add(i)

                category = match['Category']
                category_scores.setdefault(category, {'AI-friendly': 0.0, 'AI-cautious': 0.0})
                category_scores[category][framing] += score

                sentence_rows.append({
                    'Country': country,
                    'Framing': framing,
                    'Category': category,
                    'Rule': match['Rule'],
                    'Weight': score,
                    'Matched text': match['Matched text'],
                    'Sentence': sentence,
                })

    words = max(word_count(text), 1)
    friendly_per_1000 = friendly_score / words * 1000
    cautious_per_1000 = cautious_score / words * 1000
    total = friendly_score + cautious_score
    summary = {
        'Country': country,
        'Sources': '; '.join(sources),
        'Word count': words,
        'AI-friendly sentence count': len(friendly_sentences),
        'AI-cautious sentence count': len(cautious_sentences),
        'AI-friendly score': round(friendly_score, 2),
        'AI-cautious score': round(cautious_score, 2),
        'AI-friendly per 1000 words': round(friendly_per_1000, 2),
        'AI-cautious per 1000 words': round(cautious_per_1000, 2),
        'Net AI-friendly framing': round(friendly_per_1000 - cautious_per_1000, 2),
        'Net AI-cautious framing': round(cautious_per_1000 - friendly_per_1000, 2),
        'AI-friendly share': round(friendly_score / total, 3) if total else 0,
    }
    return summary, sentence_rows, category_scores


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bar_svg(path: Path, title: str, rows: list[dict], keys: list[str], colors: list[str], width=1100, row_height=42) -> None:
    margin_left = 230
    margin_right = 60
    margin_top = 70
    height = margin_top + row_height * len(rows) + 70
    plot_width = width - margin_left - margin_right
    max_value = max(abs(float(row[key])) for row in rows for key in keys) or 1
    zero_x = margin_left if min(float(row[key]) for row in rows for key in keys) >= 0 else margin_left + plot_width / 2
    scale = (plot_width if zero_x == margin_left else plot_width / 2) / max_value

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;font-size:13px}.title{font-size:20px;font-weight:700}.axis{stroke:#777;stroke-width:1}.grid{stroke:#ddd;stroke-width:1}.label{font-weight:600}</style>',
        f'<text class="title" x="{width/2}" y="32" text-anchor="middle">{html.escape(title)}</text>',
    ]
    svg.append(f'<line class="axis" x1="{zero_x:.1f}" y1="{margin_top-20}" x2="{zero_x:.1f}" y2="{height-45}"/>')

    for i, row in enumerate(rows):
        y_base = margin_top + i * row_height
        svg.append(f'<text class="label" x="{margin_left-12}" y="{y_base+22}" text-anchor="end">{html.escape(row["Country"])}</text>')
        for j, key in enumerate(keys):
            value = float(row[key])
            bar_h = 15
            y = y_base + 4 + j * 18
            if value >= 0:
                x = zero_x
                bar_w = value * scale
            else:
                x = zero_x + value * scale
                bar_w = -value * scale
            svg.append(f'<rect x="{x:.1f}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" fill="{colors[j]}"/>')
            label_x = x + bar_w + 5 if value >= 0 else x - 5
            anchor = 'start' if value >= 0 else 'end'
            svg.append(f'<text x="{label_x:.1f}" y="{y+12}" text-anchor="{anchor}">{value:.2f}</text>')

    legend_x = margin_left
    legend_y = height - 25
    for j, key in enumerate(keys):
        svg.append(f'<rect x="{legend_x + j*250}" y="{legend_y-12}" width="14" height="14" fill="{colors[j]}"/>')
        svg.append(f'<text x="{legend_x + j*250 + 20}" y="{legend_y}">{html.escape(key)}</text>')
    svg.append('</svg>')
    path.write_text('\n'.join(svg), encoding='utf-8')


def markdown_report(path: Path, rows: list[dict]) -> None:
    sorted_rows = sorted(rows, key=lambda row: row['Net AI-friendly framing'], reverse=True)
    lines = [
        '# Semantic AI Framing Analysis',
        '',
        'This analysis scores sentence-level context in national AI strategy documents for innovation-friendly versus AI-cautious framing.',
        '',
        'Innovation-friendly examples include reducing regulatory barriers, flexible or risk-based governance, regulatory sandboxes, AI adoption, investment, productivity, and competitiveness.',
        '',
        'AI-cautious examples include regulation framed as necessary, mandatory oversight, restrictions, compliance obligations, risks, safety, harms, privacy, and rights protection.',
        '',
        '| Rank | Country | AI-friendly / 1000 words | AI-cautious / 1000 words | Net AI-friendly | Friendly share |',
        '| --- | --- | ---: | ---: | ---: | ---: |',
    ]
    for rank, row in enumerate(sorted_rows, start=1):
        lines.append(
            f'| {rank} | {row["Country"]} | {row["AI-friendly per 1000 words"]} | '
            f'{row["AI-cautious per 1000 words"]} | {row["Net AI-friendly framing"]} | '
            f'{row["AI-friendly share"]} |'
        )
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    repo_root = find_repo_root(Path.cwd())
    outputs = repo_root / 'outputs'
    outputs.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    sentence_rows = []
    category_rows = []

    for country in COUNTRIES:
        text, sources = load_country_text(repo_root, country)
        summary, rows, category_scores = analyze_country(country, text, sources)
        summary_rows.append(summary)
        sentence_rows.extend(rows)
        words = max(summary['Word count'], 1)
        for category, scores in category_scores.items():
            category_rows.append({
                'Country': country,
                'Category': category,
                'AI-friendly score': round(scores.get('AI-friendly', 0.0), 2),
                'AI-cautious score': round(scores.get('AI-cautious', 0.0), 2),
                'AI-friendly per 1000 words': round(scores.get('AI-friendly', 0.0) / words * 1000, 2),
                'AI-cautious per 1000 words': round(scores.get('AI-cautious', 0.0) / words * 1000, 2),
            })

    summary_rows = sorted(summary_rows, key=lambda row: row['Net AI-friendly framing'], reverse=True)

    write_csv(
        outputs / 'semantic_ai_framing_summary.csv',
        summary_rows,
        [
            'Country', 'Sources', 'Word count', 'AI-friendly sentence count', 'AI-cautious sentence count',
            'AI-friendly score', 'AI-cautious score', 'AI-friendly per 1000 words',
            'AI-cautious per 1000 words', 'Net AI-friendly framing', 'Net AI-cautious framing',
            'AI-friendly share',
        ],
    )
    write_csv(
        outputs / 'semantic_ai_framing_sentence_matches.csv',
        sentence_rows,
        ['Country', 'Framing', 'Category', 'Rule', 'Weight', 'Matched text', 'Sentence'],
    )
    write_csv(
        outputs / 'semantic_ai_framing_category_breakdown.csv',
        category_rows,
        ['Country', 'Category', 'AI-friendly score', 'AI-cautious score', 'AI-friendly per 1000 words', 'AI-cautious per 1000 words'],
    )

    bar_svg(
        outputs / 'semantic_ai_friendly_vs_cautious.svg',
        'Semantic AI Framing: Friendly vs Cautious Mentions per 1,000 Words',
        summary_rows,
        ['AI-friendly per 1000 words', 'AI-cautious per 1000 words'],
        ['#2ca02c', '#d62728'],
    )
    bar_svg(
        outputs / 'semantic_net_ai_friendly_framing.svg',
        'Net AI-Friendly Framing per 1,000 Words',
        summary_rows,
        ['Net AI-friendly framing'],
        ['#1f77b4'],
    )
    markdown_report(outputs / 'semantic_ai_framing_overview.md', summary_rows)

    print('Saved semantic framing outputs:')
    for name in [
        'semantic_ai_framing_summary.csv',
        'semantic_ai_framing_sentence_matches.csv',
        'semantic_ai_framing_category_breakdown.csv',
        'semantic_ai_friendly_vs_cautious.svg',
        'semantic_net_ai_friendly_framing.svg',
        'semantic_ai_framing_overview.md',
    ]:
        print(f' - {outputs / name}')


if __name__ == '__main__':
    main()
