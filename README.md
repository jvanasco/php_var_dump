php_var_dump
~~~~~~~~~~~~

![Python package](https://github.com/jvanasco/php_var_dump/workflows/Python%20package/badge.svg)

A port of the `var_dump` function of PHP to Python.

This module allows you to "dump" trivial Python objects into PHP code.

Why? So you can use Python to write fast PHP websites when you need to run PHP websites.

Sometimes you need to run a PHP website.  


Why on earth would you want this?!?!?
=====================================

Imagine that you have to deploy something in PHP.
You don't have a choice.
You HAVE to.

`php_var_dump` lets you do all your data processing and management in Python.
You then convert your native Python data structures into native PHP code,
which can then be saved as include fles for PHP.

Other Python modules that can accomplish the general idea:

* `phpserialize`
  Implements the PHP serialize/unserialize functions in Python.
  Allows you to serialize a Python data structure to PHP.
  Allows you to unserialize a php data structure to Python.

* `json` / `simplejson`
  There are json parsers in PHP, which can read code you save.

The main benefit of using the var_dump method, is that there is no overhead
in loading/unloading/parsing/etc.

This method allows you to build a PHP include file that simply runs fast,
and that can use multiple includes within the filesystem as a database-like
system. This way you don't have to set up any databases, libraries,
or whatever - you can just deploy PHP code without coding much in PHP.

Usage
=====

.. code-block:: python

	from php_var_dump import php_var_dump
	data = "Hello World"
	as_php = php_var_dump('var', data )
	print(as_php)

That will generate valid PHP code:

.. code-block:: php

	$var = 'Hello World';

You'd probable then want to save it...

.. code-block:: python

    data_string = "<?php\n\n%s\n\n?>" % as_php
    open('data.php', 'w').write(data_string.encode( "utf-8" ))

Then just include the `data.php` file in your PHP programs.

`php_as_block()` wraps raw PHP source in PHP tags. Serialize data with
`php_var_dump()` before passing the resulting assignment to `php_as_block()`.

### Datetime values

Pass `datetime_format` to `php_var_dump()` to select how it encodes every
Python `datetime` in the assignment, including values nested in containers.

| Format | PHP output |
| --- | --- |
| `"timestamp"` (default) | A `DateTimeImmutable` created with `createFromTimestamp()`. Requires PHP 8.4 or later. |
| `"timestamp_legacy"` | A `DateTimeImmutable` created with an `@timestamp` string. Use this for PHP 8.3 and earlier. |
| `"string"` | A quoted ISO 8601 string with the original UTC offset when present. |

Both timestamp modes require a timezone-aware datetime and preserve the instant
and microseconds in UTC. The string mode also accepts naive datetimes, whose
output has no UTC offset.

```python
from datetime import datetime, timezone
from php_var_dump import php_var_dump

value = datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc)
php_var_dump("value", value)
php_var_dump("value", value, datetime_format="timestamp_legacy")
php_var_dump("value", value, datetime_format="string")
```

### Calendar dates and exact decimals

`datetime.date` values become `YYYY-MM-DD` strings in every datetime mode.
`decimal.Decimal` values become strings using Python's decimal representation,
which preserves precision, trailing zeros, and exponent notation when present.
For example, `Decimal("12.3400")` produces the PHP string `'12.3400'`.
Non-finite decimals also become strings, such as `'Infinity'` and `'NaN'`.

### PHP value boundaries

**Array keys.** PHP can convert a quoted integer key such as `'12345'` to
the integer `12345`. Leading-zero keys such as `'01234'` and ZIP+4 or precinct
keys such as `'12345-6789'` and `'42-07'` stay strings. If every identifier
must remain a string, store it as a record value. If it must be a key, use a
consistent nonnumeric prefix. [PHP array key rules](https://www.php.net/manual/en/language.types.array.php)

PHP may represent integers outside its integer range as floats, which can
lose precision.

:copyright: 2012-2026 by Jonathan Vanasco
:license: MIT

Changelog
=========

v1.0.0
----------

* Build with setuptools through ``pyproject.toml`` and keep package metadata and
  tox settings in ``setup.cfg``.
* Install `six` in isolated Python 2 builds so setuptools can read the version.
* Align the tox and GitHub Actions matrices through Python 3.15 and generate
  HTML coverage reports.
* Escape strings and dictionary keys, validate assignment names, emit PHP
  boolean and non-finite float literals, and reject recursive containers.
* Add optional PHP CLI round-trip tests for nested values and numeric boundaries.
* Encode datetimes as PHP 8.4+ timestamps by default, with legacy timestamp and
  ISO 8601 string options. Run PHP round-trip tests in the Python 3.14 CI job.
* Encode calendar dates and decimals as strings and document PHP array key
  coercion for identifiers.
* MIT License

v0.3.2
* packaging fixes

v0.3.1
* packaging fixes

v0.3
* upgraded black; 20.8b1
* integrated with pre-commit
* tox, github actions
* python3 support

v0.2
* flake8

v0.1
* initial
