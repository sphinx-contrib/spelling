.. -*- restructuredtext -*-

=============================
aafigure extension for Sphinx
=============================

:author: Leandro Lucarella <llucax@gmail.com>


About
=====

This extension allows embedded ASCII art to be rendered as nice looking images
using aafigure_.

aafigure_ is a program and a reStructuredText_ directive to allow embedded
ASCII art figures to be rendered as nice images in various image formats. The
aafigure_ directive needs a *hardcoded* image format, so it doesn't goes well
with Sphinx_ multi-format support.

This extension adds the ``aafig`` directive that automatically selects the
image format to use acording to the Sphinx_ writer used to generate the
documentation.

You can see the latest documentation at the `sphinxcontrib-aafig website`__
or `download it in PDF format`__.

__ http://packages.python.org/sphinxcontrib-aafig/
__ http://packages.python.org/sphinxcontrib-aafig/sphinxcontrib-aafig.pdf


Quick Example
-------------

This source::

    .. aafig::
        :aspect: 60
        :scale: 150
        :proportional:
        :textual:

        +-------+         +-----------+
        | Hello +-------->+ aafigure! |
        +-------+         +-----------+

is rendered as:

.. aafig::
    :aspect: 60
    :scale: 150
    :proportional:
    :textual:

    +-------+         +-----------+
    | Hello +-------->+ aafigure! |
    +-------+         +-----------+


Download
========

You can see all the `available versions`__ at PyPI_.

__ http://pypi.python.org/pypi/sphinxcontrib-aafig


Requirements
------------

* aafigure_ (0.3 or later).
* reportlab_ (for LaTeX/PDF output)
* PIL_ (for any image format other than SVG or PDF)

aafigure_ should be installed in the system for this extension to work.
Alternatively you can download it to any folder and add that folder to the
Python's path through the Sphinx_ ``conf.py`` file, for example::

    import sys, os

    sys.path.extend(os.path.abspath('path/to/aafigure')])


From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the sphinxcontrib-aafig-x.y directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually downloading the
files and installing as described above or using:

easy_install -U sphinxcontrib-aafig


Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.aafig`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.aafig']


Usage
=====

You can always use the original reStructuredText_ aafigure_ extension, but
choosing a hardcoded format can be a bad idea when using Sphinx, because PDF
might not be suitable for HTML and PNG can look ugly in a PDF document.

This extension uses the same aafigure_ code to add a more *Sphinxy* directive
called ``aafig``. This directive accepts the same options as the original
aafigure_ directive (please, see aafigure_ documentation for more information).
There are some differences though:

* The ``:format:`` option is not available, the format is selected
  automatically depending on the Sphinx_ builder you are using.
* ``:scale:`` and ``:aspect:`` options are specified using percentages
  (without the *%* sign), to match the reStructuredText_ image directive.

For an example on using the ``aafig`` directive see the `Quick Example`_.


Configuration
-------------

A few configuration options are added (all optional, of course ;) to Sphinx_
so you can set them in the ``conf.py`` file:

``aafig_format`` <dict>:
   image format used for the different builders. All ``latex``, ``html`` and
   ``text`` builder are supported, and it should be trivial to add support for
   other builders if they correctly handle images (and if aafigure_ can render
   an image format suitable for that builder) by just adding the correct format
   mapping here.

   A special format ``None`` is supported, which means not to use aafigure_ to
   render the image, just show the raw ASCII art as is in the resulting
   document (using a literal block). This is almost only useful for the text
   builder.

   You can specify the format - builder mapping using a dict. For example::

      aafig_format = dict(latex='pdf', html='svg', text=None)

   These are the actual defaults.

``aafig_default_options`` <dict>:
    default aafigure_ options. These options are used by default unless they
    are overridden explicitly in the ``aafig`` directive. The default aafigure_
    options are used if this is not specified. You can provide partial
    defaults, for example::

        aafig_default_options = dict(scale=1.5, aspect=0.5, proportional=True)

    Note that in this case the ``aspec`` and ``scale`` options are specified
    as floats, as originally done by aafigure_. See aafigure_ documentation
    for a complete list of options and their defaults.


TODO
====

* Add color validation for ``fill``, ``background`` and ``foreground`` options.
* Add ``aa`` role for easily embed small images (like arrows).


.. Links:
.. _aafigure: http://launchpad.net/aafigure
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _reportlab: http://www.reportlab.org/
.. _PIL: http://www.pythonware.com/products/pil/
.. _PyPI: http://pypi.python.org/pypi

