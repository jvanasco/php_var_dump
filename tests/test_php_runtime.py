"""Check generated PHP with the optional PHP CLI."""

import errno
import json
import os
import subprocess
from datetime import date, datetime
from decimal import Decimal

import pytest

from php_var_dump import php_as_block, php_var_dump
from tests import FixedOffset


def _run_php(data, expression, datetime_format="timestamp", min_php_version=0):
    # type: (object, str, str, int) -> object
    """Evaluate a test expression using the generated assignment."""
    if os.environ.get("CI") and "PHP_BINARY" not in os.environ:
        pytest.skip("PHP runtime tests run in the CI job that sets PHP_BINARY.")
    source = php_as_block(
        "if (PHP_VERSION_ID < %d) { exit(77); }\n" % min_php_version
        + php_var_dump("value", data, datetime_format=datetime_format)
        + "\necho json_encode("
        + expression
        + ");"
    ).encode("utf-8")
    executable = os.environ.get("PHP_BINARY", "php")
    try:
        process = subprocess.Popen(
            [executable, "-n"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        if exc.errno != errno.ENOENT or "PHP_BINARY" in os.environ:
            raise
        pytest.skip("PHP CLI unavailable. Set PHP_BINARY to its executable path.")
    stdout, stderr = process.communicate(source)
    if process.returncode == 77:
        assert not os.environ.get(
            "CI"
        ), "PHP CLI is older than the configured CI version"
        pytest.skip("The selected datetime encoding requires PHP 8.4 or later.")
    assert process.returncode == 0, (stdout, stderr)
    assert not stderr, stderr
    return json.loads(stdout.decode("utf-8"))


def test_nested_values_round_trip():
    # type: () -> None
    """Preserve nested values, Unicode, quotes, backslashes, and embedded NULs."""
    key = "quote'\\"
    text = b"caf\xc3\xa9\x00'\\$value".decode("utf-8")
    data = {key: [text, True, False, None, -123, 1.25]}
    result = _run_php(data, "$value")
    assert json.dumps(result, sort_keys=True) == json.dumps(data, sort_keys=True)


def test_numeric_string_keys():
    # type: () -> None
    """Characterize which numeric-looking string keys PHP coerces to integers."""
    data = dict.fromkeys(("12345", "01234", "+12345", "12345-6789", "42-07"), True)
    assert sorted(_run_php(data, "array_keys($value)"), key=str) == [
        "+12345",
        "01234",
        12345,
        "12345-6789",
        "42-07",
    ]


def test_integer_outside_php_range():
    # type: () -> None
    """Characterize the precision loss when a PHP integer literal overflows."""
    value = 2**80 + 1
    assert _run_php(value, "array(is_float($value), $value == pow(2, 80))") == [
        True,
        True,
    ]


@pytest.mark.parametrize(
    "datetime_format,min_php_version",
    [("timestamp", 80400), ("timestamp_legacy", 0)],
)
def test_datetime_timestamp_round_trip(datetime_format, min_php_version):
    # type: (str, int) -> None
    """Preserve the instant and fractional seconds on both sides of the epoch."""
    values = [
        datetime(1970, 1, 1, 0, 59, 59, 876544, tzinfo=FixedOffset()),
        datetime(9999, 1, 1, 1, 0, 0, 123456, tzinfo=FixedOffset()),
    ]
    assert (
        _run_php(
            {"dates": values},
            """array($value['dates'][0]->format('Y-m-d H:i:s.u P'),
                 $value['dates'][1]->format('Y-m-d H:i:s.u P'))""",
            datetime_format,
            min_php_version,
        )
        == ["1969-12-31 23:59:59.876544 +00:00", "9999-01-01 00:00:00.123456 +00:00"]
    )


def test_datetime_string_round_trip():
    # type: () -> None
    """Preserve the ISO string and original offset in a nested value."""
    value = datetime(1970, 1, 1, 1, 0, 0, 123456, tzinfo=FixedOffset())
    assert _run_php([value], "$value", "string") == ["1970-01-01T01:00:00.123456+01:00"]


def test_date_and_decimal_round_trip():
    # type: () -> None
    """PHP receives date and decimal fields as strings."""
    value = {"day": date(2028, 2, 29), "amount": Decimal("12345678901234567890.1200")}
    assert _run_php(value, "$value") == {
        "day": "2028-02-29",
        "amount": "12345678901234567890.1200",
    }
