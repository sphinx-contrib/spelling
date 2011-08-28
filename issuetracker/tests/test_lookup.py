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
    test_lookup
    ===========

    Test issue lookup.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import pytest

from sphinxcontrib.issuetracker import TrackerConfig


def pytest_funcarg__app(request):
    """
    Adds the ``mock_lookup`` and ``build_app`` markers to the current test
    before creating the ``app``.
    """
    request.applymarker(pytest.mark.mock_lookup)
    request.applymarker(pytest.mark.build_app)
    return request.getfuncargvalue('app')


@pytest.mark.with_content('#10')
@pytest.mark.with_issue(id='10', title='Eggs', closed=False, url='eggs')
def test_lookup_existing_issue(cache, issue):
    """
    Test resolval of an existing issue.
    """
    assert cache == {'10': issue}


@pytest.mark.with_content('#10')
def test_lookup_missing_issue(cache):
    """
    Test resolval of a missing issue.
    """
    assert cache == {'10': None}


@pytest.mark.build_app
@pytest.mark.with_content('#10')
def test_event_emitted(app, mock_lookup):
    """
    Test that issue resolval emits the event with the right arguments.
    """
    assert mock_lookup.call_count == 1
    mock_lookup.assert_called_with(
        app, TrackerConfig.from_sphinx_config(app.config), '10')


@pytest.mark.build_app
@pytest.mark.with_content('#10 #10 #11 #11')
@pytest.mark.with_issue(id='10', title='Eggs', closed=True, url='eggs')
def test_event_emitted_only_once(app, mock_lookup, issue):
    """
    Test that the resolval event is only emitted once for each issue id, and
    that subsequent lookups hit the cache.
    """
    assert mock_lookup.call_count == 2
    assert app.env.issuetracker_cache == {'10': issue, '11': None}
