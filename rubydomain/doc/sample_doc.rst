###############
Sample Document
###############

.. default-domain:: rb

.. module:: BerryMQ

========
Ruby API
========

Ruby API is similar to Python API. I this section show samples in Ruby. 
If you need detail information see Python API reference.

.. index::
   single: decorator; Ruby

Decorators
==========

berryMQ provides module methods :meth:`Follower.following` and :meth:`Follower.auto_twitter`. They works like ``Class.public`` and ``Class.private`` and so on. It emurates decorator mechanism in Python.

Use this like following:

.. code-block:: ruby

   require 'berrymq'

   class Logger
     include BerryMQ::Follower

     following("*:log")
     def receive_log(message)
       ...
     end
   end

``Class.public`` keeps effect until other module method will be called, 
But this functions effect only the next method definition.


.. warning::

   Ruby implementation uses module including mechanism to class.
   So you can't set module function receiver like Python.


.. class:: Follower

   If you want to use the method as receiver, set this class as metaclass.
   
   This class provide special decorators. :func:`following` 
   and :func:`auto_twitter`. Use like this:

   .. code-block:: ruby

      # Ruby
      class Logger
        include BerryMQ::Follower
        
        following("*:log")
        def receive_log(message)
           ...
        end
      end

   .. classmethod:: following(identifier[, guard_condition])

      This is a decorator function. This decorator can use for only instanse methods of the classes which use :class:`Follower` metaclass.

      :param identifier: receive message filter identifier.
      :type  identifier: str
      :param guard_condition: if this guard function return False, message receive will be skipped
      :type  guard_condition: callable object with one paramater(message object)

   .. classmethod:: auto_twitter(identifier[, entry[, exit]])

      This is a decorator function. 
      The decorated function is called, automatically sends message.

      .. code-block:: python

         @auto_twitter("function")
         def sample_function():
             ... do something

      If this function is called, ``function:entry`` message will be sent before running function, and then ``function:exit`` message will be sent after running function.

      Use ``entry``, ``exit`` parameter for controlling message.

      ===== ===== ==================
      entry exit  action
      ===== ===== ==================
      False False send both.
      False True  exit message only
      True  False entry message only
      True  True  send both.
      ===== ===== ==================

      :param identifier: Send message :ref:``identifier``
      :type  identifier: str
      :param entry: Send message before calling function?(default: False)
      :type  entry: True or False
      :param exit: Send message after calling function?(default: False)
      :type  exit: True or False

.. index::
   single: function; Ruby

Functions
=========

You can use :func:`BerryMQ.twitter` function like this:

.. code-block:: ruby

   require 'berrymq'

   def on_button_pressed
      BerryMQ.twitter("on_button_pressed:log")
      .
      .
   end


.. function:: twitter(identifier[, ...])

   Send message. It is the most important function in berryMQ.
   This funciton can recieve any args and kwargs. These values are delivered
   via :class:`Message` object.


.. note::

   In future release, if last paramter is ``Hash``, it will pass as kwargs.

.. index::
   single: class; Ruby

Classes
=======

.. class:: Message

   This object is created in berryMQ automatically. User doesn't 
   create this object directly.

   All of following attributes are readonly(defined as property).

   .. attr_reader:: name

      This is a front part of Identifier.
      
   .. attr_reader:: action
   
      This is a back part of Identifier.
      
   .. attr_reader:: id
   
      This is a string form of Identifier
      
   .. attr_reader:: args
   
      If you pass any parameters at twitter(), this attribute stores them.

      .. code-block:: ruby

         .
         twitter("do_something:log", time.ctime())
         .

         class Logger
            following("*:log)
            def receive_log(message)
               puts message.args[0]  # print time.ctime() value
            end
         end

