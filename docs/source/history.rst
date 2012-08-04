.. .. spelling::

..    wordlist
..    txt

=================
 Release History
=================

dev

  - Fixed detection of builtins under PyPy, contributed by Hong Minhee
    (https://bitbucket.org/dahlia).

1.3

  - Handle text nodes without parents. (#19)
  - Include the input document name in the console output.
  - Use the Sphinx wrapper for registering a directive.

1.2

  - Add the document name to the messages showing the contents of a
    local dictionary created by the ``spelling`` directive.
  - Add title nodes to the list of node types checked for
    spelling. Resolves issue #17.
  - Add test/test_wordlist.txt to the manifest so it is included in
    the source distribution and the tests will pass. Resolves issue
    #17.
  - Documentation patch from Hank Gay.

1.1.1

  - Fix initialization so the per-document filters work even if no
    ``spelling`` directive is used.

1.1

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

  - Re-implement using just a Builder, without a separate visitor
    class.
  - Show the file and line number of any words not appearing in the
    dictionary, instead of the section title.
  - Log the file, line, and unknown words as the documents are
    processed.

0.2

  - Warn but otherwise ignore unknown node types.

0.1

  - First public release.
