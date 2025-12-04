from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import random

import pandas as pd

from ...core.base_generator import BaseScenarioGenerator


@dataclass
class SparkLogsConfig:
    num_jobs: int = 10
    max_stages_per_job: int = 5
    max_tasks_per_stage: int = 20
    num_rows: int | None = None
    start_time: datetime = datetime(2024, 1, 1, 0, 0, 0)
    seed: int = 101


class SparkLogsGenerator(BaseScenarioGenerator):
    """Synthetic Spark-like logs (jobs, stages, tasks)."""

    def __init__(self, config: SparkLogsConfig | None = None) -> None:
        self.config = config or SparkLogsConfig()
        random.seed(self.config.seed)

    def generate(self) -> pd.DataFrame:
        records: List[dict] = []
        t = self.config.start_time

        for job_id in range(1, self.config.num_jobs + 1):
            app_id = f"app-{job_id:04d}"
            num_stages = random.randint(1, self.config.max_stages_per_job)

            for stage_id in range(num_stages):
                num_tasks = random.randint(1, self.config.max_tasks_per_stage)
                for task_id in range(num_tasks):
                    t += timedelta(seconds=random.randint(1, 10))
                    level = random.choices(
                        ["INFO", "WARN", "ERROR"],
                        weights=[0.9, 0.07, 0.03],
                        k=1,
                    )[0]
                    msg = f"Job {job_id} Stage {stage_id} Task {task_id} {level}"
                    records.append(
                        {
                            "ts": t,
                            "app_id": app_id,
                            "job_id": job_id,
                            "stage_id": stage_id,
                            "task_id": task_id,
                            "level": level,
                            "message": msg,
                        }
                    )
                    if (
                        self.config.num_rows is not None
                        and len(records) >= self.config.num_rows
                    ):
                        return pd.DataFrame(records)

        return pd.DataFrame(records)
