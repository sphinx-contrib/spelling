# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the phpdomain Sphinx extension.

This extension provides a PHP domain for sphinx

'''

requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-phpdomain',
    version='0.1.2',
    url='http://bitbucket.org/markstory/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-phpdomain',
    license='BSD',
    author='Mark Story',
    author_email='mark at mark-story dot com',
    description='Sphinx "phpdomain" extension',
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
