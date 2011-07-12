# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the seqdiag Sphinx extension.

.. _Sphinx: http://sphinx.pocoo.org/
.. _seqdiag: http://tk0miya.bitbucket.org/seqdiag/build/html/index.html

This extension enable you to insert sequence diagrams in your Sphinx document.
Following code is sample::

   .. seqdiag::

      diagram {
        browser => webserver => database;
      }


This module needs seqdiag_.
'''

requires = ['seqdiag>=0.3.3', 'Sphinx>=0.6']

setup(
    name='sphinxcontrib-seqdiag',
    version='0.2.0',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-seqdiag',
    license='BSD',
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "seqdiag" extension',
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
