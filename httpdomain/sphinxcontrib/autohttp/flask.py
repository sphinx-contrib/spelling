"""
    sphinxcontrib.autohttp.flask
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sphinx.ext.autodoc-style HTTP API reference builder (from Flask)
    for sphinxcontrib.httpdomain.

    :copyright: Copyright 2011 by Hong Minhee
    :license: BSD, see LICENSE for details.

"""

import re
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from docutils import nodes
from docutils.statemachine import ViewList

from sphinx.util.compat import Directive
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docstrings import prepare_docstring

from sphinxcontrib import httpdomain


def import_object(import_name):
    module_name, expr = import_name.split(':', 1)
    mod = __import__(module_name)
    mod = reduce(getattr, module_name.split('.')[1:], mod)
    globals = __builtins__
    if not isinstance(globals, dict):
        globals = globals.__dict__
    return eval(expr, globals, mod.__dict__)


def http_directive(method, path, content):
    method = method.lower().strip()
    if isinstance(content, basestring):
        content = content.splitlines()
    yield ''
    yield '.. http:{method}:: {path}'.format(**locals())
    yield ''
    for line in content:
        yield '   ' + line
    yield ''


def translate_werkzeug_rule(rule):
    from werkzeug.routing import parse_rule
    buf = StringIO.StringIO()
    for conv, arg, var in parse_rule(rule):
        if conv:
            buf.write('(')
            if conv != 'default':
                buf.write(conv)
                buf.write(':')
            buf.write(var)
            buf.write(')')
        else:
            buf.write(var)
    return buf.getvalue()


def get_routes(app):
    for rule in app.url_map.iter_rules():
        methods = rule.methods.difference(['OPTIONS', 'HEAD'])
        for method in methods:
            path = translate_werkzeug_rule(rule.rule)
            yield method, path, rule.endpoint


class AutoflaskDirective(Directive):

    has_content = True
    required_arguments = 1
    option_spec = {'undoc-endpoints': str,
                   'undoc-static': str,
                   'include-empty-docstring': str}

    @property
    def undoc_endpoints(self):
        try:
            endpoints = re.split(r'\s*,\s*', self.options['undoc-endpoints'])
        except KeyError:
            return frozenset()
        return frozenset(endpoints)

    def make_rst(self):
        app = import_object(self.arguments[0])
        for method, path, endpoint in get_routes(app):
            if endpoint in self.undoc_endpoints:
                continue
            try:
                static_url_path = app.static_url_path # Flask 0.7 or higher
            except AttributeError:
                static_url_path = app.static_path # Flask 0.6 or under
            if ('undoc-static' in self.options and endpoint == 'static' and
                path == static_url_path + '/(path:filename)'):
                continue
            view = app.view_functions[endpoint]
            docstring = view.__doc__ or ''
            if not docstring and 'include-empty-docstring' not in self.options:
                continue
            docstring = prepare_docstring(docstring)
            for line in http_directive(method, path, docstring):
                yield line

    def run(self):
        node = nodes.section()
        node.document = self.state.document
        result = ViewList()
        for line in self.make_rst():
            result.append(line, '<autoflask>')
        nested_parse_with_titles(self.state, result, node)
        return node.children


def setup(app):
    if 'http' not in app.domains:
        httpdomain.setup(app)
    app.add_directive('autoflask', AutoflaskDirective)

