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


Test Case - Global symbols with no namespaces
---------------------------------------------

:php:global:`$global_var`

:php:const:`SOME_CONSTANT`

:php:func:`in_array`

:php:class:`DateTime`

:php:func:`DateTime::setTime()`

:php:func:`~DateTime::setDate()`

:php:func:`DateTime::ATOM`

:php:func:`DateTime::$testattr`

:php:func:`OtherClass::staticMethod`


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


Test Case - not including namespace
-----------------------------------

:php:func:`namespaced_function()`

:php:class:`LibraryClass`

:php:class:`~LibraryName\\LibraryClass`

:php:func:`LibraryClass::instanceMethod`

:php:func:`LibraryClass::staticMethod()`


Test Case - global access
-------------------------

:php:class:`DateTime`

:php:func:`DateTime::setTime()`

:php:global:`$global_var`

:php:const:`SOME_CONSTANT`


Nested namespaces
=================

.. php:namespace:: LibraryName\SubPackage

.. php:class:: SubpackageClass

    A class in a subpackage


Test Case - Test subpackage links
---------------------------------

:php:class:`SubpackageClass`

:php:class:`LibraryName\\SubPackage\\SubpackageClass`
