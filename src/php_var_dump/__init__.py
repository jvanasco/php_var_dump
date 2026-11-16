"""Serialize simple Python values as PHP source code."""

import math
import re
from datetime import date, datetime
from decimal import Decimal

import six

__VERSION__ = "1.0.0"

_EPOCH = datetime(1970, 1, 1)
_DATETIME_FORMATS = ("timestamp", "timestamp_legacy", "string")

# PHP accepts ASCII letters, underscores, and non-ASCII bytes in identifiers.
_VARIABLE_NAME = re.compile(
    r"\A(?:[A-Za-z_]|[^\x00-\x7f])(?:[A-Za-z_0-9]|[^\x00-\x7f])*\Z"
)


def _php_string(value):
    # type: (object) -> str
    """Quote a value as a PHP string, preserving Python 2 text types."""
    if not isinstance(value, six.string_types):
        value = str(value)
    return "'%s'" % value.replace("\\", "\\\\").replace("'", "\\'")


def _php_datetime(value, datetime_format):
    # type: (datetime, str) -> str
    """Render an ISO 8601 literal or a PHP DateTimeImmutable expression."""
    if datetime_format == "string":
        return _php_string(value.isoformat())

    offset = value.utcoffset()
    if offset is None:
        raise ValueError("Timestamp encoding requires a timezone-aware datetime")

    delta = value.replace(tzinfo=None) - _EPOCH - offset
    seconds = delta.days * 86400 + delta.seconds
    if datetime_format == "timestamp_legacy":
        total_microseconds = seconds * 1000000 + delta.microseconds
        whole, fraction = divmod(abs(total_microseconds), 1000000)
        timestamp = ("-" if total_microseconds < 0 else "") + str(whole)
        if fraction:
            timestamp += ".%06d" % fraction
        return "new \\DateTimeImmutable(%s)" % _php_string("@" + timestamp)

    expression = "\\DateTimeImmutable::createFromTimestamp(%d)" % seconds
    if delta.microseconds:
        expression += "->modify('+%d microseconds')" % delta.microseconds
    return expression


def _php_var_dump(data, depth=0, ancestors=None, datetime_format="timestamp"):
    # type: (object, int, set[int] | None, str) -> str
    """Render a literal with indentation and reject recursive containers."""
    padding = "  " * depth
    if isinstance(data, (dict, list, tuple)):
        if ancestors is None:
            ancestors = set()
        identity = id(data)
        if identity in ancestors:
            raise ValueError("Cannot serialize a recursive container")
        ancestors.add(identity)
        try:
            if isinstance(data, dict):
                keypadding = padding + "  "
                items = [
                    "%s%s => %s"
                    % (
                        keypadding,
                        _php_string(key),
                        _php_var_dump(value, depth + 1, ancestors, datetime_format),
                    )
                    for key, value in data.items()
                ]
            else:
                items = [
                    _php_var_dump(value, depth + 1, ancestors, datetime_format)
                    for value in data
                ]
        finally:
            ancestors.remove(identity)
        return "%sArray(\n%s\n%s)" % (padding, ",\n".join(items), padding)
    if isinstance(data, six.string_types):
        return padding + _php_string(data)
    if isinstance(data, bool):
        return padding + ("true" if data else "false")
    if isinstance(data, six.integer_types):
        return padding + ("%d" % data)
    if data is None:
        return padding + "null"
    if isinstance(data, datetime):
        return padding + _php_datetime(data, datetime_format)
    if isinstance(data, date):
        return padding + _php_string(data.isoformat())
    if isinstance(data, Decimal):
        return padding + _php_string(str(data))
    if isinstance(data, float):
        if math.isnan(data):
            return padding + "NAN"
        if math.isinf(data):
            return padding + ("-INF" if data < 0 else "INF")
        return padding + repr(float(data))
    raise ValueError("Unsupported data type (%s)" % type(data))


def php_var_dump(name, data, datetime_format="timestamp"):
    # type: (str, object, str) -> str
    """Render a PHP assignment using the selected format for datetime values.

    Dates and decimals become strings. PHP can coerce quoted integer-like
    dictionary keys to integers. Store identifiers as values when their string
    type must survive.
    """
    if (
        not isinstance(name, six.string_types)
        or not _VARIABLE_NAME.match(name)
        or name in ("this", "GLOBALS")
    ):
        raise ValueError("Invalid PHP variable name")
    if datetime_format not in _DATETIME_FORMATS:
        raise ValueError(
            "Invalid datetime_format. Use timestamp, timestamp_legacy, or string."
        )
    depth = 1 if isinstance(data, dict) else 0
    return "$%s = %s;" % (
        name,
        _php_var_dump(data, depth=depth, datetime_format=datetime_format),
    )


def php_as_block(stringed_var):
    # type: (str) -> str
    """Wrap PHP source in opening and closing tags."""
    return "<?php\n\n%s\n\n?>" % stringed_var
