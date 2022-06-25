=======================
 Configuration Options
=======================

These options can be set in ``conf.py`` along with the other Sphinx
configuration settings.

Input Options
=============

``spelling_lang='en_US'``

  String specifying the language, as understood by PyEnchant and
  enchant.  Defaults to ``en_US`` for US English.

``tokenizer_lang='en_US'``

    String specifying the tokenizer language as understood by PyEnchant
    and enchant. Defaults to ``en_US`` for US English.

``spelling_word_list_filename='spelling_wordlist.txt'``

  String specifying a file containing a list of words known to be
  spelled correctly but that do not appear in the language dictionary
  selected by ``spelling_lang``.  The file should contain one word per
  line. Refer to the `PyEnchant tutorial`_ for details.

  To add multiple files use a list, or a comma separated string. This
  is useful when calling sphinx with ``-D
  spelling_word_list_filename=...`` which will not accept a list and
  will only accept a string parameter.

``spelling_word_list_filename=['spelling_wordlist.txt','another_list.txt']``

  Same as above, but with several files of correctly spelled words.

``spelling_word_list_filename='spelling_wordlist.txt,another_list.txt'``

  Same as above, but with several files of correctly spelled words, and
  passing the setting as a single string. 

``spelling_exclude_patterns=['ignored_*']``

  A list of glob-style patterns that should be ignored when checking spelling.
  They are matched against the source file names relative to the source
  directory, using slashes as directory separators on all platforms. See Sphinx's
  `exclude_patterns`_ option for more details on glob-style patterns.

.. _PyEnchant tutorial: https://github.com/rfk/pyenchant/blob/master/website/content/tutorial.rst
.. _exclude_patterns : https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-exclude_patterns

.. _output-options:

Output Options
==============

``spelling_show_suggestions=False``

  Boolean controlling whether suggestions for misspelled words are
  printed.  Defaults to ``False``.

``spelling_suggestion_limit=0``

  Integer number of suggestions to emit when
  ``spelling_show_suggestions`` is ``True``. Defaults to ``0``,
  meaning no limit. Any positive value truncates the suggestion limit.

``spelling_show_whole_line=True``

  Boolean controlling whether the contents of the line containing each
  misspelled word is printed, for more context about the location of each
  word.  Defaults to True.

``spelling_warning=False``

  Boolean controlling whether a misspelling is emitted as a sphinx
  warning or as an info message. Defaults to False.

``spelling_verbose=True``

  Choose whether or not the misspelled words should be displayed in
  the terminal. Defaults to True.

Word Filters
============

Enable or disable the built-in filters to control which words are
returned by the tokenizer to be checked.

``spelling_ignore_pypi_package_names=False``

  Boolean controlling whether words that look like package names from
  PyPI are treated as spelled properly. When ``True``, the current
  list of package names is downloaded at the start of the build and
  used to extend the list of known words in the dictionary. Defaults
  to ``False``.

``spelling_ignore_wiki_words=True``

  Boolean controlling whether words that follow the CamelCase
  conventions used for page names in :spelling:word:`wikis` should be treated as
  spelled properly. Defaults to ``True``.

``spelling_ignore_acronyms=True``

  Boolean controlling treatment of words that appear in all capital
  letters, or all capital letters followed by a lower case ``s``. When
  ``True``, acronyms are assumed to be spelled properly. Defaults to
  ``True``.

``spelling_ignore_python_builtins=True``

  Boolean controlling whether names built in to Python should be
  treated as spelled properly. Defaults to ``True``.

``spelling_ignore_importable_modules=True``

  Boolean controlling whether words that are names of modules found on
  ``sys.path`` are treated as spelled properly. Defaults to ``True``.

``spelling_ignore_contributor_names=True``

  Boolean controlling whether contributor names taken from the git
  history for the repository are considered as spelled correctly.

``spelling_filters=[]``

  List of importable filter classes to be added to the tokenizer that
  produces words to be checked. For example,
  ``["enchant.tokenize.MentionFilter"]``.  The classes should be
  derived from ``enchant.tokenize.Filter``. Refer to the `PyEnchant
  tutorial`_ for examples.

Private Dictionaries
====================

There are three ways to provide a list of known good words. The
``spelling_word_list_filename`` option (described above) specifies the
name of a plain text file containing one word per line. All of the
words in the file are assumed to be spelled correctly and may appear
in any part of the document being processed.

You can use multiple text files with words to be added to the dictionary,
to do this all you need to do is use a list and include the name of your
text files.

For example::

  spelling_word_list_filename = ['spelling_wordlist.txt', 'my_wordlist.txt']

The ``spelling:word-list`` directive can be used to create a list of
words known to be spelled correctly within a single file.  For
example, if a document refers to a person or project by name, the name
can be added to the list of known words for just that document.

::

  .. spelling::

     Docutils
     Goodger

The ``spelling:word`` role can be used to annotate individual words as
being spelled correctly.


::

  This text refers to :spelling:word:`Goodger`.

.. _PyEnchant: https://github.com/rfk/pyenchant

Custom Word Filters
===================

The PyEnchant tokenizer supports a "filtering" API for processing
words from the input. Filters can alter the stream of words by adding,
replacing, or dropping values.

New filters should be derived from ``enchant.tokenize.Filter`` and
implement either the ``_split()`` method (to add or replace words) or
``_skip()`` (to treat words as being spelled correctly). For example,
this :class:`AcronymFilter` skips words that are all uppercase letters
or all uppercase with a trailing lowercase "s".

::
    
    class AcronymFilter(Filter):
        """If a word looks like an acronym (all upper case letters),
        ignore it.
        """

        def _skip(self, word):
            return (word.isupper() # all caps
                    or
                    # pluralized acronym ("URLs")
                    (word[-1].lower() == 's'
                     and
                     word[:-1].isupper()
                     )
                    )

To be used in a document, the custom filter needs to be installed
somewhere that Sphinx can import it while processing the input
files. The Sphinx project's ``conf.py`` then needs two changes.

1. Import the filter class.
2. Add the import string for the filter class to the
   ``spelling_filters`` configuration variable.

::

   spelling_filters = ['mymodule.MyFilter']

.. seealso::

   * `Creating a Spelling Checker for reStructuredText Documents
     <https://doughellmann.com/posts/creating-a-spelling-checker-for-restructuredtext-documents/>`_
   * `PyEnchant tutorial`_
