from src.event_log import EventLog
from src.hardware import detect_hardware


def test_hardware_diagnostics_are_read_only_and_have_expected_keys():
    result = detect_hardware()
    assert "os" in result
    assert "architecture" in result
    assert "gpu_vendors" in result
    assert isinstance(result["gpu_vendors"], list)


def test_event_log_is_bounded_and_formats_levels():
    log = EventLog(max_items=2)
    log.add("first")
    log.add("second", "warning")
    log.add("third")
    lines = log.lines()
    assert len(lines) == 2
    assert "WARNING" in lines[0]
    assert "third" in lines[1]
