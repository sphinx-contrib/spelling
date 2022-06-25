.. spelling:word-list::

   sphinxcontrib

.. sphinxcontrib.spelling documentation master file, created by
   sphinx-quickstart on Sun Apr 17 15:33:23 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================
 sphinxcontrib.spelling
========================

``sphinxcontrib.spelling`` is a spelling checker for Sphinx_.  It uses
PyEnchant_ to produce a report showing misspelled words.

Features
========

1. Supports multiple source languages using the standard enchant
   dictionaries.
2. Supports project-specific dictionaries for localized jargon and
   other terminology that may not appear in the global dictionaries.
3. Suggests alternatives to words not found in the dictionary, when
   possible.

Details
=======

.. toctree::
   :maxdepth: 2

   install
   customize
   run
   developers
   history


.. _PyEnchant: https://github.com/rfk/pyenchant

.. _Sphinx: https://www.sphinx-doc.org/
