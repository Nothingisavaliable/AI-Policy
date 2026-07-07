from pathlib import Path

import pandas as pd

from common import COUNTRIES, COUNTRY_ALIASES, TARGET_COUNTRIES


def read_csv_safely(path: Path) -> pd.DataFrame:
    """Read CSV with encoding fallback."""
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='latin1')


def find_countries_in_file(csv_path: Path, target_countries=TARGET_COUNTRIES) -> list:
    """Return the target countries that appear in a CSV file."""
    try:
        text = csv_path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return []

    found = []
    for canonical, aliases in target_countries.items():
        for alias in aliases:
            if alias in text:
                found.append(canonical)
                break
    return found


def get_file_metadata(csv_path: Path) -> dict:
    """Return row, column, and column-name metadata for a CSV file."""
    try:
        df = read_csv_safely(csv_path)
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': ', '.join(map(str, df.columns)),
        }
    except Exception as exc:
        return {'rows': None, 'columns': None, 'column_names': f'ERROR: {exc}'}


def generate_markdown_summary(df: pd.DataFrame, min_country_count: int) -> str:
    lines = [
        '# G7 + China AI Datasets',
        '',
        'Datasets from the Stanford AI Index 2026 public data that contain at least '
        f'{min_country_count} of the G7 + China countries.',
        '',
        '**G7 countries**: United States, United Kingdom, France, Germany, Italy, Japan, Canada  ',
        '**Plus**: China',
        '',
        '---',
        '',
    ]

    for chapter in sorted(df['chapter'].unique()):
        sub = df[df['chapter'] == chapter].sort_values('country_count', ascending=False)
        lines.append(f'## {chapter} ({len(sub)} datasets)')
        lines.append('')
        lines.append('| Figure | Country Count | Columns |')
        lines.append('|--------|---------------|---------|')
        for _, row in sub.iterrows():
            cols = str(row['column_names']).replace('|', '\\|')
            lines.append(f"| {row['figure']} | {row['country_count']} | {cols} |")
        lines.append('')

    return '\n'.join(lines)


def to_number(value):
    """Coerce a value to float, stripping percentages and thousands separators."""
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(',', '').rstrip('%').strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_figure(figure_id, dataset_index: pd.DataFrame, repo_root: Path) -> pd.DataFrame:
    """Load a Stanford AI Index CSV by figure id."""
    match = dataset_index[dataset_index['figure'] == figure_id]
    if len(match) == 0:
        raise ValueError(f'{figure_id} not in g7_china_datasets.csv')
    return read_csv_safely(repo_root / match.iloc[0]['relative_path'])


def extract_g7_china(df: pd.DataFrame, country_col: str, value_col: str) -> dict:
    """Return one float per G7+China country, using 0.0 when a country is missing."""
    df = df.copy()
    df[country_col] = df[country_col].replace(COUNTRY_ALIASES)
    sub = df[df[country_col].isin(COUNTRIES)]
    return {
        country: to_number(sub.loc[sub[country_col] == country, value_col].iloc[0])
        if (sub[country_col] == country).any() else 0.0
        for country in COUNTRIES
    }
