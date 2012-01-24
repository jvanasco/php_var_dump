r"""
    php_var_dump
    ~~~~~~~~~~~~

    A port of the ``var_dump`` function of php to python.
    
    Why on earth would you want this?!?!?
    =====================================
    
    Imagine that you have to deploy something in php.  You don't have a choice.
    You HAVE to.
    
    php_var_dump lets you do all your data processing and management in python.
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
    
    data_string= "<?php\n\n%s\n\n?>" % as_php
    open('data.php','w').write(data_string.encode( "utf-8" ))
    
    Then just include that file in your php programs.
    
    There's also a php_as_block function, which does the trivial encapsulation as above.
    

    :copyright: 2012 by Jonathan Vanasco
    license: BSD
"""

import types

def _php_var_dump(data,depth=0):
    """ utility function; recursively called.  depth is used to control the amount of padding. 
    This has a limited amount of support for data structures. functions, lambas, etc are not supported
    """
    padding= "  "*depth
    keypadding= "  "*(depth+1)
    depth+= 1
    if ( type(data) == types.DictType ) or ( type(data) == types.DictionaryType ):
        items = []
        for i in data :
            item = keypadding + "'%s' => %s" % (i,_php_var_dump(data[i],depth=depth))
            items.append(item)
        items = ',\n'.join(items)
        return '%sArray(\n%s\n%s)' % ( padding, items, padding)
    elif ( type(data) == types.ListType ) or ( type(data) == types.TupleType ):
        items = []
        for i in data :
            items.append(_php_var_dump(i,depth=depth))
        items = ',\n'.join(items)
        return '%sArray(\n%s\n%s)' % ( padding, items, padding)
    elif type(data) == types.StringType :
        return padding + "'%s'" % data
    elif type(data) == types.UnicodeType :
        return padding + "'%s'" % data
    elif type(data) == types.IntType :
        return padding + "%s" % data
    elif type(data) == types.BooleanType :
        return padding + "%s" % data
    elif type(data) == types.NoneType :
        return padding + "null"
    elif type(data) == types.LongType :
        return padding + "%s" % data
    elif type(data) == types.FloatType :
        return padding + "%s" % data
    else:
        raise ValueError("Unsupported data type (%s) for data : '%s'" % ( type(data) , data ))


def php_var_dump(name,data):
    """ php_var_dump """
    depth=0
    if type(data) == types.DictType:
        depth= 1
    return "$%s = %s;" % ( name , _php_var_dump(data,depth=depth) )
    

def php_as_block(stringed_var):
    return "<?php\n\n%s\n\n?>" % stringed_var
    