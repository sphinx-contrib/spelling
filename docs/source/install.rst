.. .. spelling::

   wikis
   sphinxcontrib

==============
 Installation
==============

Installing sphinxcontrib.spelling
=================================

1. Follow the instructions on the PyEnchant_ site to install
   **enchant** and then **PyEnchant**.
2. Install the extension with pip: ``pip install sphinxcontrib-spelling``

.. _PyEnchant: http://packages.python.org/pyenchant/

Configuration
=============

1. Add ``'sphinxcontrib.spelling'`` to the ``extensions`` list in ``conf.py``.

  ::

    extensions = [ 'sphinxcontrib.spelling' ]

.. _install-options:
