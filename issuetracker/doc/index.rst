:mod:`sphinxcontrib.issuetracker` -- Reference issues in issue trackers
========================================================================

.. module:: sphinxcontrib.issuetracker
   :synopsis: Parse issue references and link to the corresponding issues

This extension for Sphinx_ 1.0 parses textual issue references like ``#10``,
looks up the issue in the configured issue tracker, and includes a link to
the issue.  References in inline literals and literal blocks (e.g. source code
examples) are ignored.

The extension is available under the terms of the BSD license, see
:doc:`license` for more information.


Installation
------------

This extension can be installed from the Python Package Index::

   pip install sphinx-contrib.issuetracker

Alternatively, you can clone the sphinx-contrib_ repository from BitBucket,
and install the extension directly from the repository::

   hg clone https://bitbucket.org/birkenfeld/sphinx-contrib
   cd sphinx-contrib/issuetracker
   python setup.py install


Configuration
-------------

Add ``sphinxcontrib.issuetracker`` to the configuration value
:confval:`extensions` to enable this extensions and configure the extension:

.. confval:: issuetracker

   The issuetracker to use.  As of now, the following trackers are
   supported:

   - ``github``: The issue tracker of https://github.com.  To use this issue
     tracker, either Python 2.6 or later must be used, or simplejson_ must be
     installed.
   - ``bitbucket``: The issue tracker of https://bitbucket.org.  To use this
     issue tracker, `lxml`_ 2.0 or newer must be installed.
   - ``launchpad``: The issue tracker of https://launchpad.net.  To use this
     issue tracker, launchpadlib_ must be installed.
   - ``google code``: The issue tracker of http://code.google.com.  To use
     this issue tracker, Python 2.5 or newer is required.
   - ``debian``: The Debian issue tracker at http://bugs.debian.org.  To use
     this issue tracker, you need the debianbts_ module from (available as
     ``python-debianbts`` in Debian package repositories).

     .. warning::

        The underlying ``debianbts`` module has serious quality issues
        [#debianbts-problems]_.  Use at own risk, the code of this issue
        tracker is unlikely to receive bug fixes and consequently might break
        any time.

.. confval:: issuetracker_project

   The project inside the issue tracker or the project, to which the issue
   tracker belongs.  Defaults to the value of :confval:`project`.

.. confval:: issuetracker_user

   The user account, to which the project belongs.  Required by the
   following issue trackers:

   - ``github``
   - ``bitbucket``

   Can be left empty, if another issue trackers is used.

For instance, with the following configuration issue references in the
documentation would refer to the `Sphinx issue tracker`_:

.. code-block:: python

   issuetracker = 'bitbucket'
   issuetracker_user = 'birkenfeld'
   issuetracker_project = 'sphinx'

Closed issues are detected and automatically struck through in HTML output.

By default the extension looks for issue references starting with a single
dash, like ``#10``.  You can however change the pattern, which is used to
find issue references:

.. confval:: issuetracker_issue_pattern

   A regular expression, which is used to find and parse issue references.
   Defaults to ``r'#(\d+)'``.  If changed to ``r'gh-(\d+)'`` for instance,
   this extension would not longer recognize references like ``#10``, but
   instead parse references like ``gh-10``.  The pattern must contain only a
   single group, which matches the issue id.


Customization
-------------

If you use an issue tracker, that is not supported by this extension, then set
:confval:`issuetracker` to ``None`` or leave it unset, and connect your own
callback to the :event:`issuetracker-resolve-issue`:

.. event:: issuetracker-resolve-issue(app, project, user, issue_id)

   Emitted if a issue reference is to be resolved.

   ``app`` is the Sphinx application object.  ``project`` and ``user`` are
   strings, describing the issuetracker project and username.  These are simply
   the values, the user entered for :confval:`issuetracker_project` and
   :confval:`issuetracker_user`.  ``issue_id`` is the issue id as string.

   Callbacks for this event must return a dictionary with issue information,
   having the following keys:

   - ``'uri'``: The URI to the issue web page
   - ``'closed'``: ``True``, if the issue is closed.  If ``False`` or if the
     key is missing, the issue is still open.

   If ``'uri'`` is missing, the issue reference is not turned into a real
   reference, but remains in plain text.

   A callback can return ``None`` instead to indicate, that it cannot resolve
   the issue.  Resolval is delegated to further callbacks, that might be
   connected to the event.


Contribution
------------

Please contact the author or create an issue in the `issue tracker`_ of the
sphinx-contrib_ repository, if you have found any bugs or miss some
functionality (e.g. integration of some other issue tracker).  Patches are
welcome!


.. rubric:: Footnotes

.. [#debianbts-problems] ``debianbts`` does not provide a standard
   distutils/setuptools installation script.  It is consequently not contained
   in the package index, and hard to install on anything else then Debian and
   Debian-based distributions.  And above all, it uses the outdated and
   unmaintained SOAPpy library internally.  Patches, which replace
   ``debianbts`` with some decent SOAP code (probably based on suds_) are
   welcome.  Patches, which replace SOAP completely with some decent RPC
   interface are even more welcome.


.. toctree::
   :maxdepth: 2
   :hidden:

   changes.rst
   license.rst


.. _Sphinx: http://sphinx.pocoo.org/
.. _Sphinx issue tracker: https://bitbucket.org/birkenfeld/sphinx/issues/
.. _lxml: http://codespeak.net/lxml
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _launchpadlib: http://pypi.python.org/pypi/launchpadlib/
.. _debianbts: https://github.com/venthur/python-debianbts
.. _suds: https://fedorahosted.org/suds/
.. _sphinx-contrib: https://bitbucket.org/birkenfeld/sphinx-contrib
.. _issue tracker: https://bitbucket.org/birkenfeld/sphinx-contrib/issues/
