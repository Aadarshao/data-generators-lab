from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import random

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


STATUSES = ["REJECTED", "PENDING", "APPROVED", "CLOSED"]
STATUS_WEIGHTS = [0.3, 0.3, 0.2, 0.2]  # approx from your sample

PRODUCT_TYPES = ["AUTO", "PERSONAL", "HOME"]
BRANCHES = ["Pokhara", "Biratnagar", "Kathmandu"]
CREDIT_SCORE_BANDS = ["LOW", "MEDIUM", "HIGH"]


@dataclass
class LoanApplicationsConfig:
    """Configuration for generating synthetic loan application data."""

    num_rows: int = 1000
    start_datetime: datetime = datetime(2025, 1, 1, 9, 0)
    end_datetime: datetime = datetime(2025, 1, 31, 18, 0)
    min_amount: int = 5000
    max_amount: int = 10000
    amount_step: int = 1000
    interest_rates: tuple[float, ...] = (
        11.0,
        11.5,
        12.0,
        12.5,
        13.0,
        13.5,
        14.0,
    )
    tenure_options: tuple[int, ...] = (12, 24, 36, 48, 60)
    seed: int = 123

    # Approximate missingness probabilities
    p_missing_created_at: float = 0.18
    p_missing_amount: float = 0.18
    p_missing_rate: float = 0.16
    p_missing_tenure: float = 0.22
    p_missing_status: float = 0.08
    p_missing_product_type: float = 0.14
    p_missing_branch: float = 0.10
    p_missing_credit_band: float = 0.16


class LoanApplicationsGenerator(BaseScenarioGenerator):
    """Generate synthetic loan application data."""

    def __init__(self, config: Optional[LoanApplicationsConfig] = None) -> None:
        self.config = config or LoanApplicationsConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        rows: List[dict] = []

        dt_range_seconds = int(
            (self.config.end_datetime - self.config.start_datetime).total_seconds()
        )

        for idx in range(1, self.config.num_rows + 1):
            loan_id = f"LN{idx:04d}"
            customer_id = f"CUST{idx:04d}"

            created_at = self._maybe_missing(
                self.config.p_missing_created_at,
                self._random_datetime(dt_range_seconds),
            )

            amount = self._maybe_missing(
                self.config.p_missing_amount,
                self._random_amount(),
            )

            interest_rate = self._maybe_missing(
                self.config.p_missing_rate,
                random.choice(self.config.interest_rates),
            )

            tenure_months = self._maybe_missing(
                self.config.p_missing_tenure,
                random.choice(self.config.tenure_options),
            )

            status = self._maybe_missing(
                self.config.p_missing_status,
                random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0],
            )

            product_type = self._maybe_missing(
                self.config.p_missing_product_type,
                random.choice(PRODUCT_TYPES),
            )

            branch = self._maybe_missing(
                self.config.p_missing_branch,
                random.choice(BRANCHES),
            )

            credit_score_band = self._maybe_missing(
                self.config.p_missing_credit_band,
                random.choice(CREDIT_SCORE_BANDS),
            )

            rows.append(
                {
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "created_at": created_at,
                    "amount": amount,
                    "interest_rate": interest_rate,
                    "tenure_months": tenure_months,
                    "status": status,
                    "product_type": product_type,
                    "branch": branch,
                    "credit_score_band": credit_score_band,
                }
            )

        df = pd.DataFrame(rows)
        return df

    def _random_datetime(self, dt_range_seconds: int) -> datetime:
        offset = random.randint(0, dt_range_seconds)
        return self.config.start_datetime + timedelta(seconds=offset)

    def _random_amount(self) -> int:
        steps = (self.config.max_amount - self.config.min_amount) // self.config.amount_step
        step_idx = random.randint(0, steps)
        return self.config.min_amount + step_idx * self.config.amount_step

    @staticmethod
    def _maybe_missing(p: float, value):
        return None if random.random() < p else value
