from data_generators.scenarios.spark_logs.generator import (
    SparkLogsGenerator,
    SparkLogsConfig,
)


def test_spark_logs_generates_rows():
    gen = SparkLogsGenerator(SparkLogsConfig(num_rows=50))
    df = gen.generate()
    assert len(df) == 50
