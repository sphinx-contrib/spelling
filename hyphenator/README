sphinxcontrib.hyphenator
========================

This extension provides hyphenation for html documentation generated
with Sphinx_. It loads the JavaScript package hypenator.js_ to hyphenate
documents on client side.

Because hyphenator.js is quite large, it is not included in the extension.

Configuration Parameters
------------------------

hyphenator_path

   The path to the hyphenator.js file. 

   Default value is http://hyphenator.googlecode.com/svn/trunk/
   that loads the JavaScript from the project repository. If you want
   Hyphenator to be available offline, you have to download it and set this
   value to a different path.

   The path can be absolute or relative; if it is relative, it is relative to
   the _static directory of the built docs.

hyphenator_language

   The hyphenator extension sets the language for hyphenator.js to the config
   value "language". If this does not work you can set hyphenator_language in
   your conf.py
   (see: http://code.google.com/p/hyphenator/wiki/en_AddNewLanguage for
   supported languages).


.. _`Sphinx`: http://sphinx.pocoo.org/latest
.. _`hypenator.js`: http://code.google.com/p/hyphenator/
