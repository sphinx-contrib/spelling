Reference
=========

.. highlight:: rst

The Ruby domain (name **rb**) provides the following directives for module
declarations. Almost all directives are similar to Python's.

.. rst:directive:: .. rb:module:: name

   This directive marks the beginning of the description of a module.
   This directive can accept nested modules(separated by ``::``).
   It does not create content (like e.g. :rst:dir:`rb:class` does).

   This directive will also cause an entry in the global module index.

   It has ``platform`` option, ``synopsis`` option and ``deprecated`` option as same as
   :rst:dir:`py:module`.


.. rst:directive:: .. rb:currentmodule:: name

   .. seealso:: :rst:dir:`py:currentmodule`

The following directives are provided for any where you want:

.. rst:directive:: .. rb:global:: name

   Describes global variable which starts with ``$``.

.. rst:directive:: .. rb:exception:: name

   Describes an exception class.  The signature can, but need not include
   parentheses with constructor arguments.

The following directives are provided for global and module level contents:

.. rst:directive:: .. rb:function:: name(signature)

   Describes a module-level function. Usage of this directive is almost as same as Python's one.
   
   .. note::
   
      Ruby has both module function and module method. Module function is 
      standard function like C, Python and so on. Module methods are enbaled
      when their module is included(Mix-in). This domain express module function as 
      ``ModuleName.func_name``, and module method as ``ModuleName#func_name``. Take care!
   
   .. seealso:: .. rb:function:: name

.. rst:directive:: .. rb:const:: name

   Describes constant which starts with capital character.

The following directive is provided for module and class contents:

.. rst:directive:: .. rb:method:: name(signature)

   Describes a module method and instance method. 
   Usage of this directive is almost as same as Python's one.
   
   .. seealso:: .. py:method:: name
                .. rb:function:: name

The following directive is provided for module contents:

.. rst:directive:: .. rb:class:: name

   Describes a class.
   
   Methods and attributes belonging to the class should be placed in this
   directive's body.  If they are placed outside, the supplied name should
   contain the class name so that cross-references still work.  Example::

      .. rb:class:: Foo
         .. rb:method:: quux()

      -- or --

      .. rb:class:: Bar

      .. rb:method:: Bar#quux()

   The first way is the preferred one.

The following directives are provided for class contents:

.. rst:directive:: .. rb:attr_reader:: name

.. rst:directive:: .. rb:attr_writer:: name

.. rst:directive:: .. rb:attr_accessor:: name

   Describes an object data attribute.  The description should include
   information about the type of the data to be expected.

.. rst:directive:: .. rb:classmethod:: name(signature)

   Like :rst:dir:`rb:method`, but indicates that the method is a class method.

   .. note::
   
      This domain expresses class method as 
      ``ModuleName.func_name``, and instance method 
      as ``ModuleName#func_name``. Take care!


Info field lists
~~~~~~~~~~~~~~~~

Ruby domain has field lists as same as Python domain except ``key``, ``keyword``.

Cross-referencing Ruby objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following roles refer to objects in modules and are possibly hyperlinked if
a matching identifier is found:

.. rst:role:: rb:mod

   Reference a module; a nested module name may be used(separated by ``::``).  

.. rst:role:: rb:func

   Reference a Ruby function; a name with module may be used.
   The role text needs
   not include trailing parentheses to enhance readability; they will be added
   automatically by Sphinx if the :confval:`add_function_parentheses` config
   value is true (the default).
   
   If you want to refer module function, you should use following style::
   
      :rb:func:`ParentModule::ModuleName.func_name`

.. rst:role:: rb:global

   Reference a global variable whose name has ``$`` prefix.
   
.. rst:role:: rb:const

   Reference a constant whose name starts with capital charactor.

.. rst:role:: rb:class

   Reference a class; a name with module may be used. In that case,
   you should use following style::
   
     :rb:class:`ModuleName::ClassName`

.. rst:role:: rb:meth

   Reference a method of an object and module. 
   The role text can include the type name and
   the method name; if it occurs within the description of a type, 
   the type name can be omitted. 

   This role supports any kind of methods::
   
     :rb:meth:`Module#method`
     :rb:meth:`Class#instance_method`
     :rb:meth:`Class.class_method`

.. rst:role:: rb:attr

   Reference a data attribute of an object.

.. rst:role:: rb:exc

   Reference an exception.  A dotted name may be used.

