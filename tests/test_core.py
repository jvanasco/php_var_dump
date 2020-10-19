# stdlib
import unittest

# pypi
import six

# local
import php_var_dump
from php_var_dump import php_var_dump


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
        lambdad = lambda x: x ** 2
        self.assertRaises(ValueError, lambda: php_var_dump("lambdad", lambdad))
