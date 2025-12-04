from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class ExperimentsConfig:
    num_experiments: int = 50
    measurements_per_experiment: int = 20
    seed: int = 123


class ExperimentsGenerator(BaseScenarioGenerator):
    """Simple lab experiment measurement generator."""

    def __init__(self, config: ExperimentsConfig | None = None) -> None:
        self.config = config or ExperimentsConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []
        for exp_id in range(1, self.config.num_experiments + 1):
            baseline = random.uniform(0.5, 1.5)
            for step in range(self.config.measurements_per_experiment):
                value = baseline + random.gauss(0, 0.05)
                records.append(
                    {
                        "experiment_id": exp_id,
                        "step": step,
                        "value": value,
                    }
                )
        return pd.DataFrame(records)
