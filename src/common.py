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

COUNTRY_ALIASES = {
    'United States of America': 'United States',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
}

TARGET_COUNTRIES = {
    'United States': ['United States', 'United States of America'],
    'China': ['China'],
    'United Kingdom': ['United Kingdom', 'United Kingdom of Great Britain and Northern Ireland'],
    'France': ['France'],
    'Germany': ['Germany'],
    'Italy': ['Italy'],
    'Japan': ['Japan'],
    'Canada': ['Canada'],
}

COUNTRY_COLORS = {
    'United States': '#1f77b4',
    'China': '#d62728',
    'United Kingdom': '#2ca02c',
    'France': '#9467bd',
    'Germany': '#8c564b',
    'Italy': '#e377c2',
    'Japan': '#ff7f0e',
    'Canada': '#17becf',
}

STRATEGY_COUNTRY_MAP = {
    'CA_National_AI_Strategy_ocr.pdf': 'Canada',
    'CN_National_AI_Strategy.pdf': 'China',
    'DE_National_AI_Strategy.pdf': 'Germany',
    'EU_AI_Strategy.pdf': 'European Union',
    'FR__National_AI_Strategy.pdf': 'France',
    'IT_National_AI_Strategy.pdf': 'Italy',
    'JP_National_AI_Strategy_ocr.pdf': 'Japan',
    'UK_National_AI_Strategy_ocr.pdf': 'United Kingdom',
    'US_National_AI_Strategy.pdf': 'United States',
    '国务院关于深入实施“人工智能+”行动的意见.pdf': 'China',
}

STRATEGY_COLORS = {
    'Canada': '#e41a1c',
    'China': '#d62728',
    'Germany': '#8c564b',
    'European Union': '#1f77b4',
    'France': '#9467bd',
    'Italy': '#e377c2',
    'Japan': '#ff7f0e',
    'United Kingdom': '#17becf',
    'United States': '#2ca02c',
}


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / 'data').is_dir():
            return path
    raise FileNotFoundError('Could not locate repo root containing `data/`')


def country_subplot_grid(n_items, n_cols=3, row_height=4.8):
    """Create enough subplots for the available strategy documents."""
    import matplotlib.pyplot as plt
    import numpy as np

    n_rows = int(np.ceil(n_items / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.2 * n_cols, row_height * n_rows))
    axes = np.atleast_1d(axes).flatten()
    for ax in axes[n_items:]:
        ax.set_visible(False)
    return fig, axes[:n_items]
