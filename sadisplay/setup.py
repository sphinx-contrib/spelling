# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))


requires = [
    'Sphinx>=0.6',
    'sadisplay>=0.3',
]


setup(
    name='sphinxcontrib-sadisplay',
    version='0.3.1',
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    #packages=['sphinxcontib',],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    tests_require=['nose >= 1.0',],
    test_suite = 'nose.collector',
    namespace_packages=['sphinxcontrib'],
)
