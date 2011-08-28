.. _devel:

===========
Development
===========
This section contains information for further development of the module.

.. index:: Building

Building
========
Python-based scription solution `Paver`_
scripting tool solution is used to build and distribute the software. Since the package already
contains the dependencies to Paver, the basic building can be done as follows

  .. code-block:: bash

     python setup.py bdist_egg sdist_src

However, installation of the paver is strongly suggested. After installation,
the documentation, building and packaging can be all in once:

  .. code-block:: bash

     paver package

To build just the documentation, run::

  paver doc


.. index:: Testing

.. _testing:

Testing
=======
The unit testing in Rusty is implemented by eating the own dog food: the latest
version of extensions are always used to generate content the documentation. In
addition to user documentation, there exists a separate test documentation that
tries the different variations of the module usage.

To run the tests (to generate the test documentation), run shell command:

  .. code-block:: bash

     python setup.py test

     OR

     paver test


Licensing
=========
The software is licensed with liberal MIT license, making it suitable for both
commercial and open source usage:

    .. include:: ../LICENSE

.. include:: global.rst
