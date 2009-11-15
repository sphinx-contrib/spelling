# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the aafigure_ Sphinx_ extension.

.. _aafigure: https://launchpad.net/aafigure
.. _Sphinx: http://sphinx.pocoo.org/

aafigure_ is a program and a reStructuredText_ directive to allow embeded ASCII
art figures to be rendered as nice images in various image formats. The
aafigure_ directive needs a *hardcoded* image format, so it doesn't goes well
with Sphinx_ multi-format support.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

This extension adds the ``aafig`` directive that automatically selects the
image format to use acording to the Sphinx_ writer used to generate the
documentation.

Usage example::

    .. aafig::
        :aspect: 60
        :scale: 150
        :proportional:
        :textual:

        +-------+         +-----------+
        | Hello +-------->+ aafigure! |
        +-------+         +-----------+

'''

requires = ['Sphinx>=0.6', 'aafigure>=0.3']

setup(
    name='sphinxcontrib-aafig',
    version='1.0',
    url='http://packages.python.org/sphinxcontrib-aafig/',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-aafig',
    license='BOLA',
    author='Leandro Lucarella',
    author_email='llucax@gmail.com',
    description='aafig Sphinx extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
