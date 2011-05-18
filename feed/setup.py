# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the feed Sphinx extension.

It creates an RSS feed of recently updated sphinx pages.
'''

requires = ['Sphinx>=0.6', 'python-dateutil<2', 'html5lib']
tests_require = ['BeautifulSoup>=3.2.0', 'feedparser', 'nose']

setup(
    name='feed',
    version='0.2',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    # download_url='http://pypi.python.org/pypi/feed',
    license='BSD',
    author='dan mackinlay',
    author_email='bitbucket@email.possumpalace.org',
    description='Sphinx extension feed',
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
    test_suite='nose.collector',
    tests_require=tests_require,
    namespace_packages=['sphinxcontrib'],
)
