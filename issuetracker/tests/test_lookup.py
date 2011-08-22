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

from functools import partial

import mock

from sphinxcontrib.issuetracker import lookup_issue


def pytest_funcarg__issue_id(request):
    return '10'


def pytest_funcarg__issue_info(request):
    return mock.sentinel.issue_info


def pytest_funcarg__lookup(request):
    app = request.getfuncargvalue('app')
    issue_id = request.getfuncargvalue('issue_id')
    return partial(lookup_issue, issue_id, app)


def test_lookup_cache_miss(app, lookup, cache, issue_id, issue_info):
    app.emit_firstresult.return_value = issue_info
    assert lookup() is issue_info
    cache.get.assert_called_with(issue_id)
    cache.__setitem__.assert_called_with(issue_id, issue_info)
    app.emit_firstresult.assert_called_with(
        'issuetracker-resolve-issue', app.config.project, issue_id)


def test_lookup_cache_hit(app, lookup, cache, issue_id, issue_info):
    cache.get.return_value = issue_info
    assert lookup() is issue_info
    cache.get.assert_called_with(issue_id)
    assert not cache.__setitem__.called
    assert not app.emit_firstresult.called
