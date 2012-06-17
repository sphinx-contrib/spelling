# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011, Sebastian Wiesner <lunaryorn@googlemail.com>
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
    sphinxcontrib.issuetracker.resolvers
    ====================================

    Builtin resolvers for :mod:`sphinxcontrib.issuetracker`.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import requests
from xml.etree import ElementTree as etree

from sphinxcontrib.issuetracker import Issue


GITHUB_API_URL = 'https://api.github.com/repos/{0.project}/issues/{1}'
BITBUCKET_URL = 'https://bitbucket.org/{0.project}/issue/{1}/'
BITBUCKET_API_URL = ('https://api.bitbucket.org/1.0/repositories/'
                     '{0.project}/issues/{1}/')
DEBIAN_URL = 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug={0}'
LAUNCHPAD_URL = 'https://bugs.launchpad.net/bugs/{0}'
GOOGLE_CODE_URL = 'http://code.google.com/p/{0.project}/issues/detail?id={1}'
GOOGLE_CODE_API_URL = ('http://code.google.com/feeds/issues/p/'
                       '{0.project}/issues/full/{1}')
# namespaces required to parse XML returned by Google Code
GOOGLE_ISSUE_NS = '{http://schemas.google.com/projecthosting/issues/2009}'
ATOM_NS = '{http://www.w3.org/2005/Atom}'
JIRA_API_URL = ('{0.url}/si/jira.issueviews:issue-xml/{1}/{1}.xml?'
                # only request the required fields
                'field=link&field=resolution&field=summary&field=project')


def check_project_with_username(tracker_config):
    if '/' not in tracker_config.project:
        raise ValueError(
            'username missing in project name: {0.project}'.format(
                tracker_config))


def get(app, url):
    """
    Get a response from the given ``url``.

    ``url`` is a string containing the URL to request via GET. ``app`` is the
    Sphinx application object.

    Return the :class:`~requests.Response` object on status code 200, or
    ``None`` otherwise. If the status code is not 200 or 404, a warning is
    emitted via ``app``.
    """
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response
    elif response.status_code != requests.codes.not_found:
        msg = 'GET {0.url} failed with code {0.status_code}'
        app.warn(msg.format(response))


def lookup_github_issue(app, tracker_config, issue_id):
    check_project_with_username(tracker_config)

    url = GITHUB_API_URL.format(tracker_config, issue_id)
    response = get(app, url)
    if response:
        issue = response.json
        closed = issue['state'] == 'closed'
        return Issue(id=issue_id, title=issue['title'], closed=closed,
                     url=issue['html_url'])


def lookup_bitbucket_issue(app, tracker_config, issue_id):
    check_project_with_username(tracker_config)

    url = BITBUCKET_API_URL.format(tracker_config, issue_id)
    response = get(app, url)
    if response:
        issue = response.json
        closed = issue['status'] not in ('new', 'open')
        url = BITBUCKET_URL.format(tracker_config, issue_id)
        return Issue(id=issue_id, title=issue['title'], closed=closed, url=url)


def lookup_debian_issue(app, tracker_config, issue_id):
    import debianbts
    try:
        # get the bug
        bug = debianbts.get_status(issue_id)[0]
    except IndexError:
        return None

    # check if issue matches project
    if tracker_config.project not in (bug.package, bug.source):
        return None

    return Issue(id=issue_id, title=bug.subject, closed=bug.done,
                 url=DEBIAN_URL.format(issue_id))


def lookup_launchpad_issue(app, tracker_config, issue_id):
    from launchpadlib.launchpad import Launchpad
    launchpad = Launchpad.login_anonymously(
        'sphinxcontrib.issuetracker', service_root='production')
    try:
        # get the bug
        bug = launchpad.bugs[issue_id]
    except KeyError:
        return None

    project_tasks = [task for task in bug.bug_tasks
                     if task.bug_target_name == tracker_config.project]
    if not project_tasks:
        # no matching task found
        return None

    is_complete = all(t.is_complete for t in project_tasks)
    return Issue(id=issue_id, title=bug.title, closed=is_complete,
                 url=LAUNCHPAD_URL.format(issue_id))


def lookup_google_code_issue(app, tracker_config, issue_id):
    url = GOOGLE_CODE_API_URL.format(tracker_config, issue_id)
    response = get(app, url)
    if response:
        issue = etree.fromstring(response.content)
        state = issue.find('{0}state'.format(GOOGLE_ISSUE_NS))
        title_node = issue.find('{0}title'.format(ATOM_NS))
        title = title_node.text if title_node is not None else None
        closed = state is not None and state.text == 'closed'
        return Issue(id=issue_id, title=title, closed=closed,
                     url=GOOGLE_CODE_URL.format(tracker_config, issue_id))


def lookup_jira_issue(app, tracker_config, issue_id):
    if not tracker_config.url:
        raise ValueError('URL required')
    url = JIRA_API_URL.format(tracker_config, issue_id)
    response = get(app, url)
    if response:
        issue = etree.fromstring(response.content)
        project = issue.find('*/item/project').text
        if project != tracker_config.project:
            return None

        url = issue.find('*/item/link').text
        state = issue.find('*/item/resolution').text
        # summary contains the title without the issue id
        title = issue.find('*/item/summary').text
        closed = state.lower() != 'unresolved'
        return Issue(id=issue_id, title=title, closed=closed, url=url)


BUILTIN_ISSUE_TRACKERS = {
    'github': lookup_github_issue,
    'bitbucket': lookup_bitbucket_issue,
    'debian': lookup_debian_issue,
    'launchpad': lookup_launchpad_issue,
    'google code': lookup_google_code_issue,
    'jira': lookup_jira_issue,
    }
