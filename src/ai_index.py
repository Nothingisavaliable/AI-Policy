import numpy as np
import pandas as pd


def normalize_scores(df: pd.DataFrame) -> pd.DataFrame:
    norm = df.copy().astype(float)
    norm = np.log10(norm.clip(lower=0) + 1)
    for col in norm.columns:
        col_min = norm[col].min()
        col_max = norm[col].max()
        rng = col_max - col_min
        norm[col] = ((norm[col] - col_min) / rng * 100) if rng > 0 else 0
    return norm.round(1)


def compute_weighted_scores(norm_df: pd.DataFrame, weights: dict):
    total = sum(weights.values())
    norm_w = {key: value / total for key, value in weights.items()} if total > 0 else {
        key: 0 for key in weights
    }
    scores = pd.Series(0.0, index=norm_df.index)
    for dim, weight in norm_w.items():
        scores += norm_df[dim] * weight
    return scores.sort_values(ascending=False), norm_w

