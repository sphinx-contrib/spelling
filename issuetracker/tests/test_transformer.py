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


import pytest
from mock import Mock
from docutils import nodes

from sphinx.addnodes import pending_xref
from sphinxcontrib import issuetracker


def assert_text(node, text):
    assert isinstance(node, nodes.Text)
    assert node.astext() == text


def assert_xref(node, target):
    assert isinstance(node, pending_xref)
    assert_text(node[0], '#%s' % target)
    assert node['reftype'] == 'issue'
    assert node['reftarget'] == target


def pytest_funcarg__env(request):
    env = Mock(name='environment')
    env.config = request.getfuncargvalue('config')
    return env


def pytest_funcarg__doc(request):
    doc = nodes.paragraph()
    para = nodes.paragraph()
    para.append(nodes.Text('Transformed #1 inside a normal paragraph'))
    para.append(nodes.Text('Not transformed #abc inside a normal paragraph'))
    doc.append(para)
    em = nodes.emphasis()
    em.append(nodes.Text('Transformed #2 inside emphasis'))
    doc.append(em)
    lit = nodes.literal()
    lit.append(nodes.Text('Not transformed #3 inside inline literal'))
    doc.append(lit)
    litblock = nodes.literal_block()
    litblock.append(nodes.Text('Not transformed #4 inside literal block'))
    doc.append(litblock)
    doc.settings = Mock(name='settings')
    doc.settings.language_code = ''
    doc.settings.env = request.getfuncargvalue('env')
    return doc


def test_issues_references(doc):
    transformer = issuetracker.IssuesReferences(doc)
    transformer.apply()
    assert isinstance(doc, nodes.paragraph)
    assert doc.astext() == ('Transformed #1 inside a normal paragraph'
                            'Not transformed #abc inside a normal paragraph'
                            'Transformed #2 inside emphasis'
                            'Not transformed #3 inside inline literal'
                            'Not transformed #4 inside literal block')

    para = doc[0]
    assert isinstance(para, nodes.paragraph)
    assert_text(para[0], 'Transformed ')
    assert_xref(para[1], '1')
    assert_text(para[2], ' inside a normal paragraph')
    assert_text(para[3], 'Not transformed #abc inside a normal paragraph')
    em = doc[1]
    assert isinstance(em, nodes.emphasis)
    assert_text(em[0], 'Transformed ')
    assert_xref(em[1], '2')
    assert_text(em[2], ' inside emphasis')
    lit = doc[2]
    assert isinstance(lit, nodes.literal)
    assert_text(lit[0], 'Not transformed #3 inside inline literal')
    litblock = doc[3]
    assert isinstance(litblock, nodes.literal_block)
    assert_text(litblock[0], 'Not transformed #4 inside literal block')


def test_issues_references_too_many_groups(doc, config):
    config.issuetracker_issue_pattern = r'(#)(\d+)'
    transformer = issuetracker.IssuesReferences(doc)
    with pytest.raises(ValueError) as exc_info:
        transformer.apply()
    error = exc_info.value
    assert str(error) == ('issuetracker_issue_pattern must have '
                          'exactly one group: %r' % ((u'#', u'1'),))
