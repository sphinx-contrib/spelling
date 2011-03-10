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
    sphinxcontrib.issuetracker
    ==========================

    Integration with isse trackers.

    Replace textual issue references (like #1) with a real reference to the
    corresponding issue on bitbucket.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

__version__ = '0.7.2'

import re
import urllib
from contextlib import closing
from os import path

from docutils import nodes
from docutils.transforms import Transform
from sphinx.addnodes import pending_xref
from sphinx.util.osutil import copyfile
from sphinx.util.console import bold


GITHUB_URL = 'https://github.com/%(user)s/%(project)s/issues/%(issue_id)s'
BITBUCKET_URL = ('https://bitbucket.org/%(user)s/%(project)s/issue/'
                 '%(issue_id)s/')


def get_github_issue_information(app, project, user, issue_id):
    try:
        import json
    except ImportError:
        import simplejson as json

    show_issue = ('https://github.com/api/v2/json/issues/show/'
                  '%(user)s/%(project)s/%(issue_id)s' % locals())

    with closing(urllib.urlopen(show_issue)) as response:
        response = json.load(response)
    if 'error' in response:
        return None

    return {'closed': response['issue']['state'] == 'closed',
            'uri': GITHUB_URL % locals()}


def get_bitbucket_issue_information(app, project, user, issue_id):
    from lxml.html import parse

    uri = BITBUCKET_URL % locals()
    with closing(urllib.urlopen(uri)) as response:
        if response.getcode() == 404:
            return None
        elif response.getcode() != 200:
            # warn about unexpected response code
            app.warn('issue %s unavailable with code %s' %
                     (issue_id, response.getcode()))
            return None
        tree = parse(response)
    info = tree.getroot().cssselect('.issues-issue-infotable')[0]
    is_new = info.cssselect('.issue-status-new')
    is_open = info.cssselect('.issue-status-open')
    return {'uri': uri, 'closed': not (is_open or is_new)}


def get_debian_issue_information(app, project, user, issue_id):
    import debianbts
    try:
        # get the bug
        bug = debianbts.get_status(debianbts.get_bugs("bugs", issue_id))[0]
    except IndexError:
        return None

    # check if issue matches project
    if project not in [bug.package, bug.source]:
        return None

    uri = 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=%s' % issue_id
    return {'uri': uri, 'closed': bug.done}


def get_launchpad_issue_information(app, project, user, issue_id):
    launchpad = getattr(app.env, 'issuetracker_launchpad', None)
    if not launchpad:
        from launchpadlib.launchpad import Launchpad
        launchpad = Launchpad.login_anonymously(
            'sphinxcontrib.issuetracker', service_root='production')
        app.env.issuetracker_launchpad = launchpad
    try:
        # get the bug
        bug = launchpad.bugs[issue_id]
    except KeyError:
        return None

    for task in bug.bug_tasks:
        if task.bug_target_name == project:
            break
    else:
        # no matching task found
        return None

    uri = 'https://bugs.launchpad.net/bugs/%s' % issue_id
    # if date_closed exists, we consider the bug as closed
    return {'uri': uri, 'closed': bool(task.date_closed)}


def get_google_code_issue_information(app, project, user, issue_id):
    from xml.etree import cElementTree as etree

    show_issue = ('http://code.google.com/feeds/issues/p/'
                  '%(project)s/issues/full/%(issue_id)s' % locals())
    with closing(urllib.urlopen(show_issue)) as response:
        if response.getcode() == 404:
            return None
        elif response.getcode() != 200:
            # warn about unavailable issues
            app.warn('issue %s unavailable with code %s' %
                     (issue_id, response.getcode()))
            return None
        tree = etree.parse(response)

    state = tree.find(
        '{http://schemas.google.com/projecthosting/issues/2009}state')
    uri = ('http://code.google.com/p/%(project)s/issues/'
           'detail?id=%(issue_id)s' % locals())
    return {'uri': uri, 'closed': state is not None and state.text == 'closed'}


BUILTIN_ISSUE_TRACKERS = {
    'github': get_github_issue_information,
    'bitbucket': get_bitbucket_issue_information,
    'debian': get_debian_issue_information,
    'launchpad': get_launchpad_issue_information,
    'google code': get_google_code_issue_information,
    }


class IssuesReferences(Transform):
    """
    Transform plain text issue numbers (e.g. #10) into ``pending_xref``
    nodes, which are then resolved through the sphinx reference resolving
    mechanism.
    """

    default_priority = 999

    def apply(self):
        config = self.document.settings.env.config
        issue_pattern = config.issuetracker_issue_pattern
        if isinstance(issue_pattern, basestring):
            issue_pattern = re.compile(issue_pattern)
        for node in self.document.traverse(nodes.Text):
            parent = node.parent
            if isinstance(parent, (nodes.literal, nodes.FixedTextElement)):
                # ignore inline and block literal text
                continue
            text = unicode(node)
            new_nodes = []
            last_issue_ref_end = 0
            for match in issue_pattern.finditer(text):
                # catch invalid pattern with too many groups
                if len(match.groups()) != 1:
                    raise ValueError(
                        'issuetracker_issue_pattern must have '
                        'exactly one group: %r' % (match.groups(),))
                # extract the text between the last issue reference and the
                # current issue reference and put it into a new text node
                head = text[last_issue_ref_end:match.start()]
                if head:
                    new_nodes.append(nodes.Text(head))
                # adjust the position of the last issue reference in the
                # text
                last_issue_ref_end = match.end()
                # extract the issue text (including the leading dash)
                issuetext = match.group(0)
                # extract the issue number (excluding the leading dash)
                issue_id = match.group(1)
                # turn the issue reference into a reference node
                refnode = pending_xref()
                refnode['reftarget'] = issue_id
                refnode['reftype'] = 'issue'
                refnode.append(nodes.Text(issuetext))
                new_nodes.append(refnode)
            if not new_nodes:
                # no issue references were found, move on to the next node
                continue
            # extract the remaining text after the last issue reference, and
            # put it into a text node
            tail = text[last_issue_ref_end:]
            if tail:
                new_nodes.append(nodes.Text(tail))
            # find and remove the original node, and insert all new nodes
            # instead
            parent.replace(node, new_nodes)


def make_issue_reference(issue_uri, content_node, is_closed=False):
    """
    Create a reference node for the given issue.

    ``issue_uri`` is the uri of a web page describing the issue.  It must *not*
    be a resource uri for a webservice of an issue tracker.  ``content_node``
    is a docutils node, which is added as content of the created reference.  If
    ``is_closed`` is ``True``, the issue is considered as closed, and the
    reference node gets an additional class ``'issue-closed'``.

    Return a :class:`docutils.nodes.reference` for the issue.
    """
    reference = nodes.reference()
    reference['refuri'] = issue_uri
    if is_closed:
        reference['classes'].append('issue-closed')
    reference['classes'].append('reference-issue')
    reference.append(content_node)
    return reference


def lookup_issue_information(issue_id, app):
    """
    Lookup information for the given issue.

    The issue information is first searched in an internal cache.  On cache
    miss, ``fallback_func`` is called to retrieve the issue information from
    the issue tracker.  This information is than cached.

    ``app`` is the sphinx application object.  ``issue_id`` is a string
    containing the issue id.
    """
    cache = app.env.issuetracker_cache
    info = cache.get(issue_id)
    if not info:
        project = app.config.issuetracker_project or app.config.project
        user = app.config.issuetracker_user
        info = app.emit_firstresult(
            'issuetracker-resolve-issue', project, user, issue_id)
        cache[issue_id] = info
    return info


def resolve_issue_references(app, doctree):
    """
    Resolve all pending issue references in the given ``doctree``.
    """
    for node in doctree.traverse(pending_xref):
        if node['reftype'] == 'issue':
            info = lookup_issue_information(node['reftarget'], app)
            if (not info) or 'uri' not in info:
                new_node = node[0]
            else:
                new_node = make_issue_reference(info['uri'], node[0],
                                                info.get('closed'))
            node.replace_self(new_node)


def auto_connect_builtin_issue_resolvers(app):
    if app.config.issuetracker:
        app.connect('issuetracker-resolve-issue',
                    BUILTIN_ISSUE_TRACKERS[app.config.issuetracker.lower()])


def add_stylesheet(app):
    app.add_stylesheet('issuetracker.css')


def init_cache(app):
    if not hasattr(app.env, 'issuetracker_cache'):
        app.env.issuetracker_cache = {}


def copy_stylesheet(app, exception):
    if app.builder.name != 'html' or exception:
        return
    app.info(bold('Copying issuetracker stylesheet... '), nonl=True)
    dest = path.join(app.builder.outdir, '_static', 'issuetracker.css')
    source = path.join(path.abspath(path.dirname(__file__)),
                          'issuetracker.css')
    copyfile(source, dest)
    app.info('done')


def setup(app):
    app.require_sphinx('1.0')
    app.add_transform(IssuesReferences)
    app.add_event('issuetracker-resolve-issue')
    app.connect('builder-inited', auto_connect_builtin_issue_resolvers)
    app.add_config_value('issuetracker_issue_pattern',
                         re.compile(r'#(\d+)'), 'env')
    app.add_config_value('issuetracker_user', None, 'env')
    app.add_config_value('issuetracker_project', None, 'env')
    app.add_config_value('issuetracker', None, 'env')
    app.connect('builder-inited', add_stylesheet)
    app.connect('builder-inited', init_cache)
    app.connect('doctree-read', resolve_issue_references)
    app.connect('build-finished', copy_stylesheet)
