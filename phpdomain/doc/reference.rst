Reference
#########

.. highlight:: rst

The PHP domain provides the following directives. 
Most directives are similar to Python's.

Directives
==========

Each directive populates the index, and or the namespace index.

.. rst:directive:: .. php:namespace:: name

   This directive declares a new PHP namespace.  It accepts nested
   namespaces by separating namespaces with ``\``.  It does not generate
   any content like :rst:dir:`php:class` does.  It will however, generate 
   an entry in the namespace/module index.
   
   It has ``synopsis`` and ``deprecated`` options, similar to :rst:dir:`py:module`
  
.. rst:directive:: .. php:global:: name

   This directive declares a new PHP global variable.

.. rst:directive:: .. php:function:: name(signature)

   Defines a new global/namespaced function outside of a class.  You can use 
   many of the same field lists as the python domain.  However, ``raises`` 
   is replaced with ``throws``

.. rst:directive:: .. php:const:: name

   This directive declares a new PHP constant, you can also used it nested 
   inside a class directive to create class constants.
   
.. rst:directive:: .. php:exception:: name

   This directive declares a new Exception in the current namespace. The 
   signature can include constructor arguments.

.. rst:directive:: .. php:class:: name

   Describes a class.  Methods, attributes, and constants belonging to the class
   should be inside this directive's body::

        .. php:class:: MyClass
        
            Class description
        
           .. php:method:: method($argument)
        
           Method description


   Attributes, methods and constants don't need to be nested.  They can also just 
   follow the class declaration::

        .. php:class:: MyClass
        
            Text about the class
        
        .. php:method:: methodName()
        
            Text about the method
        

   .. seealso:: .. php:method:: name
                .. php:attr:: name
                .. php:const:: name

.. rst:directive:: .. php:method:: name(signature)

   Describe a class method, its arguments, return value, and exceptions::
   
        .. php:method:: instanceMethod($one, $two)
        
            :param string $one: The first parameter.
            :param string $two: The second parameter.
            :returns: An array of stuff.
            :throws: InvalidArgumentException
        
           This is an instance method.

.. rst:directive:: .. php:staticmethod:: ClassName::methodName(signature)

    Describe a static method, its arguments, return value and exceptions,
    see :rst:dir:`php:method` for options.

.. rst:directive:: .. php:attr:: name

   Describe an property/attribute on a class.

Cross Referencing
=================

The following roles refer to php objects and are links are generated if a 
matching directive is found:

.. rst:role:: php:ns

   Reference a namespace. Nested namespaces need to be separated by two \\ due 
   to the syntax of ReST::
   
      .. php:ns:`LibraryName\\SubPackage` will work correctly.

.. rst:role:: php:func

   Reference a PHP function either in a namespace or out. If the function is in
   a namespace, be sure to include the namespace, unless you are currently 
   inside the same namespace.

.. rst:role:: php:global

   Reference a global variable whose name has ``$`` prefix.
   
.. rst:role:: php:const

   Reference either a global constant, or a class constant.  Class constants should
   be preceded by the owning class::
   
        DateTime has an :php:const:`DateTime::ATOM` constant.

.. rst:role:: php:class

   Reference a class; a name with namespace can be used. If you include a namespace,
   you should use following style::
   
     :php:class:`LibraryName\\ClassName`

.. rst:role:: php:meth

   Reference a method of a class. This role supports both kinds of methods::
   
     :php:meth:`DateTime::setDate`
     :php:meth:`Classname::staticMethod`

.. rst:role:: php:attr

   Reference a property on an object::
   
      :php:attr:`ClassName::$propertyName`

.. rst:role:: php:exc

   Reference an exception.  A namespaced name may be used.
