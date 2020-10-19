"""
php_var_dump installation script.
"""
import os
import re

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

# store version in the init.py
with open(
    os.path.join(os.path.dirname(__file__), "php_var_dump", "__init__.py")
) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)

requires = [
    "six",
]
tests_require = []
testing_extras = tests_require + [
    "pytest",
]

setup(
    name="php_var_dump",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    version=VERSION,
    url="http://github.com/jvanasco/php_var_dump",
    description="A port of the var_dump function of PHP to Python.",
    long_description=README,
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: PHP",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
