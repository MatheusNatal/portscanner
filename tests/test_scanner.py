import pytest
from portscanner.cli import parse_ports


def test_parse_ports_single_and_comma():
    assert parse_ports("80, 443, 8080") == [80, 443, 8080]


def test_parse_ports_range():
    assert parse_ports("20-23") == [20, 21, 22, 23]


def test_parse_ports_combined():
    assert parse_ports("22, 80-82, 443") == [22, 80, 81, 82, 443]


def test_parse_ports_invalid_string():
    with pytest.raises(ValueError):
        parse_ports("invalid_port")


def test_parse_ports_out_of_range():
    with pytest.raises(ValueError):
        parse_ports("70000")


def test_parse_ports_inverted_range():
    with pytest.raises(ValueError):
        parse_ports("100-20")