import os
from setuptools import setup
from setuptools import find_packages


def get_docs():
    result = []
    in_docs = False
    f = open(os.path.join(os.path.dirname(__file__), "php_var_dump/__init__.py"))
    try:
        for line in f:
            if in_docs:
                if line.lstrip().startswith(":copyright:"):
                    break
                result.append(line[4:].rstrip())
            elif line.strip() == 'r"""':
                in_docs = True
    finally:
        f.close()
    return "\n".join(result)


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
    version="0.3",
    url="http://github.com/jvanasco/php_var_dump",
    description="a port of the var_dump function of php to python.",
    long_description=get_docs(),
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
