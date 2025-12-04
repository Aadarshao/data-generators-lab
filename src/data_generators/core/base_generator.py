from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd


class BaseScenarioGenerator(ABC):
    """Base class for all scenario generators.

    Subclasses must implement :meth:`generate` and return a pandas DataFrame.
    """

    @abstractmethod
    def generate(self) -> pd.DataFrame:
        """Generate a pandas DataFrame for this scenario."""
        raise NotImplementedError

    def save(
        self,
        path: str | Path,
        *,
        format: str | None = None,
        **kwargs: Any,
    ) -> Path:
        """Generate and save data to the specified path.

        Format can be inferred from the extension (.csv / .parquet)
        or provided explicitly.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df = self.generate()

        fmt = format or path.suffix.lower().lstrip(".")
        if fmt == "csv":
            df.to_csv(path, index=False, **kwargs)
        elif fmt in {"parquet", "pq"}:
            df.to_parquet(path, index=False, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        return path
