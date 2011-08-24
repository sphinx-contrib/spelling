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

from sphinxcontrib.issuetracker import TrackerConfig


def pytest_funcarg__content(request):
    # dummy content
    return 'dummy content'


def test_tracker_config_only_project():
    tracker_config = TrackerConfig('eggs')
    assert tracker_config.project == 'eggs'


def test_tracker_config_project_and_url():
    tracker_config = TrackerConfig('eggs', 'http://example.com')
    assert tracker_config.project == 'eggs'
    assert tracker_config.url == 'http://example.com'


def test_tracker_config_trailing_slash():
    tracker_config = TrackerConfig('eggs', 'http://example.com/')
    assert tracker_config.url == 'http://example.com'


def test_tracker_config_equality():
    c = TrackerConfig
    assert c('eggs') == c('eggs')
    assert c('eggs') != c('spam')
    assert c('eggs') != c('eggs', 'spam')
    assert c('eggs', 'spam') == c('eggs', 'spam')
    assert c('eggs', 'spam') != c('eggs', 'foo')
    assert c('eggs', 'spam') != c('spam', 'spam')


@pytest.mark.confoverrides(
    project='eggs', issuetracker_url='http://example.com')
def test_tracker_config_from_sphinx_config(app):
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == 'eggs'
    assert tracker_config.url == 'http://example.com'


@pytest.mark.confoverrides(project='eggs', issuetracker_project='spam',
                           issuetracker_url='http://example.com')
def test_tracker_config_from_sphinx_config_with_project(app):
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == 'spam'
    assert tracker_config.url == 'http://example.com'


@pytest.mark.confoverrides(
    project='eggs', issuetracker_url='http://example.com/')
def test_tracker_config_from_sphinx_config_trailing_slash(app):
    tracker_config = TrackerConfig.from_sphinx_config(app.config)
    assert tracker_config.project == 'eggs'
    assert tracker_config.url == 'http://example.com'
