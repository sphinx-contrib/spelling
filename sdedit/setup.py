# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the Sphinx_ extension for sdedit_.

.. _Sphinx: http://sphinx.pocoo.org/
.. _sdedit: http://sdedit.sourceforge.net/

This extension enable you to insert sequence diagrams of UML in your Sphinx docu
ment. Following code is sample::

   .. sequence-diagram::

      actor:Actor
      sphinx:Sphinx[a]
      dot:Graphviz
      sdedit:Quick Sequence Diagram Editor

      actor:sphinx.make html
      sphinx:dot.render_diagram()
      sphinx:sdedit.render_diagram()


This module needs sdedit_ and PIL.
'''

requires = ['Sphinx>=0.6', 'PIL']

setup(
    name='sphinxcontrib-sdedit',
    version='0.3',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-sdedit',
    license='BSD',
    author='SHIBUKAWA Yoshiki',
    author_email='yoshiki@shibu.jp',
    description='Sphinx extension for drawing sequence diagrams',
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
