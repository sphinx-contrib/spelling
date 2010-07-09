# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the sphinxcontrib-erlangdomain Sphinx extension.

This extension adds Erlang Domain to Sphinx.
It needs Sphinx 1.0 or newer.
'''

requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-erlangdomain',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-erlangdomain',
    license='BSD',
    author='SHIBUKAWA Yoshiki',
    author_email='yoshiki at shibu.jp',
    description='Sphinx extension sphinxcontrib-erlangdomain',
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
        'Programming Lauguage :: Erlang',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
