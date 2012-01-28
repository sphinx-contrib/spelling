# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

f = open('README', 'r')
try:
    long_desc = f.read()
finally:
    f.close()

requires = ['Sphinx>=0.6',
            #'PyEnchant>=1.6.5',
            ]

setup(
    name='sphinxcontrib-spelling',
    version='1.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    license='BSD',
    author='Doug Hellmann',
    author_email='doug.hellmann@gmail.com',
    description='Sphinx "spelling" extension',
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
