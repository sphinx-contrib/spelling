#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the requirements Sphinx extension.

Allows declaring requirement specs wherever in the documentation (for instance,
in docstrings of UnitTest.test_* methods) and displaying them as a single
list.
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-requirements',
    version='0.1',
    url='http://bitbucket.org/neithere/sphinx-contrib-requirements',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-requirements',
    license='BSD',
    author='Andrey Mikhaylenko',
    author_email='neithere@gmail.com',
    description='Sphinx "requirements" extension',
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
