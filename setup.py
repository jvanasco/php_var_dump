import os
from setuptools import setup

def get_docs():
    result = []
    in_docs = False
    f = open(os.path.join(os.path.dirname(__file__), 'php_var_dump.py'))
    try:
        for line in f:
            if in_docs:
                if line.lstrip().startswith(':copyright:'):
                    break
                result.append(line[4:].rstrip())
            elif line.strip() == 'r"""':
                in_docs = True
    finally:
        f.close()
    return '\n'.join(result)

setup(
    name='php_var_dump',
    author='Jonathan Vanasco',
    author_email='jonathan@findmeon.com',
    version='0.1',
    url='http://github.com/jvanasco/php_var_dump',
    py_modules=['php_var_dump'],
    description='a port of the var_dump function of php to python.',
    long_description=get_docs(),
    zip_safe=False,
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: PHP',
        'Programming Language :: Python',
    ]
)
