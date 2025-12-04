import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

fake = Faker()


@dataclass
class BankTransactionsConfig:
    num_rows: int = 1000
    seed: int = 42
    fraud_rate: float = 0.02  # 2% fraud
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"


class BankTransactionsGenerator:
    def __init__(self, config: BankTransactionsConfig):
        self.cfg = config
        random.seed(config.seed)
        Faker.seed(config.seed)

        self.merchant_categories = {
            "grocery": ["Walmart", "Carrefour", "Big Basket", "Kroger"],
            "travel": ["Uber", "Lyft", "Booking.com", "Airbnb"],
            "food": ["McDonald's", "Starbucks", "KFC", "Pizza Hut"],
            "electronics": ["Apple Store", "Best Buy", "Mi Store"],
            "utilities": ["Electric Co", "Water Board", "Gas Authority"],
        }

        self.channels = ["online", "card_swipe", "atm", "upi", "net_banking"]

    def random_timestamp(self):
        start = datetime.fromisoformat(self.cfg.start_date)
        end = datetime.fromisoformat(self.cfg.end_date)
        delta = end - start
        random_second = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_second)

    def generate(self) -> pd.DataFrame:
        rows = []

        for _ in range(self.cfg.num_rows):

            # choose merchant category
            category = random.choice(list(self.merchant_categories.keys()))
            merchant = random.choice(self.merchant_categories[category])

            amount = round(random.uniform(1, 2500), 2)

            is_fraud = 1 if random.random() < self.cfg.fraud_rate else 0

            rows.append(
                {
                    "transaction_id": str(uuid.uuid4()),
                    "customer_id": f"CUST-{random.randint(10000, 99999)}",
                    "timestamp": self.random_timestamp(),
                    "amount": amount,
                    "transaction_type": "debit" if random.random() > 0.5 else "credit",
                    "merchant": merchant,
                    "merchant_category": category,
                    "location": fake.city(),
                    "channel": random.choice(self.channels),
                    "is_fraud": is_fraud,
                }
            )

        return pd.DataFrame(rows)
