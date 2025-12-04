from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class BillingConfig:
    num_customers: int = 100
    seed: int = 202


class BillingGenerator(BaseScenarioGenerator):
    """Placeholder billing scenario (extend later)."""

    def __init__(self, config: BillingConfig | None = None) -> None:
        self.config = config or BillingConfig()

    def generate(self) -> pd.DataFrame:
        # TODO: implement realistic billing data
        return pd.DataFrame()
