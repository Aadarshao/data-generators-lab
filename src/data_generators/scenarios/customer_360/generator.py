from __future__ import annotations

import random
from dataclasses import dataclass

import pandas as pd
from faker import Faker

fake = Faker()


@dataclass
class Customer360Config:
    """Configuration for customer 360 profile generator."""

    num_customers: int = 1000
    seed: int = 2025


class Customer360Generator:
    """Generate synthetic Customer 360 profiles."""

    def __init__(self, config: Customer360Config | None = None) -> None:
        self.cfg = config or Customer360Config()
        random.seed(self.cfg.seed)
        Faker.seed(self.cfg.seed)

        self.occupations = [
            "Student",
            "Engineer",
            "Teacher",
            "Manager",
            "Self-employed",
            "Doctor",
            "Nurse",
            "Government",
            "Unemployed",
            "Retired",
        ]

    def _sample_customer(self, idx: int) -> dict:
        customer_id = f"CUST-{idx:06d}"
        profile = fake.simple_profile()

        full_name = profile["name"]
        gender_raw = profile["sex"]  # 'M' or 'F'
        gender = gender_raw if gender_raw in {"M", "F"} else "O"

        age = random.randint(18, 75)
        country = fake.country()
        city = fake.city()

        # Income distribution: different tiers
        if age < 24:
            income = random.uniform(100000, 400000)
        elif age < 35:
            income = random.uniform(300000, 900000)
        elif age < 50:
            income = random.uniform(400000, 1500000)
        else:
            income = random.uniform(200000, 800000)
        income = round(income, 2)

        occupation = random.choice(self.occupations)

        # Product ownership
        has_credit_card = 1 if random.random() < 0.65 else 0
        has_loan = 1 if random.random() < 0.45 else 0
        has_savings = 1 if random.random() < 0.85 else 0

        num_products = has_credit_card + has_loan + has_savings
        if num_products == 0 and random.random() < 0.3:
            # Force at least one product sometimes
            has_savings = 1
            num_products = 1

        # Total balance approximate model
        base_balance = 0.0
        if has_savings:
            base_balance += random.uniform(20000, 300000)
        if has_credit_card:
            base_balance += random.uniform(-50000, 50000)  # could be net positive or debt
        if has_loan:
            base_balance -= random.uniform(50000, 500000)  # debt impact

        total_balance = round(base_balance, 2)

        # Risk & engagement modeling
        # Higher debt / lower income -> higher risk
        debt_indicator = 1 if has_loan or total_balance < 0 else 0
        if debt_indicator and income < 400000:
            risk_segment = "HIGH"
        elif debt_indicator:
            risk_segment = "MEDIUM"
        else:
            risk_segment = random.choices(["LOW", "MEDIUM"], weights=[0.7, 0.3], k=1)[0]

        # Churn score: inverse of engagement and product count (very rough)
        engagement_score = random.uniform(0.1, 0.9)
        engagement_score += 0.05 * (num_products - 1)
        engagement_score = max(0.0, min(1.0, engagement_score))

        churn_score = 1.0 - engagement_score
        if risk_segment == "HIGH":
            churn_score = min(1.0, churn_score + 0.2)
        churn_score = round(churn_score, 3)
        engagement_score = round(engagement_score, 3)

        return {
            "customer_id": customer_id,
            "full_name": full_name,
            "age": age,
            "gender": gender,
            "country": country,
            "city": city,
            "income_annual": income,
            "occupation": occupation,
            "risk_segment": risk_segment,
            "has_credit_card": has_credit_card,
            "has_loan": has_loan,
            "has_savings_account": has_savings,
            "num_products": num_products,
            "total_balance": total_balance,
            "churn_score": churn_score,
            "engagement_score": engagement_score,
        }

    def generate(self) -> pd.DataFrame:
        rows: list[dict] = []
        for i in range(1, self.cfg.num_customers + 1):
            rows.append(self._sample_customer(i))
        return pd.DataFrame(rows)
