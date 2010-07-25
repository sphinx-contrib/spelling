# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as stream:
    long_desc = stream.read()


requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-programoutput',
    version='0.4',
    url='http://packages.python.org/sphinxcontrib-programoutput',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-programoutput',
    license='BSD',
    author='Sebastian Wiesner',
    author_email='lunaryorn@googlemail.com',
    description='Sphinx extension to include program output',
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
