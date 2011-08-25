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

import re


BUILTIN_TRACKER_NAME_PATTERN = re.compile('lookup_(.*)_issue')

import pytest
from sphinx.environment import SphinxStandaloneReader

from sphinxcontrib import issuetracker


def pytest_funcarg__content(request):
    """
    Dummy content for this test module, overrides the global ``content``
    funcarg.

    This test module doesn't need issue references, but just a loaded and
    ready-to-build sphinx application.  Thus the content doesn't matter, but
    still a sphinx application needs some content to build.
    """
    return 'dummy content'


def test_builtin_issue_trackers():
    """
    Test that all builtin issue trackers are really declared in the
    BUILTIN_ISSUE_TRACKERS dict.
    """
    trackers = dict(issuetracker.BUILTIN_ISSUE_TRACKERS)
    for attr in dir(issuetracker):
        match = BUILTIN_TRACKER_NAME_PATTERN.match(attr)
        if match:
            tracker_name = match.group(1).replace('_', ' ')
            assert tracker_name in trackers
            trackers.pop(tracker_name)
    assert not trackers


def test_unknown_tracker(app):
    """
    Test that setting ``issuetracker`` to an unknown tracker fails.
    """
    app.config.issuetracker = 'spamtracker'
    with pytest.raises(KeyError):
        issuetracker.connect_builtin_tracker(app)


def test_add_stylesheet(app):
    """
    Test that the stylesheet is properly added.
    """
    from sphinx.builders.html import StandaloneHTMLBuilder
    assert '_static/issuetracker.css' in StandaloneHTMLBuilder.css_files


def test_transform_added(app):
    """
    Test that the transformer is properly added.
    """
    assert issuetracker.IssuesReferences in SphinxStandaloneReader.transforms


@pytest.mark.confoverrides(issuetracker_plaintext_issues=False)
def test_transform_not_added(app):
    """
    Test that the transformer is not added if transformations are disabled.
    """
    assert issuetracker.IssuesReferences not in SphinxStandaloneReader.transforms
