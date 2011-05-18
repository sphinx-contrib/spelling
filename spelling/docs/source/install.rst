.. spelling::

   wikis

==============
 Installation
==============

Installing sphinxcontrib.spelling
=================================

1. Follow the instructions on the PyEnchant_ site to install
   **enchant** and then **PyEnchant**.
2. ``pip install sphinxcontrib-spelling``

Configuration
=============

1. Add ``'sphinxcontrib.spelling'`` to the ``extensions`` list in ``conf.py``.

  ::

    extensions = [ 'sphinxcontrib.spelling' ]

.. _install-options:

Configuration Options
=====================

``spelling_show_suggestions``
  Boolean controlling whether suggestions for misspelled words are
  printed.  Defaults to False.
``spelling_lang``
  String specifying the language, as understood by PyEnchant and
  enchant.  Defaults to ``en_US`` for US English.
``spelling_word_list_filename``
  String specifying a file containing a list of words known to be
  spelled correctly but that do not appear in the language dictionary
  selected by ``spelling_lang``.  The file should contain one word per
  line.  Refer to the `PyEnchant tutoral
  <http://www.rfk.id.au/software/pyenchant/tutorial.html>`_ for
  details.
``spelling_ignore_pypi_package_names``
  Boolean controlling whether words that look like package names from
  PyPI are treated as spelled properly. When ``True``, the current
  list of package names is downloaded at the start of the build and
  used to extend the list of known words in the dictionary. Defaults
  to ``False``.
``spelling_ignore_wiki_words``
  Boolean controlling whether words that follow the CamelCase
  conventions used for page names in wikis should be treated as
  spelled properly. Defaults to ``True``.
``spelling_ignore_acronyms``
  Boolean controlling treatment of words that appear in all capital
  letters, or all capital letters followed by a lower case ``s``. When
  ``True``, acronyms are assumed to be spelled properly. Defaults to
  ``True``.
``spelling_ignore_python_builtins``
  Boolean controlling whether names built in to Python should be
  treated as spelled properly. Defaults to ``True``.
``spelling_ignore_importable_modules``
  Boolean controlling whether words that are names of modules found on
  ``sys.path`` are treated as spelled properly. Defaults to ``True``.
``spelling_filters``
  List of filter classes to be added to the tokenizer that produces
  words to be checked. The classes should be derived from
  ``enchant.tokenize.Filter``. Refer to `the PyEnchant tutorial
  <http://www.rfk.id.au/software/pyenchant/tutorial.html#basics>`__
  for examples.

.. _PyEnchant: http://www.rfk.id.au/software/pyenchant/
