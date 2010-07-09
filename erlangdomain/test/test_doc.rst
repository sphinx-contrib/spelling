===============
Acceptance Test
===============

If all links are valid, test is done successfully.

Global(erlang module's contents)
================================

.. erl:function:: function_out_of_module

.. erl:module:: test_module

Single Module 'test_module'
===========================

.. erl:function:: module_function(Identifier)

   test
   
   :param Identifier: identify sender
   :type  Identifier: str
   :return: status
   :rtype:  atom()

.. erl:function:: variable_function(Name[, Optition]) -> ok

   test

   :param Name: identify sender
   :type  Name: str
   :param Option: option param
   :type  Option: atom()


.. erl:macro:: HostName
   
   Host name of test server.

.. erl:record:: #user_address

   It contains user name, e-mail, address and so on

Test Case - Access Without Module Name in Same Module
-----------------------------------------------------

:erl:mod:`test_module`

:erl:func:`module_function/1`

:erl:func:`variable_function/1`

:erl:func:`variable_function/2`

:erl:macro:`HostName`

:erl:record:`#user_address`

Test Case - Access to Default Module Name
-----------------------------------------

:erl:func:`erlang:function_out_of_module/0`

.. erl:module dummy_other_module

Test Case - Access With Module Name in Other Module
---------------------------------------------------

:erl:mod:`test_module`

:erl:func:`test_module:module_function`

:erl:func:`test_module:module_function/1`

:erl:func:`test_module:variable_function/1`

:erl:func:`test_module:variable_function/2`

:erl:func:`test_module:variable_function`

:erl:macro:`test_module:HostName`

:erl:record:`test_module:#user_address`


