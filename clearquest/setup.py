#!/usr/bin/env python

from setuptools import setup, find_packages

long_desc = open('README', 'r').read()

# We need 'pywin32' too but it is not available on pypi.
# To avoid crashes of easy_install and pip, I removed the dependency here.
requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-clearquest',
    version='0.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-clearquest',
    license='BSD',
    author='Robin Jarry',
    author_email='robin.jarry@gmail.com',
    description='Sphinx "clearquest" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    keywords=['clearquest', 'sphinx'],
    platforms='Windows',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
