# -*- coding: utf-8 -*-

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

try:
    long_desc = open('README', 'r').read()
except IOError:
    long_desc = '''
This package contains an alternative integration of Sphinx and Paver allowing for both HTML and PDF generation from the same pavement.py file.
'''

requires = ['Sphinx>=0.6', 'Paver>=1.0.1']

NAME='sphinxcontrib-paverutils'
VERSION='1.2'

setup(
    name=NAME,
    version=VERSION,
    url = 'http://www.doughellmann.com/projects/%s/' % NAME,
    download_url = 'http://www.doughellmann.com/downloads/%s-%s.tar.gz' % \
                    (NAME, VERSION),
    license='BSD',
    author='Doug Hellmann',
    author_email='doug.hellmann@gmail.com',
    description='Sphinx/Paver integration',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
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
    py_modules = [ 'distribute_setup' ],
)
