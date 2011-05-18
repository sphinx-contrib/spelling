# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the blockdiag Sphinx extension.

.. _Sphinx: http://sphinx.pocoo.org/
.. _blockdiag: http://tk0miya.bitbucket.org/blockdiag/build/html/index.html

This extension enable you to insert block diagrams in your Sphinx document.
Following code is sample::

   .. blockdiag::

      diagram {
        A -> B -> C;
             B -> D;
      }


This module needs blockdiag_.
'''

requires = ['blockdiag>=0.8.0', 'Sphinx>=0.6']

setup(
    name='sphinxcontrib-blockdiag',
    version='0.8.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-blockdiag',
    license='BSD',
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "blockdiag" extension',
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
