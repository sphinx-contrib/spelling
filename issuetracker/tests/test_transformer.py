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
from mock import Mock
from docutils import nodes
from docutils.utils import Reporter

from sphinx.addnodes import pending_xref
from sphinxcontrib import issuetracker


def assert_text(node, text):
    __tracebackhide__ = True
    assert isinstance(node, nodes.Text)
    assert node.astext() == text


def assert_xref(node, target):
    __tracebackhide__ = True
    assert isinstance(node, pending_xref)
    assert_text(node[0], '#{0}'.format(target))
    assert node['reftype'] == 'issue'
    assert node['trackerconfig'] == issuetracker.TrackerConfig('issuetracker')
    assert node['reftarget'] == target


def pytest_funcarg__env(request):
    env = Mock(name='environment')
    env.config = request.getfuncargvalue('config')
    return env


def pytest_funcarg__doc(request):
    doc = nodes.paragraph()
    doc.settings = Mock(name='settings')
    doc.settings.language_code = ''
    doc.settings.env = request.getfuncargvalue('env')
    doc.reporter = Reporter('face_source', 0, 0)
    return doc


class TestIssueReferences(object):

    def transform(self, doc):
        transformer = issuetracker.IssuesReferences(doc)
        transformer.apply()

    def test_reference_in_paragraph(self, doc):
        doc.append(nodes.Text('Transformed #1 inside a normal paragraph'))
        self.transform(doc)
        assert_text(doc[0], 'Transformed ')
        assert_xref(doc[1], '1')
        assert_text(doc[2], ' inside a normal paragraph')

    def test_reference_in_emphasis(self, doc):
        em = nodes.emphasis()
        em.append(nodes.Text('Transformed #2 inside emphasis'))
        doc.append(em)
        self.transform(doc)
        assert_text(em[0], 'Transformed ')
        assert_xref(em[1], '2')
        assert_text(em[2], ' inside emphasis')

    def test_reference_in_literal(self, doc):
        lit = nodes.literal()
        text = 'Not transformed #3 inside inline literal'
        lit.append(nodes.Text(text))
        doc.append(lit)
        self.transform(doc)
        assert_text(lit[0], text)

    def test_reference_in_literal_block(self, doc):
        block = nodes.literal_block()
        text = 'Not transformed #4 inside literal block'
        block.append(nodes.Text(text))
        doc.append(block)
        self.transform(doc)
        assert_text(block[0], text)

    def test_invalid_reference(self, doc):
        text = 'Not transformed #abc inside a normal paragraph'
        doc.append(nodes.Text(text))
        self.transform(doc)
        assert_text(doc[0], text)

    def test_too_many_groups(self, doc, config):
        doc.append(nodes.Text('example reference #1'))
        config.issuetracker_issue_pattern = r'(#)(\d+)'
        transformer = issuetracker.IssuesReferences(doc)
        with pytest.raises(ValueError) as exc_info:
            transformer.apply()
        error = exc_info.value
        assert str(error) == ('issuetracker_issue_pattern must have '
                              'exactly one group: {0!r}'.format((u'#', u'1')))
