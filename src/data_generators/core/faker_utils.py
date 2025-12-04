from __future__ import annotations

from faker import Faker

_faker = Faker()

def get_faker() -> Faker:
    """Return a shared Faker instance."""
    return _faker
