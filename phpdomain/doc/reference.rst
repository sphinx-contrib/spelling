Reference
#########

.. highlight:: rst

The PHP domain provides the following directives. 
Most directives are similar to Python's.

.. rst:directive:: .. php:namespace:: name

   This directive declares a new PHP namespace.  It accepts nested
   namespaces by separating namespaces with ``\``.  It does not generate
   any content like :rst:dir:`php:class` does.  It will however, generate 
   an entry in the namespace/module index.
   
   It has ``synopsis`` and ``deprecated`` options, similar to :rst:dir:`py:module`
  
.. rst:directive:: .. php:global:: name

   This directive declares a new PHP global variable.

.. rst:directive:: .. php:const:: name

   This directive declares a new PHP constant, you can also used it nested inside
   a class directive to create class constants.
   
.. rst:directive:: .. php:exception:: name

   This directive declares a new Exception in the current namespace. The signature
   can include constructor arguments.

.. rst:directive:: .. php:class:: name

   Describes a class.  Methods, attributes, and constants belonging to the class
   should be inside this directive's body.
