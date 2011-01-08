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

import re

from mock import Mock, MagicMock


def pytest_funcarg__config(request):
    config = Mock(name='config')
    config.project = 'issuetracker'
    config.issuetracker = 'spamtracker'
    config.issuetracker_user = 'foobar'
    config.issuetracker_project = None
    config.issuetracker_issue_pattern = re.compile(r'#(\d+)')
    return config


def pytest_funcarg__cache(request):
    cache = MagicMock(name='issue_cache')
    # fake cache misses to always trigger a call to the fallback function
    cache.get = Mock(name='issue_cache.get', return_value=None)
    return cache


def pytest_funcarg__app(request):
    app = Mock(name='application')
    config = request.getfuncargvalue('config')
    app.config = config
    app.env = Mock('environment')
    app.env.config = config
    app.env.issuetracker_cache = request.getfuncargvalue('cache')
    return app
