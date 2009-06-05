# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the mscgen Sphinx extension.

Allow mscgen-formatted Message Sequence Chart graphs to be included in
Sphinx-generated documents inline.
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-mscgen',
    version='0.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/mscgen',
    license='BSD',
    author='Leandro Lucarella',
    author_email='llucax@gmail.com',
    description='Sphinx extension mscgen',
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
