# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the nwdiag Sphinx extension.

.. _Sphinx: http://sphinx.pocoo.org/
.. _nwdiag: http://tk0miya.bitbucket.org/nwdiag/build/html/index.html

This extension enable you to insert network diagrams in your Sphinx document.
Following code is sample::

   .. nwdiag::

      diagram {
        network {
          web01; web02;
        }
        network {
          web01; web02; db01;
        }
      }


This module needs nwdiag_.
'''

requires = ['nwdiag>=0.2.3', 'Sphinx>=0.6']

setup(
    name='sphinxcontrib-nwdiag',
    version='0.2.0',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-nwdiag',
    license='BSD',
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "nwdiag" extension',
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
