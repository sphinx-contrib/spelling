PHP Domain
##########

:author: Mark Story <mark at mark-story.com>

About
=====

A domain for sphinx >= 1.0 that provides language support for PHP.

PHP Domain supports following objects:

* Global variable
* Global function
* Constant
* Namespace

  * Function
  * Class

* Class

  * Class constant
  * Instance methods
  * Static methods
  * Properties

.. note::

   This domain expresses methods and attribute names like this::

      Class::method_name
      Class::$attribute_name

   You address classes/functions in namespaces using \\ syntax as you would in PHP::

        Package\Subpackage\Class

URLs
====

:PyPI: http://pypi.python.org/pypi/sphinxcontrib-phpdomain
:Detail Document: http://packages.python.org/sphinxcontrib-phpdomain

Quick Sample
============

This is source::

  .. php:class:: DateTime

    Datetime class

    .. php:method:: setDate($year, $month, $day)

        Set the date.

        :param int $year: The year.
        :param int $month: The month.
        :param int $day: The day.
        :returns: Either false on failure, or the datetime object for method chaining.


    .. php:method:: setTime($hour, $minute[, $second])

        Set the time.

        :param int $hour: The hour
        :param int $minute: The minute
        :param int $second: The second
        :returns: Either false on failure, or the datetime object for method chaining.

    .. php:const:: ATOM

        Y-m-d\TH:i:sP

Result
-----------------

.. php:class:: DateTime

  Datetime class

  .. php:method:: setDate($year, $month, $day)

      Set the date.

      :param int $year: The year.
      :param int $month: The month.
      :param int $day: The day.
      :returns: Either false on failure, or the DateTime object for method chaining.


  .. php:method:: setTime($hour, $minute[, $second])

      Set the time.

      :param int $hour: The hour
      :param int $minute: The minute
      :param int $second: The second
      :returns: Either false on failure, or the DateTime object for method chaining.

  .. php:const:: ATOM

      Y-m-d\TH:i:sP

Cross referencing
-----------------

From other place, you can create cross reference like that::

   You can modify a DateTime's date using :php:meth:`DateTime::setDate`.

Result
-----------

You can modify a DateTime's date using :php:meth:`DateTime::setDate`.

Install
=======

You can install the phpdomain using easy_install::

   easy_install -U sphinxcontrib-phpdomain

