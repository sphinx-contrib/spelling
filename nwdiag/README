nwdiag extension README
==========================
This is a sphinx extension which render network diagrams by using
`nwdiag <http://bitbucket.org/tk0miya/nwdiag/>`_ .

rendered:

.. nwdiag::

   diagram {
     network {
       web01; web02;
     }
     network {
       web01; web02; db01;
     }
   }

source:

.. code-block:: text

   .. nwdiag::

      diagram {
        network {
          web01; web02;
        }
        network {
          web01; web02; db01;
        }
      }

Setting
=======
.. You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxcontrib-nwdiag>`_.

You can get archive file at http://bitbucket.org/birkenfeld/sphinx-contrib/

Required components
-------------------
* `nwdiag <http://bitbucket.org/tk0miya/nwdiag>`_ .

Install
-------

.. code-block:: bash

   > easy_install sphinxcontrib-nwdiag


Configure Sphinx
----------------
To enable this extension, add ``sphinxcontrib.nwdiag`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   import os, sys

   # Path to the folder where nwdiag.py is
   # NOTE: not needed if the package is installed in traditional way
   # using setup.py or easy_install
   sys.path.append(os.path.abspath('/path/to/sphinxcontrib.nwdiag'))

   # Enabled extensions
   extensions = ['sphinxcontrib.nwdiag']


Directive
=========

.. describe:: .. nwdiag:: [filename]

   This directive insert a network diagram into the generated document.
   If filename is specified, sphinx reads external file as source script of blockfile.
   In another case, nwdiag directive takes code block as source script.

   Examples::

      .. nwdiag:: foobar.diag

      .. nwdiag::

         diagram {
            // some diagrams are here.
         }


Configuration File Options
==========================

.. confval:: nwdiag_fontpath

   This is a path for renderring fonts. You can use truetype font (.ttf) file path.

.. confval:: nwdiag_antialias

   If :confval:`nwdiag_antialias: is True, nwdiag generates images
   with anti-alias filter.


Repository
==========
This code is hosted by Bitbucket.

  http://bitbucket.org/birkenfeld/sphinx-contrib/
