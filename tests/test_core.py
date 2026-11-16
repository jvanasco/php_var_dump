# stdlib
import unittest
from datetime import date, datetime
from decimal import Decimal

# pypi
import six

# local
import php_var_dump
from php_var_dump import php_var_dump
from tests import FixedOffset

# ==============================================================================


class TestVarDump(unittest.TestCase):
    """
    Since we're printing strings, which could be sorted any-which-way, the easiest way to test (short of embedding a php interpreter) is to just see if we trigger an error.
    """

    def test_string(self):
        string = "a"
        as_var = php_var_dump("string", string)

    if six.PY2:

        def test_string_unicode(self):
            string = "a"
            string = unicode(string)
            as_var = php_var_dump("string", string)

        def test_string_utf8(self):
            string = "a"
            string = unicode(string, "utf-8")
            as_var = php_var_dump("string", string)

    def test_int(self):
        int = 1
        as_var = php_var_dump("int", int)

    def test_list(self):
        list = ["a", "b"]
        as_var = php_var_dump("list", list)

    def test_list_of_lists(self):
        list_of_lists = ["a", ["1", "2"], "b", ["3", "4"], "c"]
        as_var = php_var_dump("list_of_lists", list_of_lists)

    def test_tuple(self):
        tuple = (1, 2, 3)
        as_var = php_var_dump("tuple", tuple)

    def test_dict(self):
        dict = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        as_var = php_var_dump("dict", dict)

    def test_none(self):
        none = None
        as_var = php_var_dump("none", none)

    def test_bool(self):
        bool = True
        as_var = php_var_dump("bool", bool)
        bool = False
        as_var = php_var_dump("bool", bool)

    if six.PY2:

        def test_long(self):
            longed = long(1.99123)
            as_var = php_var_dump("longed", longed)

    def test_float(self):
        floated = float(2.912)
        as_var = php_var_dump("floated", floated)

    def test_def(self):
        """This should fail!"""

        def deffed():
            return 1

        self.assertRaises(ValueError, lambda: php_var_dump("deffed", deffed))

    def test_lambda(self):
        """This should fail!"""
        lambdad = lambda x: x**2
        self.assertRaises(ValueError, lambda: php_var_dump("lambdad", lambdad))

    def test_php_string_literals(self):
        # type: () -> None
        """Escape quotes and backslashes in both value and key literals."""
        key = "key'\\"
        value = b"caf\xe9'\\$name".decode("latin-1")
        expected = b"$data = 'caf\xe9\\'\\\\$name';".decode("latin-1")
        self.assertEqual(php_var_dump("data", value), expected)
        self.assertIn(r"'key\'\\' =>", php_var_dump("data", {key: value}))

    def test_invalid_assignment_names(self):
        # type: () -> None
        """Reject malformed and read-only assignment names."""
        for name in (
            "",
            "0value",
            "$value",
            "two words",
            "value\n",
            "this",
            "GLOBALS",
            1,
        ):
            self.assertRaises(ValueError, php_var_dump, name, 1)

    def test_php_scalar_literals(self):
        # type: () -> None
        """Render booleans and non-finite floats as PHP literals."""
        for value, literal in (
            (True, "true"),
            (False, "false"),
            (float("inf"), "INF"),
            (float("-inf"), "-INF"),
            (float("nan"), "NAN"),
        ):
            self.assertEqual(php_var_dump("value", value), "$value = %s;" % literal)

    def test_recursive_and_shared_containers(self):
        # type: () -> None
        """Detect cycles while allowing the same value in separate branches."""
        shared = [1]
        self.assertEqual(php_var_dump("data", [shared, shared]).count("Array("), 3)
        shared.append({"cycle": shared})
        self.assertRaises(ValueError, php_var_dump, "data", shared)

    def test_datetime_encodings(self):
        # type: () -> None
        """Encode an aware datetime in all three formats."""
        value = datetime(1970, 1, 1, 1, tzinfo=FixedOffset())
        self.assertEqual(
            php_var_dump("date", value),
            "$date = \\DateTimeImmutable::createFromTimestamp(0);",
        )
        self.assertEqual(
            php_var_dump("date", value, datetime_format="timestamp_legacy"),
            "$date = new \\DateTimeImmutable('@0');",
        )
        self.assertEqual(
            php_var_dump("date", value, datetime_format="string"),
            "$date = '1970-01-01T01:00:00+01:00';",
        )

    def test_datetime_naive_and_invalid_format(self):
        # type: () -> None
        """Allow naive strings and reject ambiguous timestamps and unknown modes."""
        value = datetime(1970, 1, 1)
        self.assertEqual(
            php_var_dump("date", value, datetime_format="string"),
            "$date = '1970-01-01T00:00:00';",
        )
        self.assertRaises(ValueError, php_var_dump, "date", value)
        self.assertRaises(
            ValueError, php_var_dump, "date", value, datetime_format="timestamp_legacy"
        )
        self.assertRaises(
            ValueError, php_var_dump, "date", 1, datetime_format="invalid"
        )

    def test_date_is_independent_of_datetime_format(self):
        # type: () -> None
        """Render a calendar date as an ISO string in each datetime mode."""
        for mode in ("timestamp", "timestamp_legacy", "string"):
            self.assertEqual(
                php_var_dump("day", date(2028, 2, 29), datetime_format=mode),
                "$day = '2028-02-29';",
            )

    def test_decimal_uses_exact_string_representation(self):
        # type: () -> None
        """Preserve decimal precision, scale, and special values as text."""
        for text in (
            "12345678901234567890.1200",
            "-0.00",
            "1E-1000000",
            "Infinity",
            "NaN",
        ):
            self.assertEqual(
                php_var_dump("amount", Decimal(text)),
                "$amount = '%s';" % text,
            )
