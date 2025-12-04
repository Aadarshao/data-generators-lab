from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import random
from typing import List

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class EcommerceConfig:
    num_users: int = 200
    max_events_per_user: int = 50
    start_time: datetime = datetime(2024, 1, 1, 0, 0, 0)
    seed: int = 7


class EcommerceEventsGenerator(BaseScenarioGenerator):
    """Simple ecommerce event stream generator (view, add_to_cart, purchase)."""

    def __init__(self, config: EcommerceConfig | None = None) -> None:
        self.config = config or EcommerceConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []

        event_types = ["view", "add_to_cart", "purchase"]
        for user_id in range(1, self.config.num_users + 1):
            t = self.config.start_time
            num_events = random.randint(5, self.config.max_events_per_user)
            for _ in range(num_events):
                t += timedelta(minutes=random.randint(1, 120))
                event = random.choices(
                    event_types, weights=[0.7, 0.2, 0.1], k=1
                )[0]
                records.append(
                    {
                        "user_id": user_id,
                        "event_time": t,
                        "event_type": event,
                    }
                )

        return pd.DataFrame(records)
