# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the zopeext Sphinx extension.

To use, install the extension by running `python setup.py install` and
then include `'sphinxcontrib.zopeext.autointerface'` in your
`extensions` list in the `conf.py` file for your documentation.

This provides some support for Zope interfaces by providing an
:dir:`autointerface` directive that acts like :dir:`autoclass` except
uses the Zope interface methods for attribute and method lookup (the
interface mechanism hides the attributes and method so the usual
:dir:`autoclass` directive fails.)  Interfaces are intended to be very
different beasts than regular python classes, and as a result require
customized access to documentation, signatures etc.

.. seealso:: :mod:`sphinx.ext.autodoc`

.. note:: This extension also serves as a simple example of using the
   new sphinx version 6.0 version :mod:`autodoc` refactoring.  Mostly
   this was straight forward, but I stumbled across a "gotcha":

   The `objtype` attribute of the documenters needs to be unique.
   Thus, for example, :attr:`InterfaceMethodDocumenter.objtype`
   cannot be `'method'` because this would overwrite the entry in
   :attr:`AutoDirective._registry` used to choose the correct
   documenter.
'''

requires = ['Sphinx>=0.6', 'zope.interface']

setup(
    name='zopeext',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/zopeext',
    license='BSD',
    author='Michael McNeil Forbes',
    author_email='mforbes@alum.mit.edu',
    description='Sphinx extension zopeext',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
