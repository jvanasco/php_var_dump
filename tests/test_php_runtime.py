"""Check generated PHP with the optional PHP CLI."""

import errno
import json
import os
import subprocess

import pytest

from php_var_dump import php_as_block, php_var_dump


def _run_php(data, expression):
    # type: (object, str) -> object
    """Evaluate a test expression using the generated assignment."""
    source = php_as_block(
        php_var_dump("value", data) + "\necho json_encode(" + expression + ");"
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
    data = {"12": True, "012": True, "+12": True}
    assert sorted(_run_php(data, "array_keys($value)"), key=str) == ["+12", "012", 12]


def test_integer_outside_php_range():
    # type: () -> None
    """Characterize the precision loss when a PHP integer literal overflows."""
    value = 2**80 + 1
    assert _run_php(value, "array(is_float($value), $value == pow(2, 80))") == [
        True,
        True,
    ]
