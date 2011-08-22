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
   - ``bitbucket``: The issue tracker of https://bitbucket.org.  Has the same
     requirements as the ``github`` tracker.
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

   .. note::

      In case of BitBucket and GitHub, the project name must include the name
      of the user or organization, the project belongs to.  For instance, the
      project name of Sphinx_ itself is not just ``sphinx``, but
      ``birkenfeld/sphinx`` instead.

   .. versionchanged:: 0.8
      Project names must include the user name now.

For instance, with the following configuration issue references in the
documentation would refer to the `Sphinx issue tracker`_:

.. code-block:: python

   issuetracker = 'bitbucket'
   issuetracker_user = 'birkenfeld/sphinx'

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

If you use an issue tracker that is not supported by this extension, then set
:confval:`issuetracker` to ``None`` or leave it unset, and connect your own
callback to the event :event:`issuetracker-resolve-issue`:

.. event:: issuetracker-resolve-issue(app, project, issue_id)

   Emitted if a issue reference is to be resolved.

   ``app`` is the Sphinx application object.  ``project`` is the issuetracker
   project to query (see :confval:`issuetracker_project`).  ``issue_id`` is the
   issue id as string.

   A callback should return an :class:`Issue` object containing the resolved
   issue, or ``None`` if it could not resolve the issue.  In the latter case
   other resolvers connected to the event may be invoked by Sphinx.

.. class:: Issue

   A :func:`~collections.namedtuple` providing issue information.

   .. attribute:: id

      The issue id as string

      If you are writing your own custom callback for
      :event:`issuetracker-resolve-issue`, set this attribute to the
      ``issue_id`` that was given as argument.

   .. attribute:: uri

      An URI providing information about this issue.

      This URI is used as hyperlink target in the generated documentation.
      Thus it should point to a webpage or something similar that provides
      human-readable information about an issue.

   .. attribute:: closed

      ``True``, if the issue is closed, ``False`` otherwise.


Contribution
------------

Please contact the author or create an issue in the `issue tracker`_ of the
sphinx-contrib_ repository, if you have found any bugs or miss some
functionality (e.g. integration of some other issue tracker).  Patches are
welcome!


.. include:: ../CREDITS


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
.. _lxml: http://lxml.de
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _launchpadlib: http://pypi.python.org/pypi/launchpadlib/
.. _debianbts: https://github.com/venthur/python-debianbts
.. _suds: https://fedorahosted.org/suds/
.. _sphinx-contrib: https://bitbucket.org/birkenfeld/sphinx-contrib
.. _issue tracker: https://bitbucket.org/birkenfeld/sphinx-contrib/issues/
