Reference
=========

.. highlight:: rst

The Erlang Domain
-----------------

The Erlang domain (name **erl**) provides the following directives for module
declarations. Almost all directives are similar to Python's.

.. rst:directive:: .. erl:module:: name

   This directive marks the beginning of the description of a module.
   This directive can accept nested modules(separated by ``::``).
   It does not create content (like e.g. :rst:dir:`erl:class` does).

   This directive will also cause an entry in the global module index.

   It has ``platform`` option, ``synopsis`` option and ``deprecated`` option as same as
   :rst:dir:`py:module`.


.. rst:directive:: .. erl:currentmodule:: name

   .. seealso:: :rst:dir:`py:currentmodule`

The following directives are provided for module level contents:

.. rst:directive:: .. erl:function:: name(signature)

   Describes a module-level function. Usage of this directive is almost as 
   same as Python's one.

   If this directive is out of :rst:dir:`erl:module` directive, 
   It is belong to "erlang" module automatically in Erlang's rule.
   
   .. code-block:: rst

      .. erl:function:: run_test(testname[, options])

         This function launch test.

   You can use ``:erl:func:`` roles to reference Erlang functions.
   But this role can accept **arity** in Erlang's customary way.
   If you don't add arity, This role search function whose arity id minimum.

   .. code-block:: rst

      You should call :erl:func:`run_test/1` to run test.

   Above funciton description has two arities,  /1 and /2. Both roles can refer
   above description.
   
   .. seealso:: .. py:function:: name


.. rst:directive:: .. erl:record:: name

   Record name starts with '#' charactor.

   .. code-block:: rst

      .. erl:record:: #person

         This records include name, address, phone number.


.. rst:directive:: .. erl:macro:: name

   Macro name starts with capital charactors.

   .. code-block:: rst

      .. erl:macro:: HostUrl

         Host address(URI format)


Info field lists
~~~~~~~~~~~~~~~~

Erlang domain has field lists as same as Python domain except ``key``, 
``keyword``.

Cross-referencing Erlang objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following roles refer to objects in modules and are possibly hyperlinked if
a matching identifier is found:

.. rst:role:: erl:mod

   Reference a module. Erlang domain doesn't support nested module name.

.. rst:role:: erl:func

   Reference a Erlang function; a name with module may be used.
   Usually role text includes trailing arity number like 
   ``:erl:func:`eggs:counter/1`. 
   If you don't add arity, this role search the function description whose
   name is same and arity is minimum.

.. rst:role:: erl:record

   Reference a record whose name has ``#`` prefix.
   
.. rst:role:: erl:macro

   Reference a macro(defined by ``-define`` directive in Erlang)
   whose name starts with capital charactor.


