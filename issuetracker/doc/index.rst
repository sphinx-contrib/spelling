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
:confval:`project <issuetracker_project>` (and possibly the :confval:`tracker
url <issuetracker_url>`), you can reference issues in the issue tracker with
the :rst:role:`issue` role:

.. rst:role:: issue

   Create a reference to the given issue.  This role understands the standard
   :ref:`cross-referencing syntax <xref-syntax>` used by Sphinx.

   An explicit title given to this role is interpreted as `format string`_,
   which is formatted with the :class:`Issue` object representing the
   referenced issue available by the key ``issue``.  You may use any attribute
   of the :class:`Issue` object in your format string.  Use this feature to
   include information about the referenced issue in the reference title.  For
   instance, you might use ``:issue:`{issue.title} (#{issue.id}) <10>``` to use
   the title and the id of the issue ``10`` as reference title.

Information about the issue (like the title) is retrieved from the configured
issue tracker.  Aside of providing it for reference titles, the extension also
uses this information to mark closed issues in HTML output by striking the
reference text through.  For this purpose, a stylesheet is added to the
generated HTML.

You can provide your own styles for issue references by adding them to the
``.xref.issue`` and ``.xref.issue.closed`` selectors (the latter are closed
issues).  For instance, the following stylesheet uses red color for open, and
green color for closed issues::

   .xref.issue {
       color: green;
   }

   .xref.issue.closed {
       color: red;
   }


Issue ids in plain text
~~~~~~~~~~~~~~~~~~~~~~~

If :confval:`issuetracker_plaintext_issues` is ``True``, this extension also
searches for issue ids like ``#10`` in plain text and turns them into issue
references.  Issue ids in literal text (e.g. inline literals or code blocks)
are ignored.  The pattern used to extract issue ids from plain text can be
configured using :confval:`issuetracker_issue_pattern`.


Configuration
-------------

General configuration
~~~~~~~~~~~~~~~~~~~~~

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
   - ``jira``: A Jira_ instance.  With this issue tracker
     :confval:`issuetracker_url` must be set to the base url of the Jira
     instance to use.  Otherwise a :exc:`~exceptions.ValueError` is raised when
     resolving the first issue reference.

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

   The base url of the issue tracker::

      issuetracker = 'jira'
      issuetracker_url = 'https://studio.atlassian.com'

   Required by all issue trackers which do not only have a single instance, but
   many different instances on many different sites.

   .. versionadded:: 0.8

For instance, with the following configuration issue references in the
documentation would refer to the `Sphinx issue tracker`_::

   issuetracker = 'bitbucket'
   issuetracker_project = 'birkenfeld/sphinx'


Plaintext issues
~~~~~~~~~~~~~~~~

.. confval:: issuetracker_plaintext_issues

   If ``True`` (the default) issue references are extracted from plain text by
   turning issue ids like ``#10`` into references to the corresponding issue.
   Issue ids in any kind of literal text (e.g. ``inline literals`` or code
   blocks) are ignored.

By default the extension looks for issue references starting with a single
dash, like ``#10``.  You can however change the pattern, which is used to
find issue references:

.. confval:: issuetracker_issue_pattern

   A regular expression, which is used to find and parse issue references.
   Defaults to ``r'#(\d+)'``.  If changed to ``r'gh-(\d+)'`` for instance,
   this extension would not longer recognize references like ``#10``, but
   instead parse references like ``gh-10``.  The pattern must contain only a
   single group, which matches the issue id.

Normally the reference title will be the whole issue id.  However you can also
use a custom reference title:

.. confval:: issuetracker_title_template

   A `format string`_ template for the title of references created from
   plaintext issue ids.  The format string gets the :class:`Issue` object
   corresponding to the referenced issue in the ``issue`` key, you may use any
   attributes of this object in your format string.  You can for instance
   include the issue title and the issue id::

      issuetracker_title_template = '{issue.title} ({issue.id})'

   If unset, the whole text matched by :confval:`issuetracker_issue_pattern` is
   used as reference title.


Customization
-------------

If you use an issue tracker that is not supported by this extension, then set
:confval:`issuetracker` to ``None`` or leave it unset, and connect your own
callback to the event :event:`issuetracker-lookup-issue`:

.. event:: issuetracker-lookup-issue(app, tracker_config, issue_id)

   Emitted if the issue with the given ``issue_id`` should be looked up in the
   issue tracker.  Issue tracker configured is provided by ``tracker_config``.

   ``app`` is the Sphinx application object.  ``tracker_config`` is the
   issuetracker configuration as :class:`TrackerConfig` object.  ``issue_id``
   is the issue id as string.

   A callback should return an :class:`Issue` object containing the looked up
   issue, or ``None`` if it could not find the issue.  In the latter case other
   callbacks connected to this event are be invoked by Sphinx.

   .. versionchanged:: 0.8
      Replaced ``project`` argument with ``tracker_config``, changed return
      value from dictionary to :class:`Issue`

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
      :event:`issuetracker-lookup-issue`, set this attribute to the
      ``issue_id`` that was given as argument.

   .. attribute:: url

      An URL providing information about this issue.

      This URL is used as hyperlink target in the generated documentation.
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
.. _format string: http://docs.python.org/library/string.html#format-string-syntax
