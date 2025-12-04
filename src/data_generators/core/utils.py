from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def concat_dataframes(dfs: Iterable[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(list(dfs), ignore_index=True)
