Acceptance tests for PHPdomain
##############################

Globals
=======

.. php:global:: $global_var

    A global variable

.. php:const:: SOME_CONSTANT

    A global constant

.. php:const:: VALUE

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

Interfaces
==========

.. php:interface:: DateTimeInterface

    Datetime interface

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

.. php:interface:: OtherInterface

    Another interface

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

:php:exc:`InvalidArgumentException`

:php:interface:`DateTimeInterface`

:php:func:`DateTimeInterface::setTime()`

:php:func:`~DateTimeInterface::setDate()`

:php:func:`DateTimeInterface::ATOM`

:php:func:`DateTimeInterface::$testattr`

:php:func:`OtherInterface`

.. php:namespace:: LibraryName

Namespaced elements
===================

.. php:function:: namespaced_function($one[, $two])

    A function in a namespace

    :param string $one: First parameter.
    :param string $two: Second parameter.

.. php:const:: NS_CONST

   A constant in a namespace

.. php:class:: LibraryClass

    A class in a namespace

    .. php:method:: instanceMethod($foo)

    An instance method

    .. php:const:: TEST_CONST

    Test constant

    .. php:attr:: property

    A property!

.. php:method:: LibraryClass::staticMethod()

    A static method in a namespace

.. php:interface:: LibraryInterface

    A interface in a namespace

    .. php:method:: instanceMethod($foo)

Test Case - not including namespace
-----------------------------------

:php:ns:`LibraryName`

:php:func:`namespaced_function()`

:php:const:`NS_CONST`

:php:class:`LibraryClass`

:php:class:`~LibraryName\\LibraryClass`

:php:func:`LibraryClass::instanceMethod`

:php:func:`LibraryClass::staticMethod()`

:php:attr:`LibraryClass::$property`

:php:const:`LibraryClass::TEST_CONST`

:php:interface:`LibraryInterface`

:php:interface:`~LibraryName\\LibraryInterface`

:php:func:`LibraryInterface::instanceMethod`

Test Case - global access
-------------------------

:php:class:`DateTime`

:php:func:`DateTime::setTime()`

:php:global:`$global_var`

:php:const:`SOME_CONSTANT`

:php:attr:`LibraryName\\LibraryClass::$property`

:php:const:`LibraryName\\LibraryClass::TEST_CONST`

:php:const:`LibraryName\\NS_CONST`

:php:interface:`DateTimeInterface`

:php:func:`DateTimeInterface::setTime()`

Nested namespaces
=================

.. php:namespace:: LibraryName\SubPackage

.. php:class:: SubpackageClass

    A class in a subpackage

.. php:interface:: SubpackageInterface

    A class in a subpackage

Test Case - Test subpackage links
---------------------------------

:php:ns:`LibraryName\\SubPackage`

:php:class:`SubpackageClass`

:php:class:`LibraryName\\SubPackage\\SubpackageClass`

:php:interface:`SubpackageInterface`

:php:class:`LibraryName\\SubPackage\\SubpackageInterface`
