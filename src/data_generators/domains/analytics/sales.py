from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import random
from typing import List

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class SalesConfig:
    start_date: date = date(2024, 1, 1)
    end_date: date = date(2024, 12, 31)
    max_orders_per_day: int = 50
    seed: int = 99


class SalesGenerator(BaseScenarioGenerator):
    """Simple daily sales orders generator."""

    def __init__(self, config: SalesConfig | None = None) -> None:
        self.config = config or SalesConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []

        d = self.config.start_date
        while d <= self.config.end_date:
            num_orders = random.randint(0, self.config.max_orders_per_day)
            for _ in range(num_orders):
                amount = round(random.uniform(10, 500), 2)
                records.append(
                    {
                        "order_id": f"O{d:%Y%m%d}{random.randint(1000, 9999)}",
                        "order_date": d,
                        "amount": amount,
                    }
                )
            d += timedelta(days=1)

        return pd.DataFrame(records)
