from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd


@dataclass
class LoanRepaymentsConfig:
    """Configuration for loan repayment schedule generator."""

    num_loans: int = 200
    min_principal: int = 50000
    max_principal: int = 500000
    min_tenure_months: int = 6
    max_tenure_months: int = 60
    min_annual_rate: float = 10.0
    max_annual_rate: float = 18.0
    start_date: date = date(2024, 1, 1)
    seed: int = 999

    # Probabilities for non-ideal behavior
    p_late_installment: float = 0.08
    p_default_loan: float = 0.04


class LoanRepaymentsGenerator:
    """Generate synthetic EMI-style loan repayment schedules."""

    def __init__(self, config: LoanRepaymentsConfig | None = None) -> None:
        self.cfg = config or LoanRepaymentsConfig()
        random.seed(self.cfg.seed)

    def _next_month(self, d: date) -> date:
        """Move to the same day next month (rough approximation)."""
        month = d.month + 1
        year = d.year
        if month > 12:
            month = 1
            year += 1
        # Clamp day to 28 to avoid invalid dates
        day = min(d.day, 28)
        return date(year, month, day)

    def _build_schedule_for_loan(
        self,
        loan_id: str,
        customer_id: str,
        principal: float,
        tenure_months: int,
        annual_rate: float,
        start_date: date,
    ) -> list[dict]:
        """Build EMI schedule rows for a single loan."""
        rows: list[dict] = []

        monthly_rate = annual_rate / 12.0 / 100.0
        n = tenure_months

        if monthly_rate == 0:
            emi = principal / n
        else:
            # Standard EMI formula
            emi = principal * monthly_rate * (1 + monthly_rate) ** n / (
                (1 + monthly_rate) ** n - 1
            )

        emi = round(emi, 2)
        remaining_principal = principal
        schedule_date = start_date

        # Decide if this loan will default at some point
        will_default = random.random() < self.cfg.p_default_loan
        default_after_installment = (
            random.randint(3, n) if will_default else None
        )

        for k in range(1, n + 1):
            # Interest for this period
            interest_component = round(remaining_principal * monthly_rate, 2)
            principal_component = round(emi - interest_component, 2)

            # Last installment adjustment to clear rounding
            if k == n:
                principal_component = remaining_principal
                emi_effective = principal_component + interest_component
            else:
                emi_effective = emi

            remaining_principal = max(
                0.0, round(remaining_principal - principal_component, 2)
            )

            # Determine status
            if will_default and default_after_installment is not None and k > default_after_installment:
                status = "DEFAULTED"
                is_missed = 1
            else:
                r = random.random()
                if r < self.cfg.p_late_installment:
                    status = "LATE"
                    is_missed = 1
                else:
                    status = "PAID"
                    is_missed = 0

            rows.append(
                {
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "schedule_date": schedule_date,
                    "installment_number": k,
                    "emi_amount": round(emi_effective, 2),
                    "principal_component": round(principal_component, 2),
                    "interest_component": round(interest_component, 2),
                    "remaining_principal": round(remaining_principal, 2),
                    "status": status,
                    "is_missed_payment": is_missed,
                }
            )

            schedule_date = self._next_month(schedule_date)

        return rows

    def generate(self) -> pd.DataFrame:
        cfg = self.cfg
        all_rows: list[dict] = []

        for idx in range(1, cfg.num_loans + 1):
            loan_id = f"LN-REP-{idx:05d}"
            customer_id = f"CUST-{random.randint(10000, 99999)}"

            principal = random.randint(cfg.min_principal, cfg.max_principal)
            tenure = random.randint(cfg.min_tenure_months, cfg.max_tenure_months)
            annual_rate = round(
                random.uniform(cfg.min_annual_rate, cfg.max_annual_rate), 2
            )

            start_date = cfg.start_date + timedelta(days=random.randint(0, 90))

            schedule_rows = self._build_schedule_for_loan(
                loan_id=loan_id,
                customer_id=customer_id,
                principal=float(principal),
                tenure_months=tenure,
                annual_rate=annual_rate,
                start_date=start_date,
            )
            all_rows.extend(schedule_rows)

        return pd.DataFrame(all_rows)
