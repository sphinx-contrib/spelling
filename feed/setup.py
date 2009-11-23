# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the ${name} Sphinx extension.

It creates an RSS feed of recently updated sphinx action.
'''

requires = ['Sphinx>=0.6']

setup(
    name='${name}',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/${name}',
    license='BSD',
    author='dan mackinlay',
    author_email='bitbucket@email.possumpalace.org',
    description='Sphinx extension ${name}',
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
