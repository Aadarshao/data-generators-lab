from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import random
from typing import List

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class IoTSensorsConfig:
    num_devices: int = 10
    num_points: int = 1000
    start_time: datetime = datetime(2024, 1, 1, 0, 0, 0)
    freq_seconds: int = 60
    seed: int = 42


class IoTSensorsGenerator(BaseScenarioGenerator):
    """Generic IoT sensor time-series data generator."""

    def __init__(self, config: IoTSensorsConfig | None = None) -> None:
        self.config = config or IoTSensorsConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []

        for device_id in range(1, self.config.num_devices + 1):
            t = self.config.start_time
            for _ in range(self.config.num_points):
                value = 20 + random.random() * 5  # simple temp-like value
                records.append(
                    {
                        "device_id": device_id,
                        "timestamp": t,
                        "value": round(value, 3),
                    }
                )
                t += timedelta(seconds=self.config.freq_seconds)

        return pd.DataFrame(records)
