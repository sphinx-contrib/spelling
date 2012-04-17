# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the nwdiag Sphinx extension and rackdiag Sphinx extension.

.. _Sphinx: http://sphinx.pocoo.org/
.. _nwdiag: http://blockdiag.com/en/nwdiag/

This extension enable you to insert network diagrams into your Sphinx document.
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

And insert rack structure diagrams::

   .. rackdiag::

      diagram {
        rackheight = 12;

        1: UPS [height = 3];
        4: DB Server (Master)
        5: DB Server (Mirror)
        7: Web Server (1)
        8: Web Server (1)
        9: Web Server (1)
        10: LoadBalancer
      }


This module needs nwdiag_.
'''

requires = ['nwdiag>=0.7.0', 'Sphinx>=0.6']

setup(
    name='sphinxcontrib-nwdiag',
    version='0.4.0',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-nwdiag',
    license='BSD',
    author='Takeshi Komiya',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx "nwdiag" and "rackdiag" extension',
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
