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


.. _PyEnchant: http://www.rfk.id.au/software/pyenchant/
