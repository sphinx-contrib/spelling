actdiag extension README
========================
This is a sphinx extension which render block diagrams by using
`actdiag <http://bitbucket.org/tk0miya/actdiag/>`_ .

rendered:

.. actdiag::

   diagram {
     A -> B -> C -> D;

     lane {
       A; B;
     }
     lane {
       C; D;
     }
   }

source:

.. code-block:: text

   .. actdiag::

      diagram {
        A -> B -> C -> D;

        lane {
          A; B;
        }
        lane {
          C; D;
        }
      }

Setting
=======
.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-actdiag>`_.

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Required components
-------------------
* `actdiag <http://bitbucket.org/tk0miya/actdiag>`_ .

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-actdiag


Configure Sphinx
----------------
To enable this extension, add ``sphinxcontrib.actdiag`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where actdiag.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.actdiag'))

   # Enabled extensions
   extensions = ['sphinxcontrib.actdiag']


Directive
=========

.. describe:: .. actdiag:: [filename]

   This directive insert a block diagram into the generated document.
   If filename is specified, sphinx reads external file as source script of blockfile.
   In another case, actdiag directive takes code block as source script.

   Examples::

      .. actdiag:: foobar.diag

      .. actdiag::

         diagram {
            // some diagrams are here.
         }


Configuration File Options
==========================

.. confval:: actdiag_fontpath

   This is a path for renderring fonts. You can use truetype font (.ttf) file path.

.. confval:: actdiag_antialias

   If :confval:`actdiag_antialias: is True, actdiag generates images
   with anti-alias filter.


Repository
==========
This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
