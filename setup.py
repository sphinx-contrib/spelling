# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

f = open('README', 'r')
try:
    long_desc = f.read()
finally:
    f.close()

requires = [
    'Sphinx>=0.6',
    'six',

    # FIXME: I would love to have a proper depdency on PyEnchant
    # listed, but since it can't actually be installed from source
    # anywhere other than Linux (maybe not even there) we all
    # lose. Install the binaries.
    #
    #'PyEnchant>=1.6.5',

]

setup(
    name='sphinxcontrib-spelling',
    version='1.4',
    url='http://bitbucket.org/dhellmann/sphinxcontrib-spelling',
    license='BSD',
    author='Doug Hellmann',
    author_email='doug@doughellmann.com',
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
