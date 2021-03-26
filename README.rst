php_var_dump
~~~~~~~~~~~~

![Python package](https://github.com/jvanasco/php_var_dump/workflows/Python%20package/badge.svg)

A port of the `var_dump` function of PHP to Python.

This module allows you to "dump" trivial Python objects into PHP code.

Why? So you can use Python to write fast PHP websites when you need to run PHP websites.

Sometimes you need to run a PHP website.  


Why on earth would you want this?!?!?
=====================================

Imagine that you have to deploy something in PHP.  You don't have a choice.
You HAVE to.

`php_var_dump` lets you do all your data processing and management in Python.
You can then convert your native Python data structures into PHP code,
which can then be saved as include fles for PHP.

Other Python modules that can accomplish the general idea:

* phpserialize
  implements the PHP serialize/unserialize functions in Python
  allows you to serialize a Python data structure to PHP
  allows you to unserialize a php data structure to Python

* simplejson
  there are json parsers in PHP, which can read code you save

The main benefit of using the var_dump method, is that there is no overhead
in loading/unloading/parsing/etc.

This method allows you to build a PHP include file that simply runs fast,
and that can use multiple includes within the filesystem as a "database"
like system. This way you don't have to set up any databases, libraries,
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

There's also a `php_as_block` function, which does the trivial encapsulation as above.

:copyright: 2012 by Jonathan Vanasco
:license: BSD

Changelog
=========

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
