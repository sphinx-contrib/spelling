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

"""
    test_resolval
    =============

    Test resolval of pending issue references.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import pytest

from sphinxcontrib.issuetracker import TrackerConfig, Issue


def pytest_funcarg__app(request):
    """
    Adds the ``mock_lookup`` marker to the current test before creating the
    ``app``.
    """
    request.applymarker(pytest.mark.mock_lookup)
    return request.getfuncargvalue('app')


@pytest.mark.with_content('#10')
def test_no_issue(app, resolved_doctree):
    """
    Test that no reference is created if an issue could not be resolved.
    """
    assert not resolved_doctree.is_('reference')


@pytest.mark.with_issue(id='10', title='Spam', url='spam', closed=False)
def test_open_issue(app, resolved_doctree, issue):
    """
    Test resolval of an open issue.
    """
    assert app.env.issuetracker_cache == {'10': issue}
    pytest.assert_issue_xref(resolved_doctree, issue, '#10')


@pytest.mark.with_issue(id='10', title='Eggs', url='eggs', closed=True)
def test_closed_issue(app, resolved_doctree, issue):
    """
    Test resolval of a closed issue.
    """
    pytest.assert_issue_xref(resolved_doctree, issue, '#10')


@pytest.mark.with_issue(id='10', title=None, url='eggs', closed=True)
def test_issue_without_title(app, resolved_doctree, issue):
    """
    Test resolval of issues without title.
    """
    pytest.assert_issue_xref(resolved_doctree, issue, '#10')


@pytest.mark.with_issue(id='10', title='Eggs', url='eggs', closed=True)
@pytest.mark.with_content(':issue:`{issue.title} (#{issue.id})<10>`')
def test_with_formatted_title(resolved_doctree, issue):
    """
    Test issue with format in title.
    """
    pytest.assert_issue_xref(resolved_doctree, issue, 'Eggs (#10)')


@pytest.mark.with_issue(id='10', title=None, url='eggs', closed=True)
@pytest.mark.with_content(':issue:`{{issue.title}} (#{issue.id}) <10>`')
def test_with_escaped_formatted_title(resolved_doctree, issue):
    """
    Test issue with escaped formats in title.
    """
    pytest.assert_issue_xref(resolved_doctree, issue, '{issue.title} (#10)')


@pytest.mark.with_issue(id='10', title='öäüß', url='eggs', closed=True)
@pytest.mark.with_content(':issue:`{issue.title} <10>`')
def test_non_ascii_title(resolved_doctree, issue):
    """
    Test issues with non-ascii titles.
    """
    pytest.assert_issue_xref(resolved_doctree, issue, 'öäüß')
    assert resolved_doctree.text() == 'öäüß'
