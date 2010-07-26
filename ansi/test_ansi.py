#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docutils import nodes

from sphinxcontrib import ansi


RAWSOURCE = '''\
\x1b[1mfoo\x1b[33;1mbar\x1b[1;34mhello\x1b[0mworld\x1b[1m'''


def pytest_funcarg__paragraph(request):
    paragraph = nodes.paragraph()
    paragraph.append(ansi.ansi_literal_block(RAWSOURCE, RAWSOURCE))
    return paragraph


def pytest_funcarg__app(request):
    obj = type('obj', (object, ), {})
    app = obj()
    app.builder = obj()
    return app


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


def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
