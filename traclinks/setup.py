# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the traclinks Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

setup(
    name='traclinks',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/traclinks',
    license='MIT',
    author='Kevin Horn',
    author_email='kevin.horn@gmail.com',
    description='Sphinx extension traclinks',
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
