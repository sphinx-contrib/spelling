# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This contrib extension, sphinxcontrib.httpdomain provides a Sphinx
domain for describing RESTful HTTP APIs.

You can find the documentation from the following URL:

http://packages.python.org/sphinxcontrib-httpdomain/
'''

requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-httpdomain',
    version='1.1.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-httpdomain',
    license='BSD',
    author='Hong Minhee',
    author_email='minhee@dahlia.kr',
    description='Sphinx domain for HTTP APIs',
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
