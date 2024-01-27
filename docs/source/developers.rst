.. spelling:word-list::

   sphinxcontrib
   reStructuredText

============
 Developers
============

If you would like to contribute to sphinxcontrib.spelling directly,
these instructions should help you get started.  Patches, bug reports,
and feature requests are all welcome through the `GitHub site
<https://github.com/sphinx-contrib/spelling>`__.
Contributions in the form of patches or pull requests are easier to
integrate and will receive priority attention.

Running tests
=============

To run the tests, you need ``tox`` installed, then just run
``tox``. This should run the unit tests, the source code linter, and
try to build the current documentation.

Enchant C Library
-----------------

You also need the C library from Enchant installed. On macOS, use
`brew` to install the `enchant` package, then set
`PYENCHANT_LIBRARY_PATH` to point to the `dylib` file included in the
output of `brew list enchant`.

.. code-block:: console

   $ brew list enchant | grep dylib
   /opt/homebrew/Cellar/enchant/2.6.4/lib/libenchant-2.dylib
   /opt/homebrew/Cellar/enchant/2.6.4/lib/libenchant-2.2.dylib

   $ export PYENCHANT_LIBRARY_PATH=/opt/homebrew/Cellar/enchant/2.6.4/lib/libenchant-2.2.dylib

Coding style
============

Python imports are formatted and sorted using `isort
<https://pycqa.github.io/isort/>`__. To format all files, run:

.. code-block:: console

   $ tox -e style

Building Documentation
======================

The documentation for sphinxcontrib.spelling is written in
reStructuredText and converted to HTML using Sphinx. The build is
driven by ``tox``. To build only the documentation, run ``tox -e
docs``.

Contributing
============

Please submit changes as pull requests using the `GitHub repository
<https://github.com/sphinx-contrib/spelling>`__.

In the pull request description, link to any issues closed by the
changes using ``Fixes #NUM``, replacing ``NUM`` with the issue number.

Release Notes
=============

Please add a release note for each pull request to ``docs/history.rst``.
