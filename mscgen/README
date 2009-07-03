.. -*- restructuredtext -*-

========================
MSC extension for Sphinx
========================

:author: Leandro Lucarella <llucax@gmail.com>


About
=====

This extension  allow Mscgen_\ -formatted :abbr:`MSC (Message Sequence Chart)`
diagrams to be included in Sphinx_-generated documents inline.

Mscgen_ is a small program (inspired by `Graphviz Dot`_) that parses
:abbr:`MSC` descriptions and produces images as the output. :abbr:`MSC`\ s are
a way of representing entities and interactions over some time period, very
similar to UML sequence diagrams.

You can see the latest documentation at the `sphinxcontrib-mscgen website`__
or `download it in PDF format`__.

__ http://packages.python.org/sphinxcontrib-mscgen/
__ http://packages.python.org/sphinxcontrib-mscgen/sphinxcontrib-mscgen.pdf


Quick Example
-------------

This source::

   .. msc::

      hscale = "0.5";

      a,b,c;

      a->b [ label = "ab()" ] ;
      b->c [ label = "bc(TRUE)"];
      c=>c [ label = "process()" ];

is rendered as:

.. msc::

   hscale = "0.5";

   a,b,c;

   a->b [ label = "ab()" ] ;
   b->c [ label = "bc(TRUE)"];
   c=>c [ label = "process()" ];


Download
========

You can see all the `available versions`__ at PyPI_.

__ http://pypi.python.org/pypi/sphinxcontrib-mscgen


Install
=======

Requirements
------------

* mscgen_ (0.14 or later).
* epstopdf_ for LaTeX/PDF output.


From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the sphinxcontrib-mscgen-x.y directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually downloading the
files and installing as described above or using::

    easy_install -U sphinxcontrib-mscgen


Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.mscgen`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.mscgen']


Usage
=====

The Mscgen_ program is used to render the :abbr:`MSC`, so you should refer
to its documentation for details on how to specify the diagram. You should
have the program installed for this extension to work. If you need LaTeX
output, you'll need the epstopdf_ program too.

This extension adds the ``mscgen`` and ``msc`` directives. The former let
you specify a full diagram, the later let you omit the ``msc { ... }``
bits so you can jump right to the important stuff.

For an example on using the ``msc`` directive see the `Quick Example`_. If you
need full control over the :abbr:`MSC` diagram you can use the ``mscgen``
directive::

   .. mscgen::

      msc {
         hscale = "0.5";

         a,b,c;

         a->b [ label = "ab()" ] ;
         b->c [ label = "bc(TRUE)"];
         c=>c [ label = "process()" ];
      }

Which renders to exact the same image as the `Quick Example`_.


Configuration
-------------

A few configuration options are added (all optional, of course ;) to Sphinx_ so
you can set them in the ``conf.py`` file:

``mscgen``:
   location of the *mscgen* program. It's expected to be in the PATH by
   default. The full path, including the binary, should be given if that's
   not the case.

``mscgen_args``:
   extra command line arguments for *mscgen* (should be a list of
   strings).

``mscgen_epstopdf``:
   location of the *epstopdf* program. It's expected to be in the PATH by
   default. The full path, including the binary, should be given if that's
   not the case.

``mscgen_epstopdf_args``:
   extra command line arguments for *epstopdf* (should be a list of
   strings).

Remember to enable the extension first (see Install_ for details).


.. Links:
.. _Sphinx: http://sphinx.pocoo.org/
.. _Mscgen: http://www.mcternan.me.uk/mscgen/
.. _`Graphviz Dot`: http://www.graphviz.org/
.. _epstopdf: http://www.ctan.org/tex-archive/support/epstopdf/
.. _PyPI: http://pypi.python.org/pypi

