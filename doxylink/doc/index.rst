Welcome to sphinxcontrib-doxylink's documentation
=================================================

Doxylink is a Sphinx extension to link to external Doxygen API documentation.

It works much like the extlinks extension but it does some more processing to link C++ symbols against their Doxygen HTML documentation.

Usage
-----

You use Doxylink like:

.. code-block:: rst

	:polyvox:`Array <PolyVox::Array>`.
	:polyvox:`PolyVox::Volume`
	:qtogre:`QtOgre::Log`
	:polyvox:`tidyUpMemory(int) <tidyUpMemory>`
	:polyvox:`PolyVox::Array::operator[]`

Where ``polyvox`` and ``qtogre`` roles are defined by the :confval:`doxylink` configuration value.

Namespaces, classes etc.
^^^^^^^^^^^^^^^^^^^^^^^^

For non-functions (i.e. namespaces, classes, enums, variables) you simply pass in the name of the symbol. If you pass in a partial symbol, e.g. ```Volume``` when you have a symbol in C++ called ``PolyVox::Utils::Volume`` then it would be able to match it as long as there is no ambiguity (e.g. with another symbol called ``PolyVox::Old::Volume``).

Functions
^^^^^^^^^

For functions there is more to be considered due to C++'s ability to overload a function with multiple signatures. If you want to link to a function and either that function is not overloaded or you don't care which version of it you link to, you can simply give the name of the function with no parentheses:

.. code-block:: rst

	:polyvox:`PolyVox::Volume::getVoxelAt`

Depending on whether you have set the :confval:`add_function_parentheses` configuration value, Doxylink will automatically add on parentheses to that it will be printed as ``PolyVox::Volume::getVoxelAt()``.

If you want to link to a specific version of the function, you must provide the correct signature. For a requested signature to match on in the tag file, it must exactly match a number of features:

- The types must be correct, including all qualifiers, e.g. ``unsigned const int``
- You must include any pointer or reference labeling, e.g. ``char*``, ``const QString &`` or ``int **``
- You must include whether the function is const, e.g. ``getx() const``

The argument list is not whitespace sensitive (any more than C++ is anyway) and the names of the arguments and their default values are ignored so the following are all considered equivalent:

.. code-block:: rst

	:myapi:`foo( const QString & text, bool recalc, bool redraw = true )`
	:myapi:`foo(const QString &foo, bool recalc, bool redraw = true )`
	:myapi:`foo( const QString& text, bool recalc, bool redraw )`
	:myapi:`foo(const QString&,bool,bool)`

When making a match, Doxylink splits up the requested string into the function symbol and the argument list. If it finds a match for the function symbol part but not for the argument list then it will return a link to any one of the function versions.

Setup
-----

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

.. confval:: add_function_parentheses

   A boolean that decides whether parentheses are appended to function and method role text. Default is ``True``.

Function reference
------------------

.. automodule:: sphinxcontrib.doxylink

.. automodule:: sphinxcontrib.parsing

:requires: Python 2.5

.. todo::

	Make the extension atuomatically re-run if the tag file is altered on disc
	
	Find a way to parse the tag file to a DOM tree *once* and then just reference it from then on.
	
	Correct function overloading when arguments are given.

:copyright: Copyright 2010 by Matt Williams
:license: BSD, see LICENSE for details.

