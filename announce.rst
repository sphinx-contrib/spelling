============================
 sphinxcontrib.spelling 2.1
============================

.. tags:: python sphinx sphinxcontrib-spelling release 

What is sphinxcontrib.spelling?
===============================

`sphinxcontrib.spelling`_ is a spelling checker for Sphinx_.  It uses
PyEnchant_ to produce a report showing misspelled words.

.. _PyEnchant: http://www.rfk.id.au/software/pyenchant/

.. _Sphinx: http://sphinx.pocoo.org/

.. _sphinxcontrib.spelling: https://bitbucket.org/dhellmann/sphinxcontrib-spelling/overview


What's New in This Release?
===========================

- Fix unicode error in ``PythonBuiltinsFilter``.
- Make error output useful in emacs compiler mode
- Only show the words being added to a local dictionary if debugging
  is enabled.

Installing
==========

Please see the documentation_ for details.

.. _documentation: http://sphinxcontrib-spelling.readthedocs.org/en/latest/
