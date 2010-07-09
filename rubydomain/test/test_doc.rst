===============
Acceptance Test
===============

If all links are valid, test is done successfully.

Global
======

.. rb:global:: $global_variable

.. rb:const:: ConstOutofModule

.. rb:class:: ClassOutofModule

   :ivar name: name
   
.. rb:function:: function_out_of_module

.. rb:module:: SingleModule

Single Module 'SingleModule'
============================

.. rb:function:: module_function(identifier[, ...])

   test
   
   :param identifier: identify sender
   :type  identifier: str


.. rb:global:: $host

   HostName of Server


.. rb:method:: module_method(host)

   :param host: URI
   :type  host: str


.. rb:class:: ClassInModule

   .. rb:classmethod:: new(identifier[, shared=false])
   
      rb:classmethod document

      :param identifier: receive message filter Identifier.
      :type  identifier: str

   .. rb:method:: empty?
   
      normal method
      
      :return: ``true`` if the queue object is empty.
      :rtype:  Boolean
      
   .. rb:attr_reader:: name
   
   .. rb:attr_writer:: addr
   
   .. rb:attr_accessor:: phone


Test Case - Access Without Module Name(1)
-----------------------------------------

:rb:global:`$global_variable`

:rb:const:`ConstOutofModule`

:rb:class:`ClassOutofModule`

:rb:func:`function_out_of_module`

:rb:func:`module_function`

:rb:meth:`module_method`

:rb:global:`$host`

:rb:class:`ClassInModule`

:rb:meth:`ClassInModule#empty?`

:rb:attr:`ClassInModule#name`, :rb:attr:`ClassInModule#addr`,
:rb:attr:`ClassInModule#phone`


Nested Module 'SingleModule::NestedModule'
==========================================

.. rb:module:: SingleModule::NestedModule

.. rb:class:: InnderClass

   class difinition.
   
   :cvar host_name: my host name

   .. rb:attr_writer:: port_number

   .. rb:method:: format(message)

   You should override this method to change message format.

Test Case - Access Without Module Name(2)
-----------------------------------------

:rb:class:`InnderClass`

:rb:attr:`InnderClass#port_number`

:rb:meth:`InnderClass#format`

Test Case - Global Reference
----------------------------

:rb:global:`$global_variable`

:rb:const:`ConstOutofModule`

:rb:class:`ClassOutofModule`

:rb:func:`function_out_of_module`


Test Case - Access With Module Name in Other Module
---------------------------------------------------

:rb:mod:`SingleModule`

:rb:func:`SingleModule.module_function`

:rb:meth:`SingleModule#module_method`

:rb:global:`$host`

:rb:class:`SingleModule::ClassInModule`

:rb:meth:`SingleModule::ClassInModule#empty?`

:rb:attr:`SingleModule::ClassInModule#name`

:rb:attr:`SingleModule::ClassInModule#addr`

:rb:attr:`SingleModule::ClassInModule#phone`

Test Case - Access With Module Name to Objects in Nested Module
---------------------------------------------------------------

:rb:mod:`SingleModule::NestedModule`

:rb:class:`SingleModule::NestedModule::InnderClass`

:rb:attr:`SingleModule::NestedModule::InnderClass#port_number`

:rb:meth:`SingleModule::NestedModule::InnderClass#format`
