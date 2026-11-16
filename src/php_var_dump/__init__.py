"""Serialize simple Python values as PHP source code."""

import math
import re

import six

__VERSION__ = "1.0.0"

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


def _php_var_dump(data, depth=0, ancestors=None):
    # type: (object, int, set[int] | None) -> str
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
                        _php_var_dump(value, depth + 1, ancestors),
                    )
                    for key, value in data.items()
                ]
            else:
                items = [_php_var_dump(value, depth + 1, ancestors) for value in data]
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
    if isinstance(data, float):
        if math.isnan(data):
            return padding + "NAN"
        if math.isinf(data):
            return padding + ("-INF" if data < 0 else "INF")
        return padding + repr(float(data))
    raise ValueError("Unsupported data type (%s)" % type(data))


def php_var_dump(name, data):
    # type: (str, object) -> str
    """Render a PHP assignment for a variable name without a dollar prefix."""
    if (
        not isinstance(name, six.string_types)
        or not _VARIABLE_NAME.match(name)
        or name in ("this", "GLOBALS")
    ):
        raise ValueError("Invalid PHP variable name")
    depth = 1 if isinstance(data, dict) else 0
    return "$%s = %s;" % (name, _php_var_dump(data, depth=depth))


def php_as_block(stringed_var):
    # type: (str) -> str
    """Wrap PHP source in opening and closing tags."""
    return "<?php\n\n%s\n\n?>" % stringed_var
