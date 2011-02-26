Acceptance tests for PHPdomain
##############################

Globals
=======

.. php:global:: $global_var

    A global variable

.. php:const:: SOME_CONSTANT

    A global constant

.. php:function:: in_array(needle, haystack)
    
    Checks for needle in haystack.
    
    :param needle: The element to search for.
    :param array haystack: The array to search.
    :returns boolean: Element exists in array.

Classes
=======

.. php:class:: DateTime

    Datetime class
    
    .. php:method:: setDate($year, $month, $day)
        
        Set the date in the datetime object
        
        :param int $year: The year.
        :param int $month: The month.
        :param int $day: The day.
    
    .. php:method:: setTime($hour, $minute[, $second])
    
        Set the time
        
        :param int $hour: The hour
        :param int $minute: The minute
        :param int $second: The second
    
    .. php:const:: ATOM
    
        Y-m-d\TH:i:sP
    
    .. php:attr:: testattr
    
        Value of some attribute

.. php:class:: OtherClass

    Another class

.. php:method:: OtherClass::staticMethod()

    A static method.

Exceptions
==========

.. php:exception:: InvalidArgumentException

    Throw when you get an argument that is bad.


.. php:namespace:: LibraryName

Namespaced elements
===================

.. php:function:: namespaced_function($one[, $two])

    A function in a namespace
    
    :param string $one: First parameter.
    :param string $two: Second parameter.

.. php:class:: LibraryClass

    A class in a namespace

    .. php:method:: instanceMethod($foo)
    
    An instance method

.. php:method:: LibraryClass::staticMethod()

    A static method in a namespace

Nested namespaces
=================

.. php:namespace:: LibraryName\SubPackage

.. php:class:: SubpackageClass

    A class in a subpackage
    