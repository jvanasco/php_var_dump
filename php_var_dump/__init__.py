r"""\
php_var_dump
~~~~~~~~~~~~

A port of the ``var_dump`` function of php to python.

Why on earth would you want this?!?!?
=====================================

Imagine that you have to deploy something in php.  You don't have a choice.
You HAVE to.

`php_var_dump` lets you do all your data processing and management in python.
You can then convert your native python data structures into php code,
which can then be saved as include fles for php.

Other python modules that can accomplish the general idea:
    phpserialize
        implements the PHP serialize/unserialize functions in python
        allows you to serialize a python data structure to PHP
        allows you to unserialize a php data structure to Python
    simplejson
        there are json parsers in php, which can read code you save

The main benefit of using the var_dump method, is that there is no overhead
in loading/unloading/parsing/etc.

This method allows you to build a php include file that simply runs fast,
and that can use multiple includes within the filesystem as a "database"
like system. This way you don't have to set up any databases, libraries,
or whatever - you can just deploy PHP code without coding much in PHP.

Usage
=====

>>> from php_var_dump import php_var_dump
>>> data= "Hello World"
>>> as_php = php_var_dump( 'var', data )
>>> print as_php
$var = 'Hello World';

You'd probable then want to save it...

    data_string = "<?php\n\n%s\n\n?>" % as_php
    open('data.php', 'w').write(data_string.encode( "utf-8" ))

Then just include that file in your php programs.

There's also a `php_as_block` function, which does the trivial encapsulation as above.

:copyright: 2012 by Jonathan Vanasco
license: BSD
"""

import six
import types


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