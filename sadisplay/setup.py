# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))


requires = [
    'Sphinx>=0.6',
    'sadisplay',
    'sphinxcontrib-plantuml'
]


setup(
    name='sphinxcontrib-sadisplay',
    version='0.2',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-sadisplay',
    license='BSD',
    author='Evgeniy Tatarkin',
    author_email='tatarkin.evg@gmail.com',
    description='Sphinx "sadisplay" extension',
    long_description=open(os.path.join(here, 'README')).read(),
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
