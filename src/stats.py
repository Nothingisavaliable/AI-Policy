import pandas as pd


def descriptive_statistics(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return count, mean, median, stdev, min, and max for numeric columns."""
    stats = (
        df[columns]
        .agg(['count', 'mean', 'median', 'std', 'min', 'max'])
        .T
        .rename(columns={'std': 'stdev'})
        .round(2)
    )
    stats.index.name = 'Variable'
    return stats

