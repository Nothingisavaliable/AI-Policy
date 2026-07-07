from pathlib import Path

import pandas as pd


ANNOTATION_KEY_COLUMNS = ['item_id', 'country', 'sentence']
LABEL_COLUMN = 'gold_label'
REFERENCE_LABEL_COLUMN = 'model_label_reference'
MODEL_TO_HUMAN_LABEL = {
    'AI-friendly': 'Innovation-oriented',
    'AI-cautious': 'Risk-oriented',
    'mixed': 'Mixed',
    'neutral': 'Neutral',
}


def load_human_framing_annotations(data_dir: Path | str) -> pd.DataFrame:
    """Load all annotator CSV files from a directory into one long DataFrame."""
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob('annotator_*.csv'))
    if not files:
        raise FileNotFoundError(f'No annotator_*.csv files found in {data_dir}')

    frames = []
    for path in files:
        df = pd.read_csv(path)
        missing = set(ANNOTATION_KEY_COLUMNS + [LABEL_COLUMN, 'annotator']) - set(df.columns)
        if missing:
            raise ValueError(f'{path} is missing required columns: {sorted(missing)}')

        df = df.copy()
        df['source_file'] = path.name
        df[LABEL_COLUMN] = df[LABEL_COLUMN].replace('', pd.NA)
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def make_label_matrix(
    annotations: pd.DataFrame,
    key_columns: list[str] | None = None,
    label_column: str = LABEL_COLUMN,
) -> pd.DataFrame:
    """Return one row per sentence with one label column per annotator."""
    key_columns = key_columns or ANNOTATION_KEY_COLUMNS
    deduped = annotations.drop_duplicates(key_columns + ['annotator'], keep='first')
    matrix = deduped.pivot(index=key_columns, columns='annotator', values=label_column)
    matrix.columns = [f'annotator_{col}_label' for col in matrix.columns]
    return matrix.reset_index()


def add_agreement_columns(label_matrix: pd.DataFrame, label_prefix: str = 'annotator_') -> pd.DataFrame:
    """Add agreement diagnostics to a sentence-level label matrix."""
    label_columns = [
        col for col in label_matrix.columns
        if col.startswith(label_prefix) and col.endswith('_label')
    ]
    if not label_columns:
        raise ValueError('No annotator label columns found.')

    rows = []
    for _, row in label_matrix.iterrows():
        labels = [row[col] for col in label_columns if pd.notna(row[col])]
        counts = pd.Series(labels, dtype='object').value_counts()
        majority_label = counts.index[0] if len(counts) else pd.NA
        majority_count = int(counts.iloc[0]) if len(counts) else 0
        rows.append({
            'n_annotators': len(label_columns),
            'n_valid_labels': len(labels),
            'majority_label': majority_label,
            'majority_count': majority_count,
            'agreement_share': majority_count / len(label_columns),
            'full_agreement': len(labels) == len(label_columns) and majority_count == len(label_columns),
        })

    agreement = pd.DataFrame(rows)
    return pd.concat([label_matrix.reset_index(drop=True), agreement], axis=1)


def filter_agreed_sentences(
    annotations: pd.DataFrame,
    min_agreement_share: float = 1.0,
    key_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Keep sentences whose annotators agree at or above the requested share."""
    matrix = make_label_matrix(annotations, key_columns=key_columns)
    agreed = add_agreement_columns(matrix)
    return agreed[agreed['agreement_share'] >= min_agreement_share].copy()


def summarize_agreement(agreed_matrix: pd.DataFrame) -> pd.DataFrame:
    """Summarize sentence counts by agreement level and final majority label."""
    return (
        agreed_matrix
        .groupby(['agreement_share', 'majority_label'], dropna=False)
        .size()
        .reset_index(name='sentence_count')
        .sort_values(['agreement_share', 'sentence_count'], ascending=[False, False])
    )


def load_reference_labels(path: Path | str) -> pd.DataFrame:
    """Load model reference labels and map them onto the human label scheme."""
    df = pd.read_csv(path).copy()
    missing = set(ANNOTATION_KEY_COLUMNS + [REFERENCE_LABEL_COLUMN]) - set(df.columns)
    if missing:
        raise ValueError(f'{path} is missing required columns: {sorted(missing)}')

    df['reference_label'] = df[REFERENCE_LABEL_COLUMN].map(MODEL_TO_HUMAN_LABEL)
    unmapped = df.loc[df['reference_label'].isna(), REFERENCE_LABEL_COLUMN].dropna().unique()
    if len(unmapped):
        raise ValueError(f'Unmapped reference labels: {sorted(unmapped)}')
    return df


def compare_annotators_to_reference(
    label_matrix: pd.DataFrame,
    reference_labels: pd.DataFrame,
    key_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Compare each annotator's labels with the mapped model reference labels."""
    key_columns = key_columns or ANNOTATION_KEY_COLUMNS
    merged = label_matrix.merge(
        reference_labels[key_columns + [REFERENCE_LABEL_COLUMN, 'reference_label']],
        on=key_columns,
        how='left',
    )
    label_columns = [
        col for col in merged.columns
        if col.startswith('annotator_') and col.endswith('_label')
    ]

    rows = []
    for col in label_columns:
        compared = merged[[col, 'reference_label']].dropna()
        rows.append({
            'annotator': col.removeprefix('annotator_').removesuffix('_label'),
            'compared_sentences': len(compared),
            'matches_reference': int((compared[col] == compared['reference_label']).sum()),
            'reference_match_rate': (
                (compared[col] == compared['reference_label']).mean()
                if len(compared) else pd.NA
            ),
        })
    return pd.DataFrame(rows).sort_values('reference_match_rate', ascending=False)


def export_agreement_outputs(
    agreed_matrix: pd.DataFrame,
    output_dir: Path | str,
    stem: str = 'human_expert_framing',
) -> dict[str, Path]:
    """Write sentence-level agreed labels and a compact summary to CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    agreed_path = output_dir / f'{stem}_agreed_sentences.csv'
    summary_path = output_dir / f'{stem}_agreement_summary.csv'

    agreed_matrix.to_csv(agreed_path, index=False)
    summarize_agreement(agreed_matrix).to_csv(summary_path, index=False)

    return {'agreed_sentences': agreed_path, 'agreement_summary': summary_path}
