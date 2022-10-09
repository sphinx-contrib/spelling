=================
 Release History
=================

.. spelling:word-list::

   Homebrew
   libenchant
   macOS
   unmaintained

7.6.1
=====

Bug Fixes
---------

- `#188 <https://github.com/sphinx-contrib/spelling/issues/188>`__
  Fix `:spelling:word:` directives from being printed verbatim in
  output files.

7.6.0
=====

Features
--------

- Convert to use Sphinx domains. Add ``spelling:word-list``
  directive. Have ``spelling`` directive report that it is deprecated.
- Add ``spelling:word`` role for marking inline text as spelled
  correctly.

7.5.1
=====

Bug Fixes
---------

- `#180 <https://github.com/sphinx-contrib/spelling/issues/180>`__
  Suppress `SystemExit` errors in `ImportableModuleFilter` caused by
  importing modules that run code on import and exit when that code
  sees an error. Bug report and reproducer provided by Trevor Gross.

7.5.0
=====

Features
--------

- `#151 <https://github.com/sphinx-contrib/spelling/issues/151>`__
  Added configuration option to limit the number of suggestions
  output. See :doc:`/customize` for more details. Idea contributed by
  Trevor Gross.
- `#169 <https://github.com/sphinx-contrib/spelling/issues/169>`__
  Adds the ability to pass in multiple wordlists via the sphinx
  command line as ``-D spelling_word_list_filename=file1,file2``.

Bug Fixes
---------

- `#36 <https://github.com/sphinx-contrib/spelling/issues/36>`__
  Include captions of figures in the set of nodes for which the text
  is checked.

7.4.1
=====

- `#160 <https://github.com/sphinx-contrib/spelling/issues/160>`__
  Fixed issue with the builder crashing when reporting a misspelled word
  in a python docstring.

7.4.0
=====

- Fix a problem that occurred when the extra word list is empty and an
  IndexError is thrown. Prevent the error by checking the contents of
  the file before using the list.
- `#153 <https://github.com/sphinx-contrib/spelling/issues/153>`__
  Ensure the correct relative filename is reported as the location of
  a misspelled word when the word is in an included file. Log the
  location ourselves instead of letting the logging system compute it
  for consistency until `the fix
  <https://github.com/sphinx-doc/sphinx/pull/10460>`__ is merged into
  Sphinx.
- Change default env list for local tox runs to only include the
  current python version, as defined by the installation of tox.
- Tell tox to pass `PYENCHANT_LIBRARY_PATH` through to commands. On
  macOS it can be a little tricky to set up libenchant if your default
  python does not match the one used by Homebrew for the
  library. Setting the variable to point to the library fixes that,
  but we don't want to set it in this file for everyone so use
  `passenv` to tell tox to pass the setting through when running the
  commands for each env.
- `#159 <https://github.com/sphinx-contrib/spelling/issues/159>`__
  Report using the line number of the misspelled word instead of using
  the first line of the node, in both the log and `.spelling` output
  file.

7.3.3
=====

Bug Fixes
---------

- `#149 <https://github.com/sphinx-contrib/spelling/pull/149>`__ Fixes
  to support testing when building RPMs. Switch to PEP 420 native
  namespace and skip contributors test when not in a git repo.
- `#150 <https://github.com/sphinx-contrib/spelling/pull/150>`__ Minor
  code cleanup primarily around string interpolation.

7.3.2
=====

Bug Fixes
---------

- `#143 <https://github.com/sphinx-contrib/spelling/pull/143>`__ Treat
  ``__main__`` as a special module name that cannot be imported. If
  the test suite is invoked by running ``python -m pytest`` instead of
  ``pytest`` then there will be no ``__main__`` and find_spec() will
  fail, so this change makes the tests work in both modes.
- `#144 <https://github.com/sphinx-contrib/spelling/pull/144>`__ Fix
  python filename handling in ``ImportableModuleFilter``.  If the word
  looks like a python module filename, strip the extension to avoid
  the side-effect of actually importing the module. This prevents, for
  example, ``'setup.py'`` triggering an import of the ``setup`` module
  during a doc build, which makes it look like Sphinx is complaining
  about a commandline argument.

7.3.1
=====

Bug Fixes
---------

- `#137 <https://github.com/sphinx-contrib/spelling/pull/137>`__
  replace the use of deprecated ``imp`` in ``ImportableModuleFilter``
  with ``importlib``

7.3.0
=====

New Features
------------

- `#131 <https://github.com/sphinx-contrib/spelling/pull/131>`__
  included a documentation update to fix a broken link.

- `#130 <https://github.com/sphinx-contrib/spelling/pull/130>`__ tested support
  for Python 3.10, and added the trove classifier.

- `#129 <https://github.com/sphinx-contrib/spelling/pull/129>`__ improved the
  speed of the ``ImportableModuleFilter``.

- `#128 <https://github.com/sphinx-contrib/spelling/pull/128>`__ fixed
  some issues with the packaging configuration.

7.2.0
=====

New Features
------------

- `#123 <https://github.com/sphinx-contrib/spelling/pull/123>`__ adds
  the ``spelling_verbose`` configuration option for controlling
  whether misspelled words are printed to the console as well as the
  output log files. See :ref:`output-options` for details.

7.1.0
=====

New Features
------------

- `#116 <https://github.com/sphinx-contrib/spelling/pull/116>`__ adds
  a config option `spelling_warning` that makes individual messages
  about misspellings warnings. The same change also updates the
  formatting of the message to make it easier for IDEs to parse,
  allowing the editor to navigate to the location of the misspelled
  word. See :ref:`output-options` for details.  Contributed by Robert
  Cohn.

7.0.1
=====

Bug Fixes
---------

- `#105 <https://github.com/sphinx-contrib/spelling/pull/105>`__
  reverts a change that switched from `imp` to `importlib`. Using
  `importlib.find_spec()`
  is not safe at runtime as it can import modules which will cause
  side effects within environments.

7.0.0
=====

This major release drops support for Python 3.5. This version is not
maintained anymore.

Bug Fixes
---------

- Fixes an issue with ellipsis incorrectly being interpreted as
  relative imports and triggering a `ValueError` in the
  `ImportableModuleFilter`. See `#96
  <https://github.com/sphinx-contrib/spelling/issues/96>`__ for
  details.

6.0.0
=====

With this release, sphinxcontrib-spelling moves from beta to
stable. It also updates the use of Python 3, including packaging
metadata, code style, and test configuration.

New Features
------------

- Add packaging metadata declaring the project stable.
- Add packaging metadata declaring support for Python 3 only.
- Add packaging metadata indicating that this is a sphinx extension.

Bug Fixes
---------

- Replace use of deprecated `imp` module with `importlib`.
- Update use of `pyenchant.get_tokenizer()` to pass filters argument
  as a keyword and avoid a runtime warning message.
- Remove unused test dependency on `fixtures`.
- Use `pyupgrade` to modernize the source code.

5.4.0
=====

New Features
------------

- Added a new filter
  (``sphinxcontrib.spelling.filters.ContributorFilter``) that treats
  contributor names extracted from the git history as spelled
  correctly, making it easier to refer to the names in
  acknowledgments . Includes a new configuration option,
  ``spelling_ignore_contributor_names`` to enable it.

5.3.0
=====

New Features
------------

- Add a configuration option ``spelling_exclude_patterns`` to manage
  skipping spell checking for some input files. The option uses a
  list of glob-style patterns that are matched against the source
  file names relative to the source directory. See :doc:`/customize`
  for more details. Contributed by sdelliot.

5.2.2
=====

Bug Fixes
---------

- Updated to only create ``.spelling`` output files for inputs that
  generate spelling warnings. Fixes #63.

5.2.0
=====

New Features
------------

- The builder is now registered using an entry point, so that if the
  ``spelling`` directive is not used in a project
  ``sphinxcontrib.spelling`` does not need to be included explicitly
  in the ``extensions`` list in ``conf.py`` in order to use it with
  the project on the command line.

- PyEnchant is an optional dependency. If it is not installed, the
  spell checker will not work, but the extension can still be
  initialized. This allows projects that use spell checking to
  publish their documentation to ``readthedocs.org``, where it is
  not possible to install PyEnchant.

- Restore support for parallel builds. Words that do not appear in
  any configured dictionary are written to a file named based on the
  input file, with the ``.rst`` extension replaced with
  ``.spelling``.

5.1.2
=====

- Mark as unsafe for parallel builds (contributed by Jared Dillard)
- Add -W arg to sphinx-build in docs so warnings cause error
  (contributed by Elsa Gonsiorowski, PhD)

5.1.0
=====

- Add an option to show the line containing a misspelling for context
  (contributed by Huon Wilson)

5.0.0
=====

- Drop Python 2.7 support. (contributed by Johannes Raggam)
- `allow customizing with classes using import strings
  <https://github.com/sphinx-contrib/spelling/pull/40>`__
- pyenchant is now maintained (contributed by Adam Johnson

4.3.0
=====

- Logging: use warning() instead of its deprecated alias (contributed
  by Sergey Kolosov)
- Support additional contractions (contributed by David Baumgold)
- require Sphinx >= 2.0.0
- declare support for Python 3.6

4.2.1
=====

- fix remaining logging issue (contributed by Timotheus Kampik)
- Remove usage of deprecated logging API (contributed by Tim Graham)

4.2.0
=====

- Fix a bug with empty word lists (contributed by FabioRosado)
- Update dependency management to use setuptools extras
- Document how to create multiple wordfiles (contributed by
  FabioRosado)
- Note that PyEnchant is unmaintained and fix links (contributed by
  Marti Raudsepp)
- Don’t use mutable default argument (contributed by Daniele Tricoli)

4.1.0
=====

- Make it possible to provide several wordlists (contributed by Tobias
  Olausson)
- Update developer documentation (contributed by Tobias Olausson)
- Update home page link (contributed by Devin Sevilla)

4.0.1
=====

- use the right method to emit warnings
- disable smart quotes so that we can recognize
  contractions/possessives correctly (contributed by Alex Gaynor)

4.0.0
=====

- Don’t fail by default (contributed by Stephen Finucane)
- Mark the extension as safe for parallel reading (contributed by Alex
  Gaynor)
- be more verbose about configuration options
- switch to testrepository for running tests
- update Python 3.3 to 3.5

2.3.0
=====

- make it possible to specify tokenizer #7 (contributed by Timotheus
  Kampik)

2.2.0
=====

- Use ``https`` with ``pypi.python.org`` package name checker
  (contributed by John-Scott Atlakson)
- Removed unnecessary shebang lines from non-script files (contributed
  by Avram Lubkin)
- Re-enable the PyEnchant dependency (contributed by Julian Berman)

2.1.2
=====

- Fixed issue with six under Python 3.4

2.1.1
=====

- Use ``str.isupper()`` instead of ad-hoc method
- fix syntax for tags directive
- Removed no more used CHANGES file

2.1
===

- Fix unicode error in ``PythonBuiltinsFilter``.
- Make error output useful in emacs compiler mode
- Only show the words being added to a local dictionary if debugging
  is enabled.


2.0
===

- Add Python 3.3 support.
- Add PyPy support.
- Use pbr for packaging.
- Update tox config to work with forked version of PyEnchant until
  changes are accepted upstream.

1.4
===

  - Fixed detection of builtins under PyPy, contributed by Hong Minhee
    (https://bitbucket.org/dahlia).

1.3
===

  - Handle text nodes without parents. (#19)
  - Include the input document name in the console output.
  - Use the Sphinx wrapper for registering a directive.

1.2
===

  - Add the document name to the messages showing the contents of a
    local dictionary created by the ``spelling`` directive.
  - Add title nodes to the list of node types checked for
    spelling. Resolves issue #17.
  - Add test/test_wordlist.txt to the manifest so it is included in
    the source distribution and the tests will pass. Resolves issue
    #17.
  - Documentation patch from Hank Gay.

1.1.1
=====

  - Fix initialization so the per-document filters work even if no
    ``spelling`` directive is used.

1.1
===

  - Add an option treat the names of packages on PyPI as spelled
    properly.
  - Add an option to treat CamelCase names as spelled properly.
  - Add an option to treat acronyms as spelled properly.
  - Add an option to treat Python built-ins as spelled properly.
  - Add an option to treat names that can be found as modules as
    spelled properly.
  - Add an option to let the user provide a list of other filter
    classes for the tokenizer.
  - Add ``spelling`` directive for passing local configuration
    settings to the spelling checker. This version allows setting a
    list of words known to be spelled correctly.

1.0
===

  - Re-implement using just a Builder, without a separate visitor
    class.
  - Show the file and line number of any words not appearing in the
    dictionary, instead of the section title.
  - Log the file, line, and unknown words as the documents are
    processed.

0.2
===

  - Warn but otherwise ignore unknown node types.

0.1
===

  - First public release.
