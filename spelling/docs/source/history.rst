=================
 Release History
=================

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
