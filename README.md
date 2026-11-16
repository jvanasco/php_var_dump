# php_var_dump

![Python package](https://github.com/jvanasco/php_var_dump/workflows/Python%20package/badge.svg)

`php_var_dump` converts Python values into PHP source code you can write to an
include file. It was originally built to turn state-specific voting data from
CSV files into PHP includes for voter registration sites and advertising
widgets. The Python ingestion tool prepares the data ahead of deployment, and
PHP loads the generated file without having to parse the original CSV or
decode a serialized payload on each request.

## Usage

```python
from php_var_dump import php_as_block, php_var_dump

assignment = php_var_dump("message", "Hello World")
with open("data.php", "wb") as output:
    output.write(php_as_block(assignment).encode("utf-8"))
```

The generated `data.php` contains:

```php
<?php

$message = 'Hello World';

?>
```

Include the generated file in your PHP program:

```php
<?php

require __DIR__ . '/data.php';
echo $message;
```

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

## PHP value boundaries

**Array keys.** PHP can convert a quoted integer key such as `'12345'` to
the integer `12345`. Leading-zero keys such as `'01234'` and ZIP+4 or precinct
keys such as `'12345-6789'` and `'42-07'` stay strings. If every identifier
must remain a string, store it as a record value. If it must be a key, use a
consistent nonnumeric prefix. [PHP array key rules](https://www.php.net/manual/en/language.types.array.php)

PHP may represent integers outside its integer range as floats, which can
lose precision.

## Changelog

### v1.0.0

* Build with setuptools through `pyproject.toml` and keep package metadata and
  tox settings in `setup.cfg`.
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

### v0.3.2

* Packaging fixes.

### v0.3.1

* Packaging fixes.

### v0.3

* Upgraded Black to 20.8b1.
* Integrated with pre-commit.
* Added tox and GitHub Actions.
* Added Python 3 support.

### v0.2

* Added Flake8.

### v0.1

* Initial release.

## License

MIT. Copyright 2012–2026 Jonathan Vanasco.
