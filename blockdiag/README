blockdiag extension README
==========================

This is a sphinx extension which render block diagrams by using
`blockdiag <http://bitbucket.org/tk0miya/blockdiag/>`_ .

rendered:

.. blockdiag::

   diagram {
     A -> B -> C;
          B -> D;
   }

source:

.. code-block:: text

   .. blockdiag::

      diagram {
        A -> B -> C;
             B -> D;
      }

Setting
=======

.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-blockdiag>`_.

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Required components
-------------------

* `blockdiag <http://bitbucket.org/tk0miya/blockdiag>`_ .

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-blockdiag


Configure Sphinx
----------------

To enable this extension, add ``sphinxcontrib.blockdiag`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where blockdiag.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.blockdiag'))

   # Enabled extensions
   extensions = ['sphinxcontrib.blockdiag']


Directive
=========

.. describe:: .. blockdiag:: [filename]

   This directive insert a block diagram into the generated document.
   If filename is specified, sphinx reads external file as source script of blockfile.
   In another case, blockdiag directive takes code block as source script.

   Examples::

      .. blockdiag:: foobar.diag

      .. blockdiag::

         diagram {
            // some diagrams are here.
         }


Configuration File Options
==========================

.. confval:: blockdiag_fontpath

   This is a path for renderring fonts. You can use truetype font (.ttf) file path.

.. confval:: blockdiag_antialias

   If :confval:`blockdiag_antialias: is True, blockdiag generates images
   with anti-alias filter.


Repository
==========

This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
