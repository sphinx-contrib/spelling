# -*- coding: utf-8 -*-

import codecs
from re import MULTILINE, DOTALL
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
    oneplus, forward_decl, NoParseError)

try:
    from collections import namedtuple
except:
    def namedtuple(name, fields):
        'Only space-delimited fields are supported.'
        def prop(i, name):
            return (name, property(lambda self: self[i]))
        methods = dict(prop(i, f) for i, f in enumerate(fields.split(' ')))
        methods.update({
            '__new__': lambda cls, *args: tuple.__new__(cls, args),
            '__repr__': lambda self: '%s(%s)' % (
                name,
                ', '.join('%s=%r' % (
                    f, getattr(self, f)) for f in fields.split(' ')))})
        return type(name, (tuple,), methods)


ENCODING = 'utf-8'

Chart = namedtuple('Chart', 'type id stmts')
Node = namedtuple('Node', 'id attrs')
Attr = namedtuple('Attr', 'name value')
DefAttrs = namedtuple('DefAttrs', 'object attrs')


class ParseException(Exception):
    pass


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        ('Comment', (r'/\*(.|[\r\n])*?\*/', MULTILINE)),
        ('Comment', (r'//.*',)),
        ('NL',      (r'[\r\n]+',)),
        ('Space',   (r'[ \t\r\n]+',)),
        ('Name',    (ur'[A-Za-z_\u0080-\uffff][A-Za-z_0-9\.\u0080-\uffff]*',)),
        ('Op',      (r'[{}():;,=\[\]]',)),
        ('Color',  (r'[A-Za-z0-9]+',)),
        ('Number',  (r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)',)),
        ('String',  (r'(?P<quote>"|\').*?(?<!\\)(?P=quote)', DOTALL)),
    ]
    useless = ['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def parse(seq):
    'Sequence(Token) -> object'
    unarg = lambda f: lambda args: f(*args)
    tokval = lambda x: x.value
    flatten = lambda list: sum(list, [])
    value_flatten = lambda l: sum([[l[0]]] + list(l[1:]), [])
    n = lambda s: a(Token('Name', s)) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))
    id = some(lambda t:
        t.type in ['Name', 'Number', 'Color', 'String']).named('id') >> tokval
    make_chart_attr = lambda args: DefAttrs(u'chart', [Attr(*args)])

    node_id = id  # + maybe(port)
    pair = (
        op_('(') + id + skip(maybe(op(','))) + id + op_(')')
        >> tuple)
    value = (id | pair)
    value_list = (
        value +
        many(op_(',') + value)
        >> value_flatten)
    a_list = (
        id +
        maybe(op_('=') + id) +
        skip(maybe(op(',')))
        >> unarg(Attr))
    attr_list = (
        many(op_('[') + many(a_list) + op_(']'))
        >> flatten)
    chart_attr = id + (op_('=') | op_(':')) + value_list >> make_chart_attr
    node_stmt = node_id + attr_list >> unarg(Node)

    stmt = (
        chart_attr
        | node_stmt
    )
    stmt_list = many(stmt + skip(maybe(op(';'))))
    chart_type = (
          n('p')   | n('pie')    | n('piechart')
        | n('p3')  | n('pie3d')  | n('piechart_3d')
        | n('lc')  | n('line')   | n('linechart')
        | n('lxy') | n('linechartxy')
        | n('bhs') | n('holizontal_barchart')
        | n('bvs') | n('vertical_barchart')
        | n('bhg') | n('holizontal_bargraph')
        | n('bvg') | n('vertical_bargraph')
        | n('v')   | n('venn')   | n('venndiagram')
        | n('s')   | n('plot')   | n('plotchart')
    )
    chart = (
        chart_type +
        maybe(id) +
        op_('{') +
        stmt_list +
        op_('}')
        >> unarg(Chart))
    dotfile = chart + skip(finished)

    return dotfile.parse(seq)


chart_types = dict(p='p',     pie='p',    piechart='p',
                   p3='p3',   pie3d='p3', piechart_3d='p3',
                   lc='lc',   line='lc',  linechart='lc',
                   lxy='lxy', linechartxy='lxy',
                   bhs='bhs', holizontal_barchart='bhs',
                   bvs='bvs', vertical_barchart='bvs',
                   bhg='bhg', holizontal_bargraph='bhg',
                   bvg='bvg', vertical_bargraph='bvg',
                   v='v',     venn='v',   venndiagram='v',
                   s='s',     plot='s',   plotchart='s',
              )


class _Chart(object):
    def __init__(self, _type):
        self.type = chart_types[_type]
        self._items = {}
        self._order = []

    def set(self, name, value):
        self._items[name] = value

        if "." in name:
            n = name.index(".")
            key = name[0:n]
        else:
            key = name

        if key not in self._order:
            self._order.append(key)

    @property
    def labels(self):
        return self._order

    @property
    def items(self):
        for key in self._order:
            yield self._items[key]

    @property
    def colors(self):
        colors = []
        for key in self._order:
            key += ".color"

            if key in self._items:
                colors.append(self._items[key][0])
            else:
                break

        return colors

    @property
    def axes(self):
        axes = []

        exist = False
        for key in self._order:
            key += ".axis"

            if key in self._items:
                exist = True
                axes.append(self._items[key])

        if not exist:
            axes = []

        return axes

    @property
    def axis_labels(self):
        labels = {}

        for i, key in enumerate(self._order):
            key += ".axis_label"

            if key in self._items:
                labels[i] = self._items[key]

        return labels


def parse_string(code):
    tree = parse(tokenize(code))

    chart = _Chart(tree.type)

    for stmt in tree.stmts:
        if isinstance(stmt, DefAttrs):
            for attr in stmt.attrs:
                chart.set(attr.name, attr.value)

    return chart


def parse_file(path):
    try:
        input = codecs.open(path, 'r', 'utf-8').read()
        return parse_string(input)
    except LexerError, e:
        message = "Got unexpected token at line %d column %d" % e.place
        raise ParseException(message)
    except Exception, e:
        raise ParseException(str(e))
