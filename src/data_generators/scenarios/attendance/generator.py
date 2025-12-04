from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, time
from typing import List
import random

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class AttendanceConfig:
    start_date: date = date(2024, 1, 1)
    end_date: date = date(2024, 12, 31)
    num_employees: int = 200
    seed: int = 42


class AttendanceGenerator(BaseScenarioGenerator):
    """Generate synthetic employee attendance data with these constraints."""

    def __init__(self, config: AttendanceConfig | None = None) -> None:
        self.config = config or AttendanceConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []

        all_dates = self._generate_dates(
            self.config.start_date, self.config.end_date
        )

        for emp_id in range(1, self.config.num_employees + 1):
            dept = random.choice(
                ["HR", "Finance", "Engineering", "Sales", "Support"]
            )

            for d in all_dates:
                if d.weekday() >= 5:  # weekend
                    if random.random() < 0.05:
                        status = random.choices(
                            ["ABSENT", "WFH"], weights=[0.7, 0.3], k=1
                        )[0]
                    else:
                        continue
                else:
                    status = self._sample_status()

                check_in, check_out = self._sample_times_for_status(status)

                records.append(
                    {
                        "employee_id": emp_id,
                        "department": dept,
                        "date": d,
                        "status": status,
                        "check_in": check_in,
                        "check_out": check_out,
                    }
                )

        return pd.DataFrame(records)

    @staticmethod
    def _generate_dates(start: date, end: date) -> List[date]:
        days = (end - start).days + 1
        return [start + timedelta(days=i) for i in range(days)]

    @staticmethod
    def _sample_status() -> str:
        return random.choices(
            ["PRESENT", "ABSENT", "LATE", "WFH"],
            weights=[0.85, 0.05, 0.05, 0.05],
            k=1,
        )[0]

    @staticmethod
    def _sample_times_for_status(status: str):
        if status == "ABSENT":
            return None, None

        base_in = datetime.combine(date.today(), time(9, 0))
        base_out = datetime.combine(date.today(), time(17, 30))

        if status == "LATE":
            delta_min = random.randint(16, 60)
        else:
            delta_min = random.randint(-30, 30)

        out_delta_min = random.randint(-15, 120)

        check_in = (base_in + timedelta(minutes=delta_min)).time()
        check_out = (base_out + timedelta(minutes=out_delta_min)).time()

        return check_in, check_out
