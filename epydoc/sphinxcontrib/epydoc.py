# -*- coding: utf-8 -*-
# Copyright (c) 2010, Sebastian Wiesner <lunaryorn@googlemail.com>
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
    sphinxcontrib.epydoc
    ====================

    Sphinx extension to cross-reference epydoc generated documentation

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import re
import posixpath

from docutils import nodes


def resolve_reference_to_epydoc(app, env, node, contnode):
    """
    Resolve a reference to an epydoc documentation.
    """
    domain = node.get('refdomain')
    if domain != 'py':
        # epydoc only holds Python docs
        return

    target = node['reftarget']
    for baseurl, patterns in app.config.epydoc_mapping.iteritems():
        # find a matching entry in the epydoc mapping
        if any(re.match(p, target) for p in patterns):
            break
    else:
        return

    objtypes = env.domains[domain].objtypes_for_role(node['reftype'])
    objtype = objtypes[0]
    if len(objtypes) > 1:
        app.warn('ambiguous object types for %s, '
                 'cannot resolve to epydoc' % target)
        return

    if objtype == 'exception':
        # exceptions are classes for epydoc
        objtype = 'class'
    if not (objtype == 'module' or objtype == 'class'):
        target, attribute = target.rsplit('.', 1)
        anchor = '#%s' % attribute
        if objtype == 'function' or objtype == 'data':
            objtype = 'module'
        else:
            objtype = 'class'
    else:
        anchor = ''
    filename = '%s-%s.html%s' % (target, objtype, anchor)
    uri = posixpath.join(baseurl, filename)

    newnode = nodes.reference('', '')
    newnode['class'] = 'external-xref'
    newnode['refuri'] = uri
    newnode['reftitle'] = 'Epydoc crossreference'
    newnode.append(contnode)
    return newnode


def setup(app):
    app.add_config_value('epydoc_mapping', {}, 'env')
    app.connect('missing-reference', resolve_reference_to_epydoc)
