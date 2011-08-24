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

from sphinxcontrib.issuetracker import Issue


def pytest_funcarg__issue(request):
    """
    A dummy issue, just to trigger issue resolval so that transformations can
    be seen in the output.
    """
    return Issue(id='10', title='Eggs', closed=False, url='eggs')


def pytest_funcarg__app(request):
    """
    Adds the ``mock_resolver`` marker to the current test before creating the
    ``app``.
    """
    request.applymarker(pytest.mark.mock_resolver)
    return request.getfuncargvalue('app')


@pytest.mark.with_content('#10')
def test_transform_simple(doctree):
    """
    Test a simple transform with just an issue id.
    """
    assert doctree.is_('reference')


@pytest.mark.with_content('before #10 after')
def test_transform_leading_and_trailing_text(doctree, content):
    """
    Test that transformation leaves leading and trailing text intact.
    """
    assert doctree.is_('reference')
    assert doctree.text() == content


@pytest.mark.with_content('*#10* **#10**')
def test_transform_inline_markup(doctree):
    """
    Test that issue ids inside inline markup like emphasis are transformed.
    """
    assert len(doctree.find('reference')) == 2
    assert doctree.text() == '#10 #10'
    assert doctree.find('reference').eq(0).parents('emphasis')
    assert doctree.find('reference').eq(1).parents('strong')


@pytest.mark.with_content('``#10``')
def test_transform_literal(doctree):
    """
    Test that transformation leaves literals untouched.
    """
    assert not doctree.is_('reference')
    literal = doctree.find('literal')
    assert literal
    assert literal.text() == '#10'


@pytest.mark.with_content("""\
spam::

   eggs
      #10""")
def test_transform_literal_block(doctree):
    """
    Test that transformation leaves literal blocks untouched.
    """
    assert not doctree.is_('reference')
    literal_block = doctree.find('literal_block')
    assert literal_block
    assert literal_block.text('eggs\n   #10')


@pytest.mark.with_content("""\
.. code-block:: python

   eggs('#10')""")
def test_transform_code_block(doctree, content):
    assert not doctree.is_('reference')
    literal_block = doctree.find('literal_block')
    assert literal_block
    assert literal_block.text("eggs('#10')")
    assert literal_block.attr.language == 'python'


@pytest.mark.with_content('ab')
@pytest.mark.confoverrides(issuetracker_issue_pattern=r'(a)(b)')
def test_too_many_groups(app):
    """
    Test that using an issue pattern with too many groups fails with an
    understandable error message.
    """
    with pytest.raises(ValueError) as excinfo:
        app.build()
    error = excinfo.value
    assert str(error) == ('issuetracker_issue_pattern must have '
                          'exactly one group: {0!r}'.format((u'a', u'b')))
