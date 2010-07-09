# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the osaka Sphinx extension.

This module converts standard Japanese sentence into Osaka dialect. Osaka is one of the most powerful area in Japan. So your formal Japanese sentence will become lively one.
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-osaka',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-osaka',
    license='BSD',
    author='SHIBUKAWA Yoshiki',
    author_email='yoshiki at shibu.jp',
    description='Sphinx extension osaka',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Linguistic',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
