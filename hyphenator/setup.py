# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup, find_packages


with open('README') as stream:
    long_desc = stream.read()

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-hyphenator',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-hyphenator',
    license='BSD',
    author='bmu',
    author_email='diehose@freenet.de',
    description='Sphinx hyphenator.js hyphenation extension',
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
