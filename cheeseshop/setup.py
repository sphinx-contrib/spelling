# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the cheeseshop Sphinx extension.

It allows to add links to Cheese Shop distribution releases and packages.
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-cheeseshop',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/cheeseshop',
    license='BSD',
    author='Richard Jones, Georg Brandl',
    author_email='georg@python.org',
    description='Sphinx extension cheeseshop',
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
