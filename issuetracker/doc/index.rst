:mod:`sphinxcontrib.issuetracker` -- Reference issues in issue trackers
=======================================================================

.. module:: sphinxcontrib.issuetracker
   :synopsis: Parse issue references and link to the corresponding issues

A Sphinx_ extension to turn textual issue ids like ``#10`` into real references
to these issues in an issue tracker.

The extension is available under the terms of the BSD license, see
:doc:`license` for more information.


Installation
------------

This extension needs Sphinx 1.0 and Python 2.6 or newer.  Python 3 is not (yet)
supported.

Use ``pip`` to install this extension straight from the Python Package Index::

   pip install sphinx-contrib.issuetracker


Operation
---------

After configuring the :confval:`tracker <issuetracker>` and the
:confval:`project <issuetracker_project>`, this extension parses issue ids in
all documents and turns the issue id into a reference to the issue.  Issues are
searched in the configured tracker, issue ids which do not exist are ignored.
Issue ids in ``inline literals`` or literal blocks are also ignored to not
spoil code examples.

The extension queries the tracker for information about each issue.  This
information is used to mark closed issues.  Such issues are automatically
struck through in HTML output.


Configuration
-------------

Add ``sphinxcontrib.issuetracker`` to the configuration value
:confval:`extensions` to enable this extensions and configure the extension:

.. confval:: issuetracker

   The issuetracker to use.  As of now, the following trackers are
   supported:

   - ``github``: The issue tracker of https://github.com.
   - ``bitbucket``: The issue tracker of https://bitbucket.org.
   - ``launchpad``: The issue tracker of https://launchpad.net.  To use this
     issue tracker, launchpadlib_ must be installed.
   - ``google code``: The issue tracker of http://code.google.com.
   - ``debian``: The Debian issue tracker at http://bugs.debian.org.  To use
     this issue tracker, debianbts_ and SOAPpy_ must be installed.
   - ``jira``: A Jira_ instance.  Use :confval:`issuetracker_url` to configure
     the Jira instance to use.

     .. versionadded:: 0.8

.. confval:: issuetracker_project

   The project inside the issue tracker or the project, to which the issue
   tracker belongs.  Defaults to the value of :confval:`project`.

   .. note::

      In case of BitBucket and GitHub, the project name must include the name
      of the user or organization, the project belongs to.  For instance, the
      project name of Sphinx_ itself is not just ``sphinx``, but
      ``birkenfeld/sphinx`` instead.  If the user name is missing, a
      :exc:`~exceptions.ValueError` will be raised when an issue is to be
      resolved the first time.

   .. versionchanged:: 0.8
      Project names must include the user name now.

.. confval:: issuetracker_url

   The base url of the issue tracker.  Required by all issue trackers which do
   not only have a single instance, but many different instances on many
   different sites.  Currently this is only ``jira``::

      issuetracker = 'jira'
      issuetracker_url = 'https://studio.atlassian.com'

   .. versionadded:: 0.8

For instance, with the following configuration issue references in the
documentation would refer to the `Sphinx issue tracker`_::

   issuetracker = 'bitbucket'
   issuetracker_project = 'birkenfeld/sphinx'

By default the extension looks for issue references starting with a single
dash, like ``#10``.  You can however change the pattern, which is used to
find issue references:

.. confval:: issuetracker_issue_pattern

   A regular expression, which is used to find and parse issue references.
   Defaults to ``r'#(\d+)'``.  If changed to ``r'gh-(\d+)'`` for instance,
   this extension would not longer recognize references like ``#10``, but
   instead parse references like ``gh-10``.  The pattern must contain only a
   single group, which matches the issue id.

Normally the issue id as found in the text will be used as reference text.
However, you can also use the title of the issue as issue text:

.. confval:: issuetracker_expandtitle

   If ``True``, use the issue title instead of the issue id as reference text.
   If an issue has no title, the issue id is used instead, just like if this
   configuration key was ``False``.

   Defaults to ``False``.

   .. versionadded:: 0.8


Customization
-------------

If you use an issue tracker that is not supported by this extension, then set
:confval:`issuetracker` to ``None`` or leave it unset, and connect your own
callback to the event :event:`issuetracker-resolve-issue`:

.. event:: issuetracker-resolve-issue(app, tracker_config, issue_id)

   Emitted if a issue reference is to be resolved.

   ``app`` is the Sphinx application object.  ``tracker_config`` is the
   issuetracker configuration as :class:`TrackerConfig` object.  ``issue_id``
   is the issue id as string.

   A callback should return an :class:`Issue` object containing the resolved
   issue, or ``None`` if it could not resolve the issue.  In the latter case
   other resolvers connected to the event may be invoked by Sphinx.

   .. versionchanged:: 0.8
      Replaced ``project`` argument with ``tracker_config``

.. autoclass:: TrackerConfig

   .. attribute:: project

      The project name as string

   .. attribute:: url

      The url of the issue tracker as string *without* any trailing slash, or
      ``None``, if there is no url configured for this tracker.  See
      :confval:`issuetracker_url`.

   .. versionadded:: 0.8

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

   .. versionadded:: 0.8


Contribution and Development
----------------------------

Please report bugs and missing functionality (e.g. a tracker not being
supported) to the `issue tracker`_.

The source code of this extension is available in the sphinx-contrib_
repository.  Feel free to clone this repository and add your changes to this
extension.  Patches and pull requests are always welcome!


.. include:: ../CREDITS


.. toctree::
   :maxdepth: 2
   :hidden:

   changes.rst
   license.rst


.. _Sphinx: http://sphinx.pocoo.org/
.. _Sphinx issue tracker: https://bitbucket.org/birkenfeld/sphinx/issues/
.. _jira: http://www.atlassian.com/software/jira/
.. _launchpadlib: http://pypi.python.org/pypi/launchpadlib/
.. _debianbts: http://pypi.python.org/pypi/python-debianbts/
.. _SOAPpy: http://pypi.python.org/pypi/SOAPpy/
.. _sphinx-contrib: https://bitbucket.org/birkenfeld/sphinx-contrib
.. _issue tracker: https://bitbucket.org/birkenfeld/sphinx-contrib/issues/
