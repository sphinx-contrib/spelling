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

import pytest

from sphinxcontrib import issuetracker


def test_builtin_issue_trackers():
    for tracker in ('github', 'bitbucket',
                    'launchpad', 'google code', 'debian'):
        assert tracker in issuetracker.BUILTIN_ISSUE_TRACKERS


def test_auto_connect_builtin_issue_resolvers_known_tracker(app):
    app.config.issuetracker = 'bitbucket'
    issuetracker.auto_connect_builtin_issue_resolvers(app)
    app.connect.assert_called_with(
        'issuetracker-resolve-issue',
        issuetracker.get_bitbucket_issue_information)


def test_auto_connect_builtin_issue_resolvers_unknown_tracker(app):
    app.config.issuetracker = 'spamtracker'
    with pytest.raises(KeyError):
        issuetracker.auto_connect_builtin_issue_resolvers(app)


def test_auto_connect_builtin_issue_resolvers_no_tracker(app):
    app.config.issuetracker = None
    issuetracker.auto_connect_builtin_issue_resolvers(app)
    assert not app.connect.called


def test_add_stylesheet(app):
    issuetracker.add_stylesheet(app)
    app.add_stylesheet.assert_called_with('issuetracker.css')


def test_setup(app):
    issuetracker.setup(app)
    app.require_sphinx.assert_called_with('1.0')
    app.add_transform.assert_called_with(issuetracker.IssuesReferences)
    app.add_event.assert_called_with('issuetracker-resolve-issue')
    assert app.connect.call_args_list == [
        (('builder-inited',
          issuetracker.auto_connect_builtin_issue_resolvers), {}),
        (('builder-inited', issuetracker.add_stylesheet), {}),
        (('builder-inited', issuetracker.init_cache), {}),
        (('doctree-read', issuetracker.resolve_issue_references), {}),
        (('build-finished', issuetracker.copy_stylesheet), {})]
    assert app.add_config_value.call_args_list == [
        (('issuetracker_issue_pattern', re.compile(r'#(\d+)'), 'env'), {}),
        (('issuetracker_project', None, 'env'), {}),
        (('issuetracker', None, 'env'), {})]
