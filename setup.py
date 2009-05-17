# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains contributed Sphinx extensions.  Currently these are:

.. Add your extension here...

The development version can be found `here
<http://bitbucket.org/birkenfeld/sphinx-contrib/get/tip.gz#egg=sphinx-contrib-dev>`_.
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinx-contrib',
    version='0.1',
    url='http://sphinx.pocoo.org/',
    download_url='http://pypi.python.org/pypi/sphinx-contrib',
    license='BSD',
    author='Multiple authors',
    description='Contributed extensions for Sphinx',
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
)
