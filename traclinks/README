.. -*- restructuredtext -*-

==================================
README for sphinxcontrib.traclinks
==================================

:author: Kevin Horn <kevin.horn@gmail.com>

.. module:: sphinxcontrib.traclinks
   :synopsis: Create TracLinks_ to a Trac instance from a Sphinx project.


This Sphinx extension adds a docutils role to create links to a Trac 
instance.

Licensing
---------
This code is released under an MIT License.  
See the LICENSE file for full text.

Requirements
------------
The target trac instance *must* support dispatching of InterTrac_ links.

For example, it must know what to do with a link like this::
    
    http://trac.edgewall.org/intertrac/ticket:1234


Installing from sphinx-contrib checkout
---------------------------------------

Clone the sphinx-contrib repository::

  $ hg clone https://bitbucket.org/birkenfeld/sphinx-contrib/

Change into the traclinks directory::

  $ cd sphinx-contrib/traclinks
  
Install the module::

  $ python setup.py install
  

Enabling the extension in Sphinx_
---------------------------------

To enable the use of this extension in your Sphinx project, you will need 
to add it to the list of extensions in the ``conf.py`` file in your Sphinx 
project.

For example::

    extensions = ['sphinxcontrib.traclinks']


Configuration
-------------

You will need to set the following config value in your Sphinx project's 
``conf.py`` file::

``traclinks_base_url`` <string>:
    The base url of the Trac instance you want to create links to.
    
Usage
-----

In your restructuredText markup, you can create links to various Trac 
entities using markup of the following format::

    :trac:`trac-links-text`
    
where ``trac-links-text`` is valid TracLinks_ markup.

For example, to link to a Trac ticket::

    trac:`#1234`
    
Or to link to a Trac wiki page::

    trac:`wiki:TracWiki`

.. Links:
.. _Sphinx: http://sphinx.pocoo.org/
.. _TracLinks: http://trac.edgewall.org/wiki/TracLinks
.. _InterTrac: http://trac.edgewall.org/wiki/InterTrac
