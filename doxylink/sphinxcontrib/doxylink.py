# -*- coding: utf-8 -*-
"""
doxylink
~~~~~~~~

Sphinx extension to link to external Doxygen API documentation.

It works much like the extlinks extension but it does some more processing to link C++ symbols against their Doxygen HTML documentation.

When generating your Doxygen documentation, you need to instruct it to create a 'tag' file. This is an XML file which contains the mapping between symbols and HTML files. To make Doxygen create this file ensure that you have a line like::

	GENERATE_TAGFILE = PolyVox.tag

in your ``Doxyfile``.

.. confval:: doxylink

	The environment is set up with a dictionary mapping the interpereted text role
	to a tuple of tag file and prefix:

	.. code-block:: python

		doxylink = {
			'polyvox' : ('/home/matt/PolyVox.tag', '/home/matt/PolyVox/html/'),
			'qtogre' : ('/home/matt/QtOgre.tag', '/home/matt/QtOgre/html/'),
		}

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

:copyright: Copyright 2010 by Matt Williams
:license: BSD, see LICENSE for details.
"""

from docutils import nodes, utils

import os

from sphinx.util.nodes import split_explicit_title

import xml.etree.ElementTree as ET

def find_url(doc, symbol):
	"""
	Return the URL for a given symbol.
	
	This is where the magic happens.
	This function could be a lot more clever. At present it required the passed symbol to be almost exactly the same as the entries in the Doxygen tag file.
	
	.. todo::
		
		Maybe print a list of all possible matches as a warning (but still only return the first)
	
	:Parameters:
		doc : xml.etree.ElementTree
			The XML DOM object
		symbol : string
			The symbol to lookup in the file. E.g. something like 'PolyVox::Array' or 'tidyUpMemory'
	
	:return: String representing the filename part of the URL
	"""
	
	#First check for an exact match with a top-level object (namespaces, objects etc.)
	
	#env = inliner.document.settings.env
	
	matches = []
	for compound in doc.findall('.//compound'):
		if compound.find('name').text == symbol:
			matches += [compound.find('filename').text]
	
	if len(matches) > 1:
		pass
		#env.warn(env.docname, 'There were multiple matches for `%s`: %s' % (symbol, matches))
	if len(matches) == 1:
		return matches[0]
	
	
	#Strip off first namespace bit of the compound name so that 'ArraySizes' can match 'PolyVox::ArraySizes'
	for compound in doc.findall('.//compound'):
		symbol_list = compound.find('name').text.split('::', 1)
		if len(symbol_list) == 2:
			reducedsymbol = symbol_list[1]
			if reducedsymbol == symbol:
				return compound.find('filename').text
	
	#Now split the symbol by '::'. Find an exact match for the first part and then a member match for the second
	#So PolyVox::Array::operator[] becomes like {namespace: "PolyVox::Array", endsymbol: "operator[]"}
	symbol_list = symbol.rsplit('::', 1)
	if len(symbol_list) == 2:
		namespace = symbol_list[0]
		endsymbol = symbol_list[1]
		for compound in doc.findall('.//compound'):
			if compound.find('name').text == namespace:
				for member in compound.findall('member'):
#					#If this compound object contains the matching member then return it
					if member.find('name').text == endsymbol:
						return member.find('anchorfile').text + '#' + member.find('anchor').text
	
	#Then we'll look at unqualified members
	for member in doc.findall('.//member'):
		if member.find('name').text == symbol:
			return member.find('anchorfile').text + '#' + member.find('anchor').text
	
	return None

def join(*args):
	return ''.join(args)

def create_role(app, tag_filename, rootdir):
	if not rootdir.endswith(('/', '\\')):
		rootdir = join(rootdir, os.sep)
	
	def find_doxygen_link(name, rawtext, text, lineno, inliner, options={}, content=[]):
		text = utils.unescape(text)
		# from :name:`title <part>`
		has_explicit_title, title, part = split_explicit_title(text)
		
		try:
			tag_file = ET.parse(tag_filename)
		except (IOError):
			env = inliner.document.settings.env
			env.warn(env.docname, 'Could not open %s' % tag_filename)
		else:
			url = find_url(tag_file, part)
			if url:
				
				#If it's an absolute path then the link will work regardless of the document directory
				if os.path.isabs(rootdir):
					full_url = join(rootdir, url)
				#But otherwise we need to add the relative path of the current document to the root source directory to the link
				else:
					relative_path_to_docsrc = os.path.relpath(app.env.srcdir, os.path.dirname(inliner.document.current_source))
					full_url = join(relative_path_to_docsrc, os.sep, rootdir, url)
				
				pnode = nodes.reference(title, title, internal=False, refuri=full_url)
				return [pnode], []
			#By here, no match was found
			env = app.env
			env.warn(env.docname, 'Could not find match for `%s` in `%s` tag file' % (part, tag_filename), lineno)
		
		pnode = nodes.inline(rawsource=title, text=title)
		return [pnode], []
		
	return find_doxygen_link

def setup_doxylink_roles(app):
	for name, [tag_filename, rootdir] in app.config.doxylink.iteritems():
		app.add_role(name, create_role(app, tag_filename, rootdir))

def setup(app):
	app.add_config_value('doxylink', {}, 'env')
	app.connect('builder-inited', setup_doxylink_roles)
