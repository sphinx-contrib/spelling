#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@googlemail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import pytest
from sphinx.application import Sphinx
from sphinx.domains.python import PythonDomain
from docutils import nodes


#: conf.py contents for the test application
CONF_PY = """\
extensions = ['sphinxcontrib.epydoc']

source_suffix = '.rst'

master_doc = 'index'

project = u'epydoc-test'
copyright = u'2011, foo'

version = '1'
release = '1'

exclude_patterns = []

pygments_style = 'sphinx'
html_theme = 'default'

epydoc_mapping = {'http://eggs/': [r'eggs(\.|$)', r'chicken\.'],
                  'http://spam/': [r'spam(\.|$)']}
"""


def pytest_funcarg__content(request):
    """
    Document content for the current test, extracted from the ``with_content``
    marker.
    """
    content = request.keywords['with_content'].args[0]
    return content


def pytest_funcarg__srcdir(request):
    """
    Generated source directory for test Sphinx application.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    srcdir = tmpdir.join('src')
    srcdir.ensure(dir=True)
    confpy = srcdir.join('conf.py')
    confpy.write(CONF_PY)
    content = request.getfuncargvalue('content')
    srcdir.join('index.rst').write(content)
    return srcdir


def pytest_funcarg__outdir(request):
    """
    Output directory for current test.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('html')


def pytest_funcarg__doctreedir(request):
    """
    The doctree directory for the current.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('doctrees')


def pytest_funcarg__confoverrides(request):
    """
    Confoverrides for the current test as dict, extracted from the keyword
    arguments to the ``confoverrides`` marker.
    """
    confoverrides_marker = request.keywords.get('confoverrides')
    if confoverrides_marker:
        return confoverrides_marker.kwargs
    else:
        return {}


def pytest_funcarg__app(request):
    """
    *Built* Sphinx application for the current test.
    """
    srcdir = request.getfuncargvalue('srcdir')
    outdir = request.getfuncargvalue('outdir')
    doctreedir = request.getfuncargvalue('doctreedir')
    confoverrides = request.getfuncargvalue('confoverrides')
    app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir), 'html',
                 status=None, warning=None, freshenv=None,
                 confoverrides=confoverrides)
    app.build()
    return app


def pytest_funcarg__doctree(request):
    """
    Doctree of the index document.
    """
    app = request.getfuncargvalue('app')
    doctree = app.env.get_and_resolve_doctree('index', app.builder)
    return doctree


FILENAME_TEST_CASES = {
    'class': {
        'Hello': 'Hello-class.html',
        'world.Hello': 'world.Hello-class.html'},
    'module': {
        'hello': 'hello-module.html',
        'hello.world': 'hello.world-module.html'},
    'function': {
        'hello.world': 'hello-module.html#world',
        'hello.world.say': 'hello.world-module.html#say'},
    'method': {
        'hello.world': 'hello-class.html#world',
        'hello.world.say': 'hello.world-class.html#say'}
}


for left, right in [('exception', 'class'), ('data', 'function'),
                    ('attribute', 'method'), ('staticmethod', 'method'),
                    ('classmethod', 'method')]:
    FILENAME_TEST_CASES[left] = FILENAME_TEST_CASES[right]


def pytest_generate_tests(metafunc):
    if metafunc.function == test_filename_for_object:
        for objtype, testcases in FILENAME_TEST_CASES.iteritems():
            for name, expected in testcases.iteritems():
                args = dict(objtype=objtype, name=name,
                            expected=expected)
                testid = '%s "%s"' % (objtype, name)
                metafunc.addcall(funcargs=args, id=testid)


def test_filename_for_object(objtype, name, expected):
    from sphinxcontrib.epydoc import filename_for_object
    assert filename_for_object(objtype, name) == expected


# marker shortcuts
with_content = pytest.mark.with_content
confoverrides = pytest.mark.confoverrides


@confoverrides(primary_domain='c')
@with_content(':func:`eggs.foobar`')
def test_no_py_domain(doctree):
    """
    Test that no reference is created for references outside the py domain.
    """
    assert not doctree.traverse(nodes.reference)


@with_content(':func:`urllib.urlopen`')
def test_no_pattern_matches(doctree):
    """
    Test that no reference is created if no epydoc mapping pattern matches.
    """
    assert not doctree.traverse(nodes.reference)


@with_content(':func:`eggs.foo` and :func:`spam.foo` and :func:`chicken.foo`')
def test_all_patterns_considered(doctree):
    """
    Test that all patterns are tried in order to find epydoc references.
    """
    assert len(doctree.traverse(nodes.reference)) == 3


def assert_reference(doctree, title, url):
    __tracebackhide__ = True
    assert len(doctree.traverse(nodes.reference)) == 1
    reference = doctree.next_node(nodes.reference)
    assert reference
    assert reference['refuri'] == url
    assert reference.astext() == title


@with_content(':mod:`eggs`')
def test_toplevel_module_reference(doctree):
    assert_reference(doctree, 'eggs', 'http://eggs/eggs-module.html')


@with_content(':mod:`eggs.spam`')
def test_nested_module_reference(doctree):
    assert_reference(doctree, 'eggs.spam', 'http://eggs/eggs.spam-module.html')


@with_content(':func:`eggs.spam`')
def test_function_reference(doctree):
    assert_reference(doctree, 'eggs.spam()', 'http://eggs/eggs-module.html#spam')


@with_content(':data:`eggs.SPAM`')
def test_data_reference(doctree):
    assert_reference(doctree, 'eggs.SPAM', 'http://eggs/eggs-module.html#SPAM')


@with_content(':class:`eggs.Eggs`')
def test_class_reference(doctree):
    assert_reference(doctree, 'eggs.Eggs', 'http://eggs/eggs.Eggs-class.html')


@with_content(':exc:`eggs.Eggs`')
def test_exception_reference(doctree):
    assert_reference(doctree, 'eggs.Eggs', 'http://eggs/eggs.Eggs-class.html')


@with_content(':meth:`eggs.Eggs.spam`')
def test_method_reference(doctree):
    assert_reference(doctree, 'eggs.Eggs.spam()',
                     'http://eggs/eggs.Eggs-class.html#spam')


@with_content(':attr:`eggs.Eggs.spam`')
def test_attribute_reference(doctree):
    assert_reference(doctree, 'eggs.Eggs.spam',
                     'http://eggs/eggs.Eggs-class.html#spam')


@with_content(':func:`Reference to foo <eggs.foo>`')
def test_with_explicit_title(doctree):
    assert_reference(doctree, 'Reference to foo',
                     'http://eggs/eggs-module.html#foo')


def main():
    pytest.cmdline.main()


if __name__ == '__main__':
    main()
