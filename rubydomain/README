===========
Ruby Domain
===========

:author: SHIBUKAWA Yoshiki <yoshiki at shibu.jp>

About
=====

This is the Ruby domain for Sphinx 1.0.
Sphinx 1.0 will deliver new feature -- Domain.
It will enable other language support except Python and C language.

This extension provides directives and roles to write Ruby documents.

Ruby Domain supports following objects:

* Global Variable
* Constant
* Module

  * Function
  * Method(for Mix-In)

* Class

  * Method
  * Class Method
  * Attribute

.. note::

   This domain expresses methods and attribute names like this::

      Module#method_name
      Class#method_name
      Class#attribute_name

   And other items(module function and class method) are expressed like this::

      Module.function_name
      Class.class_method_name

   Take care separator charactors!

URLs
====

:PyPI: http://pypi.python.org/pypi/sphinxcontrib-rubydomain
:Detail Document: http://packages.python.org/sphinxcontrib-rubydomain

Quick Sample
============

.. note::
   These contents is copied from http://ruby-doc.org/stdlib/libdoc/drb/rdoc/classes/DRb/DRbObject.html

This is source::

  .. rb:module:: DRb

  .. rb:class:: DRbObject

     Object wrapping a reference to a remote drb object.

     Method calls on this object are relayed to the remote object that this object is a stub for.

     .. rb:classmethod:: new(obj[, uri=nil])

        Create a new remote object stub.

        obj is the (local) object we want to create a stub for. Normally this is nil. 
        uri is the URI of the remote object that this will be a stub for.

     .. rb:classmethod:: new_with_uri(uri)

        Create a new DRbObject from a URI alone.

     .. rb:method:: method_missing(msg_id, *a, &b)

        Routes method calls to the referenced object.

Result:

-----------------

.. rb:module:: DRb

.. rb:class:: DRbObject

    Object wrapping a reference to a remote drb object.

    Method calls on this object are relayed to the remote object that this object is a stub for.

    .. rb:classmethod:: new(obj[, uri=nil])

       Create a new remote object stub.

       obj is the (local) object we want to create a stub for. Normally this is nil. 
       uri is the URI of the remote object that this will be a stub for.

    .. rb:classmethod:: new_with_uri(uri)

       Create a new DRbObject from a URI alone.

    .. rb:method:: method_missing(msg_id, *a, &b)

       Routes method calls to the referenced object.

------------------

From other place, you can create cross reference like that::

   If you want to connect other node, use :rb:meth:`DRb::DRbObject.new_with_uri` and get front object.

Result:

-----------

If you want to connect other node, use :rb:meth:`DRb::DRbObject.new_with_uri` and get front object.

-----------

Install
=======

.. code-block::

   easy_install -U sphinxcontrib-rubydomain

