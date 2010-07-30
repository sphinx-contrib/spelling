#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial

from docutils import nodes
from mock import Mock

from sphinxcontrib import epydoc


FILENAME_TEST_DATA = {
    'class': {
        'Hello': 'Hello-class.html',
        'world.Hello': 'world.Hello-class.html',
        },
    'module': {
        'hello': 'hello-module.html',
        'hello.world': 'hello.world-module.html',
        },
    'function': {
        'hello.world': 'hello-module.html#world',
        'hello.world.say': 'hello.world-module.html#say',
        },
    'method': {
        'hello.world': 'hello-class.html#world',
        'hello.world.say': 'hello.world-class.html#say',
        }
    }

for left, right in [('exception', 'class'), ('data', 'function'),
                    ('attr', 'method')]:
    FILENAME_TEST_DATA[left] = FILENAME_TEST_DATA[right]


def pytest_generate_tests(metafunc):
    if metafunc.function == test_filename_for_object:
        for objtype, testcases in FILENAME_TEST_DATA.iteritems():
            for name, expected in testcases.iteritems():
                args = dict(objtype=objtype, name=name,
                            expected=expected)
                id = '%s "%s"' % (objtype, name)
                metafunc.addcall(funcargs=args, id=id)


def pytest_funcarg__app(request):
    app = Mock()
    app.config.epydoc_mapping = {
        'http://example.com/': [r'hello\..*']}
    return app


def pytest_funcarg__env(request):
    env = Mock()
    env.domains = {'py': Mock()}
    return env


def pytest_funcarg__node(request):
    node = nodes.reference(text='foo')
    node['refdomain'] = 'py'
    node['reftype'] = 'method'
    node['reftarget'] = 'hello.World.say'
    return node


def pytest_funcarg__resolve(request):
    app = request.getfuncargvalue('app')
    env = request.getfuncargvalue('env')
    node = request.getfuncargvalue('node')
    return partial(epydoc.resolve_reference_to_epydoc, app, env,
                   node, node[0])


def test_filename_for_object(objtype, name, expected):
    assert epydoc.filename_for_object(objtype, name) == expected


def test_resolve_reference_to_epydoc_invalid_domain(resolve, node):
    node['refdomain'] = 'foo'
    assert resolve() is None

def test_resolve_reference_to_epydoc_not_matching(resolve, node):
    node['reftarget'] = 'foo.bar'
    assert resolve() is None

def test_resolve_reference_to_epydoc_ambiguous_objtype(
    resolve, node, app, env):
    env.domains['py'].objtypes_for_role.return_value = ('foo', 'bar')
    assert resolve() is None
    assert app.warn.called
    app.warn.assert_called_with('ambiguous object types for %s, cannot '
                                'resolve to epydoc' % node['reftarget'])

def test_resolve_reference_to_epydoc_success(resolve, node, env):
    env.domains['py'].objtypes_for_role.return_value = ('method',)
    new_node = resolve()
    uri = 'http://example.com/hello.World-class.html#say'
    assert new_node
    assert new_node['class'] == 'external-xref'
    assert new_node['refuri'] == uri
    assert new_node['reftitle'] == 'Epydoc crossreference'
    assert new_node[0] is node[0]

def test_setup(app):
    epydoc.setup(app)
    app.add_config_value.assert_called_With('epydoc_mapping', {}, 'env')
    app.connect.assert_called_with('missing-reference',
                                   epydoc.resolve_reference_to_epydoc)


def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
