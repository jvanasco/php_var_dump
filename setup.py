"""
php_var_dump installation script.
"""
import os
import re

from setuptools import setup
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

long_description = (
    description
) = "A port of the var_dump function of PHP to Python. This lets you make PHP files with Python."
with open(os.path.join(HERE, "README.rst")) as fp:
    long_description = fp.read()

# store version in the init.py
with open(os.path.join(HERE, "src", "php_var_dump", "__init__.py")) as v_file:
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
    description=description,
    long_description=long_description,
    license="BSD",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
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
