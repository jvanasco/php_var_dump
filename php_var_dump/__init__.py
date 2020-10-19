# pypi
import six


__VERSION__ = "0.3.1"


# ==============================================================================


def _php_var_dump(data, depth=0):
    """
    utility function; recursively called.
    depth is used to control the amount of padding.
    This has a limited amount of support for data structures.
    functions, lambas, etc are not supported.
    """
    padding = "  " * depth
    keypadding = "  " * (depth + 1)
    depth += 1
    if isinstance(data, dict):
        items = []
        for i in data:
            item = keypadding + "'%s' => %s" % (i, _php_var_dump(data[i], depth=depth))
            items.append(item)
        items = ",\n".join(items)
        return "%sArray(\n%s\n%s)" % (padding, items, padding)
    elif isinstance(data, (list, tuple)):
        items = []
        for i in data:
            items.append(_php_var_dump(i, depth=depth))
        items = ",\n".join(items)
        return "%sArray(\n%s\n%s)" % (padding, items, padding)
    elif isinstance(data, str):
        return padding + "'%s'" % data
    elif isinstance(data, int):
        return padding + "%s" % data
    elif isinstance(data, bool):
        return padding + "%s" % data
    elif data is None:
        return padding + "null"
    elif isinstance(data, float):
        return padding + "%s" % data
    else:
        if six.PY2:
            if isinstance(data, long):
                return padding + "%s" % data
            elif isinstance(data, unicode):
                return padding + "'%s'" % data
        raise ValueError(
            "Unsupported data type (%s) for data: '%s'" % (type(data), data)
        )


def php_var_dump(name, data):
    """
    php_var_dump
    :param name: name of the function
    :param data: data for the function
    """
    depth = 0
    if isinstance(data, dict):
        depth = 1
    return "$%s = %s;" % (name, _php_var_dump(data, depth=depth))


def php_as_block(stringed_var):
    """
    php_as_block
    :param stringed_var: stringed_var
    """
    return "<?php\n\n%s\n\n?>" % stringed_var
