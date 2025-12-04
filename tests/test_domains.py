from data_generators.domains.engineering.iot_sensors import (
    IoTSensorsGenerator,
    IoTSensorsConfig,
)


def test_iot_sensors_generates_rows():
    gen = IoTSensorsGenerator(IoTSensorsConfig(num_devices=2, num_points=10))
    df = gen.generate()
    assert not df.empty
