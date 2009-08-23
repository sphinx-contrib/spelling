# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = """
This package contains the Whoosh_ Sphinx_ extension.

.. _Whoosh: http://whoosh.ca/
.. _Sphinx: http://sphinx.pocoo.org/

Whoosh is a pure-Python full-text indexing search engine, and this extension
indexes a Sphinx document using it.

"""

requires = ['Sphinx>=0.6', 'Whoosh>=0.3']

setup(
    name='sphinxcontrib-whoosh',
    version='0.1',
    url='http://packages.python.org/sphinxcontrib-whoosh/',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-whoosh',
    license='BSD',
    author='Pauli Virtanen',
    author_email='pav@iki.fi',
    description='Whoosh Sphinx extension',
    long_description=long_desc,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
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
