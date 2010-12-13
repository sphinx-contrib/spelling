# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the omegat Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-omegat',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-omegat',
    license='BSD',
    author='SHIBUKAWA Yoshiki',
    author_email='yoshiki at shibu.jp',
    description='Sphinx "omegat" extension',
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
    package_data = {'': ["omegat.project"]},
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
