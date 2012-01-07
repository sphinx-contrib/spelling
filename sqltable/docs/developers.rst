============
 Developers
============

If you would like to contribute to sphinxcontrib.sqltable directly,
these instructions should help you get started.  Patches, bug reports,
and feature requests are all welcome through the `BitBucket site
<https://bitbucket.org/birkenfeld/sphinx-contrib/>`__.
Contributions in the form of patches or pull requests are easier to
integrate and will receive priority attention.

Building Documentation
======================

The documentation for sphinxcontrib.sqltable is written in
reStructuredText and converted to HTML using Sphinx. The build itself
is driven by make.  You will need the following packages in order to
build the docs:

- Sphinx
- docutils
- sphinxcontrib.sqltable

Once all of the tools are installed into a virtualenv using
pip, run ``make html`` to generate the HTML version of the
documentation.
