from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()


@dataclass
class CreditCardSpendConfig:
    """Configuration for credit card spend generator."""

    num_rows: int = 1000
    seed: int = 101
    fraud_rate: float = 0.015  # 1.5% fraud
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"


class CreditCardSpendGenerator:
    """Generate synthetic credit card spend data."""

    def __init__(self, config: CreditCardSpendConfig | None = None) -> None:
        self.cfg = config or CreditCardSpendConfig()
        random.seed(self.cfg.seed)
        Faker.seed(self.cfg.seed)

        # Merchant category -> sample merchants
        self.merchant_categories: dict[str, list[str]] = {
            "grocery": ["Local Mart", "City Supermarket", "Fresh Grocery"],
            "fuel": ["Petro Station", "Fuel Point", "Highway Fuel"],
            "travel": ["Sky Airlines", "City Hotel", "Travel Hub"],
            "food": ["Urban Cafe", "Food Corner", "Spice Kitchen"],
            "electronics": ["Tech World", "Gadget Store", "Digital Arena"],
            "clothing": ["Fashion Hub", "Style Street", "Trend Store"],
            "utilities": ["Power Company", "Water Utility", "ISP Service"],
            "entertainment": ["Cinema Hall", "Game Zone", "Streaming Service"],
        }

        self.card_networks = ["VISA", "MASTERCARD", "AMEX", "RUPAY"]
        self.currencies = ["NPR", "USD", "EUR", "INR"]
        self.channels = ["POS", "ECOM", "ATM", "UPI"]

    def _random_timestamp(self) -> datetime:
        start = datetime.fromisoformat(self.cfg.start_date)
        end = datetime.fromisoformat(self.cfg.end_date)
        delta = end - start
        random_second = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_second)

    def _sample_transaction(self) -> dict:
        category = random.choice(list(self.merchant_categories.keys()))
        merchant = random.choice(self.merchant_categories[category])

        card_network = random.choice(self.card_networks)
        currency = random.choices(self.currencies, weights=[0.6, 0.2, 0.1, 0.1], k=1)[0]
        channel = random.choice(self.channels)

        # Amount distribution: normal spending vs a few large outliers
        base_amount = random.lognormvariate(3.0, 0.6)  # skewed positive
        amount = round(min(max(base_amount, 10), 5000), 2)

        # International vs domestic
        is_international = 1 if currency in {"USD", "EUR"} and random.random() < 0.5 else 0

        # Online vs not
        is_online = 1 if channel in {"ECOM", "UPI"} else 0

        # Simple fraud logic: higher chance for international + online + high amount
        fraud_score = 0.0
        if is_international:
            fraud_score += 0.4
        if is_online:
            fraud_score += 0.3
        if amount > 1000:
            fraud_score += 0.3

        # Base fraud probability from config
        base_prob = self.cfg.fraud_rate
        prob_fraud = min(0.9, base_prob + fraud_score)
        is_fraud = 1 if random.random() < prob_fraud else 0

        txn_time = self._random_timestamp()
        country = fake.country()
        city = fake.city()

        return {
            "transaction_id": str(uuid.uuid4()),
            "customer_id": f"CUST-{random.randint(10000, 99999)}",
            "card_id": f"CARD-{random.randint(100000, 999999)}",
            "card_network": card_network,
            "txn_timestamp": txn_time,
            "amount": amount,
            "currency": currency,
            "merchant": merchant,
            "merchant_category": category,
            "channel": channel,
            "country": country,
            "city": city,
            "is_international": is_international,
            "is_online": is_online,
            "is_fraud": is_fraud,
        }

    def generate(self) -> pd.DataFrame:
        rows: list[dict] = []
        for _ in range(self.cfg.num_rows):
            rows.append(self._sample_transaction())
        return pd.DataFrame(rows)
