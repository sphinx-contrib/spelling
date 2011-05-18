seqdiag extension README
==========================
This is a sphinx extension which render sequence diagrams by using
`seqdiag <http://bitbucket.org/tk0miya/seqdiag/>`_ .

rendered:

.. seqdiag::

   diagram {
     browser => webserver => database;
   }

source:

.. code-block:: text

   .. seqdiag::

      diagram {
        browser => webserver => database;
      }

Setting
=======

.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-seqdiag>`_.

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Required components
-------------------
* `seqdiag <http://bitbucket.org/tk0miya/seqdiag>`_ .

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-seqdiag


Configure Sphinx
----------------
To enable this extension, add ``sphinxcontrib.seqdiag`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where seqdiag.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.seqdiag'))

   # Enabled extensions
   extensions = ['sphinxcontrib.seqdiag']


Directive
=========

.. describe:: .. seqdiag:: [filename]

   This directive insert a sequence diagram into the generated document.
   If filename is specified, sphinx reads external file as source script of blockfile.
   In another case, seqdiag directive takes code block as source script.

   Examples::

      .. seqdiag:: foobar.diag

      .. seqdiag::

         diagram {
            // some diagrams are here.
         }


Configuration File Options
==========================

.. confval:: seqdiag_fontpath

   This is a path for renderring fonts. You can use truetype font (.ttf) file path.

.. confval:: seqdiag_antialias

   If :confval:`seqdiag_antialias: is True, seqdiag generates images
   with anti-alias filter.


Repository
==========
This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
