from __future__ import annotations

import argparse
from pathlib import Path

from .scenarios.attendance.generator import AttendanceGenerator, AttendanceConfig
from .scenarios.spark_logs.generator import SparkLogsGenerator, SparkLogsConfig
from .scenarios.loan_applications.generator import (
    LoanApplicationsGenerator,
    LoanApplicationsConfig,
)
from .scenarios.bank_transactions.generator import (
    BankTransactionsGenerator,
    BankTransactionsConfig,
)
from .scenarios.credit_card_spend.generator import (
    CreditCardSpendGenerator,
    CreditCardSpendConfig,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data_generators",
        description="Synthetic data generators for various realistic scenarios.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate data for a scenario.")
    gen.add_argument(
        "scenario",
        choices=[
            "attendance",
            "spark_logs",
            "loans",
            "bank_transactions",
            "credit_card_spend",
        ],
        help="Scenario name.",
    )
    gen.add_argument(
        "--rows",
        type=int,
        default=None,
        help="Approximate number of rows to generate (if supported).",
    )
    gen.add_argument(
        "--out",
        type=str,
        required=True,
        help="Output file path (CSV or Parquet based on extension).",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.scenario == "attendance":
        config = AttendanceConfig()
        if args.rows is not None:
            config.num_employees = max(1, args.rows // 200)
        gen = AttendanceGenerator(config)
        df = gen.generate()

    elif args.scenario == "spark_logs":
        config = SparkLogsConfig()
        if args.rows is not None:
            config.num_rows = args.rows
        gen = SparkLogsGenerator(config)
        df = gen.generate()

    elif args.scenario == "loans":
        config = LoanApplicationsConfig()
        if args.rows is not None:
            config.num_rows = args.rows
        gen = LoanApplicationsGenerator(config)
        df = gen.generate()

    elif args.scenario == "bank_transactions":
        config = BankTransactionsConfig()
        if args.rows is not None:
            config.num_rows = args.rows
        gen = BankTransactionsGenerator(config)
        df = gen.generate()

    elif args.scenario == "credit_card_spend":
        config = CreditCardSpendConfig()
        if args.rows is not None:
            config.num_rows = args.rows
        gen = CreditCardSpendGenerator(config)
        df = gen.generate()

    else:
        parser.error(f"Unknown scenario: {args.scenario}")

    if out_path.suffix.lower() == ".csv":
        df.to_csv(out_path, index=False)
    elif out_path.suffix.lower() in {".parquet", ".pq"}:
        df.to_parquet(out_path, index=False)
    else:
        parser.error("Output file must end with .csv or .parquet")

    print(f"Generated {len(df)} rows -> {out_path}")


if __name__ == "__main__":
    main()
