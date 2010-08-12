Welcome to sphinxcontrib-doxylink's documentation
=================================================

Doxylink is a Sphinx extension to link to external Doxygen API documentation.

It works much like the extlinks extension but it does some more processing to link C++ symbols against their Doxygen HTML documentation.

When generating your Doxygen documentation, you need to instruct it to create a 'tag' file. This is an XML file which contains the mapping between symbols and HTML files. To make Doxygen create this file ensure that you have a line like:

.. code-block:: ini

	GENERATE_TAGFILE = PolyVox.tag

in your ``Doxyfile``.

Configuration values
--------------------

.. confval:: doxylink

	The environment is set up with a dictionary mapping the interpereted text role
	to a tuple of tag file and prefix:
	
	.. code-block:: python
	
		doxylink = {
			'polyvox' : ('/home/matt/PolyVox.tag', '/home/matt/PolyVox/html/'),
			'qtogre' : ('/home/matt/QtOgre.tag', '/home/matt/QtOgre/html/'),
		}

Usage
-----

This allows one to do:

.. code-block:: rst

	:polyvox:`Array <PolyVox::Array>`.
	:polyvox:`PolyVox::Volume`
	:qtogre:`QtOgre::Log`
	:polyvox:`tidyUpMemeory(int) <tidyUpMemory>`
	:polyvox:`PolyVox::Array::operator[]`

:requires: Python 2.5

.. todo::

	Make the extension atuomatically re-run if the tag file is altered on disc
	
	Find a way to parse the tag file to a DOM tree *once* and then just reference it from then on.
	
	Correct function overloading when arguments are given.

:copyright: Copyright 2010 by Matt Williams
:license: BSD, see LICENSE for details.

