nicovideo extension README
==========================
This is a sphinx extension which embed videos from nicovideo_ .

.. _nicovideo:: http://www.nicovideo.jp/

Setting
=======

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-nicovideo


Configure Sphinx
----------------
To enable this extension, add ``sphinxcontrib.nicovideo`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where nicovideo.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.nicovideo'))

   # Enabled extensions
   extensions = ['sphinxcontrib.nicovideo']


Directives and Roles
=====================

.. rst:role: nicovideo

   nicovideo role makes a link to movie page::

      :nicovideo:`sm9`

.. rst:directive:: .. nicovideo:: [video_id]

   nicovideo directive embeds a movie into the generated document.


Repository
==========
This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
