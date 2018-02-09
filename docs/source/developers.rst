.. .. spelling::

..    sphinxcontrib
..    reStructuredText

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
-------------
To run the tests, you need ``tox`` installed. Then just run ``make test``.

Building Documentation
======================

The documentation for sphinxcontrib.spelling is written in
reStructuredText and converted to HTML using Sphinx. The build itself
is driven by make.  You will need the following packages in order to
build the docs:

- Sphinx
- docutils
- sphinxcontrib.spelling

Once all of the tools are installed into a virtualenv using
pip, run ``make html`` to generate the HTML version of the
documentation.
