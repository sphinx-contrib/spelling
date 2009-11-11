.. -*- restructuredtext -*-

=============================
Gnuplot extension for Sphinx
=============================

:author: Vadim Gubergrits <vadim.gubergrits@gmail.com>


About
=====

This extensions allows rendering of plots using the gnuplot_ language. 

This extensions adds the ``gnuplot`` directive that will replace the gnuplot
commands with the image of the plot. 


Quick Example
-------------

This source::

    .. gnuplot::
        :title: The sine function

        plot sin(x)

is rendered as:

.. gnuplot::
    :title: The sine function

    plot sin(x)



Requirements
------------

* gnuplot_.

Gnuplot_ should be installed and be in the system's path.


Installing from sphinx-contrib checkout
---------------------------------------

Checkout sphinx-contrib::

  $ hg clone https://bitbucket.org/birkenfeld/sphinx-contrib/

Change into the gnuplot directory::

  $ cd sphinx-contrib/gnuplot
  
Install the module::

  $ python setup.py install



Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.gnuplot`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.gnuplot']


Usage
=====

Options
-------

``size``: X,Y
  Width and height of the resulting plot.

``title``: <TITLE>
  set the plot title to TITLE. Equivalent to "set title TITLE".


Configuration
-------------

For now one optional configuration is added to Sphinx_. It can be set in
``conf.py`` file:

``gnuplot_fromat`` <dict>:
  image format used for the different builders. ``latex`` and ``html`` fromats
  are supported.

  For example::

    gnuplot_format = dict(latex='pdf', html='png')

  These are the actual defaults.

  

Plotting data files
-------------------

Gnuplot is instructed to change its working directory to the document base
directory. When referencing data files in gnuplot they must be relative to the
document. 

To provide a link to the data source you can use Sphinx_ standard ``download`` role::

  .. gnuplot::

     plot 'data.dat' using 1:2
     
  The source is :download:`here <data.dat>`.



.. Links:
.. _gnuplot: http://www.gnuplot.info/
.. _Sphinx: http://sphinx.pocoo.org/

