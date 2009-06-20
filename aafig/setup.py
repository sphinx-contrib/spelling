# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the aafigure_ Sphinx_ extension.

.. _aafigure: http://docutils.sourceforge.net/sandbox/aafigure/
.. _Sphinx: http://sphinx.pocoo.org/

_aafigure is a program and a reStructuredText_ directive to allow embeded ASCII
art figures to be rendered as nice images in various image formats. The
aafigure_ directive needs a *hardcoded* image format, so it doesn't goes well
with Sphinx_ multi-format support.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

This extension adds the ``aafig`` directive that automatically selects the
image format to use acording to the Sphinx_ writer used to generate the
documentation.
'''

requires = ['Sphinx>=0.6', 'aafigure>=0.3']

setup(
    name='sphinxcontrib-aafig',
    version='0.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-aafig',
    license='BSD',
    author='Leandro Lucarella',
    author_email='llucax@gmail.com',
    description='aafig Sphinx extension',
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
