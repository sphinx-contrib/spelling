rawfiles extension README
=========================
Copy raw files, like a CNAME.

Setting
=======
.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-rawfiles>`_.

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Install
-------

::

   > easy_install sphinxcontrib-rawfiles

Configure Sphinx
----------------
To enable this extension, add ``sphinxcontrib.rawfiles`` module to extensions
option at `conf.py` and add .

::

   import os, sys

   # Path to the folder where rawfiles.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.rawfiles'))

   # Enabled extensions
   extensions = ['sphinxcontrib.rawfiles']

   # Files you want to copy
   rawfiles = ['CNAME']

Repository
==========
This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
