#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docutils import nodes
from mock import Mock

from sphinxcontrib import ansi


RAWSOURCE = '''\
\x1b[1mfoo\x1b[33;1mbar\x1b[1;34mhello\x1b[0mworld\x1b[1m'''


def pytest_funcarg__paragraph(request):
    paragraph = nodes.paragraph()
    paragraph.append(ansi.ansi_literal_block(RAWSOURCE, RAWSOURCE))
    return paragraph


def pytest_funcarg__app(request):
    return Mock()


def pytest_funcarg__parser(request):
    return ansi.ANSIColorParser()


def _assert_colors(node, *colors):
    assert isinstance(node, nodes.inline)
    for color in colors:
        assert ('ansi-%s' % color) in node['classes']


def _assert_text(node, text):
    assert isinstance(node, nodes.Text)
    assert node.astext() == text


def test_parser_strip_colors(app, parser, paragraph):
    app.builder.name = 'foo'
    parser(app, paragraph, 'foo')
    assert isinstance(paragraph[0], nodes.literal_block)
    _assert_text(paragraph[0][0], 'foobarhelloworld')
    assert not paragraph[0][0].children
    assert paragraph.astext() == 'foobarhelloworld'


def test_parser_colors_parsed(app, parser, paragraph):
    app.builder.name = 'html'
    parser(app, paragraph, 'foo')
    block = paragraph[0]
    assert isinstance(block, nodes.literal_block)
    _assert_colors(block[0], 'bold')
    _assert_text(block[0][0], 'foo')
    _assert_colors(block[1], 'bold', 'yellow')
    _assert_text(block[1][0], 'bar')
    _assert_colors(block[2], 'bold', 'blue')
    _assert_text(block[2][0], 'hello')
    _assert_text(block[3], 'world')
    _assert_colors(block[4], 'bold')
    assert not block[4].children
    assert paragraph.astext() == 'foobarhelloworld'


def test_setup(app):
    ansi.setup(app)
    app.require_sphinx.assert_called_with('1.0')
    app.add_config_value.assert_called_with(
        'html_ansi_stylesheet', None, 'env')
    app.add_directive.assert_called_with(
        'ansi-block', ansi.ANSIBlockDirective)
    assert app.connect.call_args_list[:2] == [
        (('builder-inited', ansi.add_stylesheet),),
        (('build-finished', ansi.copy_stylesheet),)]
    assert app.connect.call_args_list[2][0][0] == 'doctree-resolved'
    assert isinstance(app.connect.call_args_list[2][0][1],
                      ansi.ANSIColorParser)


def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
