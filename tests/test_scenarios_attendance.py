from data_generators.scenarios.attendance.generator import (
    AttendanceGenerator,
    AttendanceConfig,
)


def test_attendance_generates_rows():
    gen = AttendanceGenerator(AttendanceConfig(num_employees=5))
    df = gen.generate()
    assert not df.empty
