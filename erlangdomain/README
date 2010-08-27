=============
Erlang Domain
=============

:author: SHIBUKAWA Yoshiki <yoshiki at shibu.jp>

About
=====

This is the Erlang domain for Sphinx 1.0.
Sphinx 1.0 will deliver new feature -- Domain.
It will enable other language support except Python and C language.

This extension provides directives and roles to write Erlang documents.

Erlang Domain supports following objects:

* Module

  * Function
  * Macro
  * Record
  
.. note::

   This domain expresses module structure like this::

      module:function_name/0
      module:#record_name
      module:MacroName

URLs
====

:PyPI: http://pypi.python.org/pypi/sphinxcontrib-erlangdomain
:Detail Document: http://packages.python.org/sphinxcontrib-erlangdomain

Quick Sample
============

.. note::
   These contents is copied from http://www.erlang.org/doc/man/lists.html

This is source::

  .. erl:module:: lists

  .. erl:function:: append(ListOfLists) -> List1

     :type ListOfLists: [[term()]] 
     :rtype: [term()]

     Returns a list in which all the sub-lists of ListOfLists 
     have been appended. For example:

     .. code-block:: erlang

        > lists:append([[1, 2, 3], [a, b], [4, 5, 6]]).
        [1,2,3,a,b,4,5,6]

  .. erl:function:: append(List1, List2) -> List3

     :param List1: First Item
     :type List1: [term()]
     :param List2: Second Item
     :type List2: [term()]
     :rtype: [term()]

     Returns a new list List3 which is made from the elements 
     of List1 followed by the elements of List2. For example:

     .. code-block:: erlang

        > lists:append("abc", "def").
        "abcdef"

     ``lists:append(A, B)`` is equivalent to ``A ++ B``.

-----------------

.. erl:module:: lists

.. erl:function:: append(ListOfLists) -> List1

   :type ListOfLists: [[term()]]
   :rtype: [term()]

   Returns a list in which all the sub-lists of ListOfLists
   have been appended. For example:         

   .. code-block:: erlang

      > lists:append([[1, 2, 3], [a, b], [4, 5, 6]]).
      [1,2,3,a,b,4,5,6]

.. erl:function:: append(List1, List2) -> List3

   :param List1: First Item
   :type List1: [term()]
   :param List2: Second Item
   :type List2: [term()]
   :rtype: [term()]

   Returns a new list List3 which is made from the elements 
   of List1 followed by the elements of List2. For example:

   .. code-block:: erlang

      > lists:append("abc", "def").
      "abcdef"

   ``lists:append(A, B)`` is equivalent to ``A ++ B``.

------------------

From other place, you can create cross reference like that::

  followed by List2. Looking at how :erl:func:`lists:append/1` 
  or ``++`` would be implemented in plain Erlang, 
  it can be seen clearly that the first list is copied.

Result:

-----------

followed by List2. Looking at how :erl:func:`lists:append/1`
or ``++`` would be implemented in plain Erlang,
it can be seen clearly that the first list is copied.

-----------

Install
=======

.. code-block:: bash

   $ easy_install -U sphinxcontrib-erlangdomain

