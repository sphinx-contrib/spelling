0.9 (in development)
====================

- Fixed TypeError caused by ``launchpad`` issue tracker
- Fixed issue title in ``launchpad`` issue tracker


0.8 (2011 Aug, 24)
==================

Incompatible changes
--------------------

- Require Python 2.6 or newer now
- Removed ``issuetracker_user`` configuration value, GitHub and BitBucket
  projects must include the username now
- Custom resolvers must return :class:`~sphinxcontrib.issuetracker.Issue`
  objects instead of dictionaries now
- Signature of :event:`issuetracker-resolve-issue` changed

Other changes
-------------

* General:

  - Builtin ``debian`` tracker is fully supported now

* New features:

  - Added Jira_ support
  - Added :confval:`issuetracker_url`
  - Added :confval:`issuetracker_expandtitle`

* Bugs fixes and improvements:

  - Use BitBucket API instead of scraping the BitBucket website
  - Cache failed issue lookups, too

.. _jira: http://www.atlassian.com/software/jira/


0.7.2 (Mar 10, 2011)
====================

- #13: Fixed source distribution to include tests again
- Fixed extraction of issue state for open issues from bitbucket
- Ignore references in inline literals and literal blocks


0.7.1 (Jan 19, 2011)
====================

- Fixed #8: Copy the stylesheet after build again to avoid exceptions on
  non-existing build directories


0.7 (Jan 08, 2011)
==================

- Issue information is now cached
- Custom issue trackers must now connect to the ``issuetracker-resolve-issue``
  event, the builtin ``missing-reference`` event is no longer used.


0.6 (Jan 04, 2011)
==================

- Added support for the debian bugtracker (thanks to Fladischer Michael)
- Fixed NameError in launchpad issue tracker
- Bitbucket also uses HTTPS urls now


0.5.4 (Nov 15, 2010)
====================

- Github uses HTTPS urls now


0.5.3 (Nov 14, 2010)
====================

- Added license text to source tarball


0.5.2 (Sep 17, 2010)
====================

- Issue reference resolvers get the application object now as fourth
  argument.  The environment is availabe in the ``.env`` attribute of this
  object.
- #4: Fixed the URL of Google Code issues (thanks to Denis Bilenko)
- Fixed detection of closed issues in Google Code (thanks to Denis Bilenko)
- Improved error message, if ``issuetracker_issue_pattern`` has too many
  groups (thanks to Denis Bilenko)
- Added warnings for unexpected HTTP status codes in BitBucket and Google
  Code issue trackers


0.5.1 (Jul 25, 2010)
====================

- Fixed client string for launchpad access


0.5 (Jul 21, 2010)
==================

- Closed issues are automatically struck trough in HTML output
- Require Sphinx 1.0 now
- Fixed #2:  Installation on windows


0.4 (May 21, 2010)
==================

- Misc spelling fixes


0.3 (May 02, 2010)
==================

- Added support for Google Code
- Added support for Launchpad
- Issue tracker callbacks get the build environment now


0.2 (Apr 13, 2010)
==================

- Use ``missing-reference`` event instead of custom event


0.1 (Apr 10, 2010)
==================

- Initial release

