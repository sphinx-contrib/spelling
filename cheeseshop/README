================================
The Cheese Shop Sphinx extension
================================

   Ah! We do have some Camembert, sir...

This extension adds directives for easy linking to Cheese Shop (Python Package
Index) packages.  It requires Sphinx 1.0.

   It's a bit runny, sir...

It supports a directive and a role, as well as a new config value.

   Well, as a matter of fact it's very runny, sir...

The ``pypi-release`` directive adds an HTML-only output block that automatically
fetches the download links for the latest release of the given package and
displays them as a list.  For example, ::

   .. pypi-release:: Sphinx
      :prefix: Download
      :class: sidebar

will display "Download:" and a list of download links (eggs and the source
distribution) for the latest Sphinx release.  The "sidebar" class makes the
resulting ``<div>`` appear like a reStructuredText sidebar.  Using "prefix", you
can select what text precedes the list.

   I think it's runnier than you like it, sir...

The ``pypi`` role links to a package.  Use it in one of these forms::

   :pypi:`Sphinx`  -- link to latest release
   :pypi:`the Sphinx package <Sphinx>`  -- dito, but explicit title given
   :pypi:`Sphinx (0.6)`  -- link to specific release
   :pypi:`the Sphinx package <Sphinx (0.6)>`  -- dito, with explicit title

This extension also adds a ``cheeseshop_url`` config value, which defaults to
``'http://pypi.python.org/pypi'`` and is used to build URLs to the Cheese Shop.

Have fun!

   Oh... The cat's eaten it.
