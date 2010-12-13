Reference
=========

.. highlight:: rst

The Erlang domain (name **erl**) provides the following directives for module
declarations. Almost all directives are similar to Python's.

.. rst:directive:: .. erl:module:: name

   This directive marks the beginning of the description of a module.
   This directive can accept nested modules(separated by ``::``).
   It does not create content (like e.g. :rst:dir:`erl:class` does).

   This directive will also cause an entry in the global module index.

   It has ``platform`` option, ``synopsis`` option and ``deprecated`` 
   option as same as :rst:dir:`py:module`.


.. rst:directive:: .. erl:currentmodule:: name

   .. seealso:: :rst:dir:`py:currentmodule`

The following directives are provided for module level contents:

.. rst:directive:: .. erl:function:: name(signature)

   Describes a module-level function. Usage of this directive is almost as same as Python's one.

   Erlang domain can accept functions whose names are same.
   To identify these, Erlang domain have arity information::

      .. erl:module:: lists

      .. erl:function:: append(List1, List2)

         This has ``lists:append/2`` for internal name.

      .. erl:function:: flatten(DeepList[, Tail]) -> List

         This has both ``lists:flatten/1`` and ``lists:flatten/2`` as
         internal name.

   .. seealso:: .. py:function:: name
   
.. rst:directive:: .. erl:macro:: name

   Describes macro which typically starts with capital character.

.. rst:directive:: .. erl:record:: name

   Describes a record.
   

Cross-referencing Erlang objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following roles refer to objects in modules and are possibly hyperlinked if
a matching identifier is found:

.. rst:role:: erl:mod

   Reference a module. 

.. rst:role:: erl:func

   Reference a Erlang function; a name with module may be used.

   It can handle **arity**. If you don't pass arity, erlang domain search
   the function whose arity is minimum.
   If you don't pass module name, it uses ``erlang`` module by default.
   The role text needs
   not include trailing parentheses to enhance readability; they will be added
   automatically by Sphinx if the :confval:`add_function_parentheses` config
   value is true (the default).
   
   If you want to refer module function, you should use following style::
   
      :erl:func:`modulename:func_name`

.. rst:role:: erl:macro

   Reference a macro whose name starts with capital charactor.

.. rst:role:: erl:record

   Reference a record. Typically, it starts with ``#``.

