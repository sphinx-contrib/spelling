# -*- coding: utf-8 -*-
"""
Requirement specs
=================

.. module:: sphinx_reqs
   :synopsis: Allow requirement specs into documents.
.. moduleauthor:: Andrey Mikhaylenko

There are two additional directives when using this extension:

.. rst:directive:: req

   Use this directive like, for example, :rst:dir:`note`. Note that all
   requirements get a status (this is not configurable yet). By default it is
   ``undecided`` (see :role:`status` for details). You can define it by using
   the ``status`` option::

       .. requirement::
          :status: todo

          User can view the list of entries

.. rst:directive:: reqlist

   This directive is replaced by a list of all req directives in the whole
   documentation.

An extra role is also provided:

.. rst:role:: status

   Defines the status of a requirement.

   Supported values are:

   * ``undecided`` (default)
   * ``todo``
   * ``done``
   * ``tested``
   * ``wontfix``

   Usage::

       :status:`tested` User can log in
       :status:`done` User can sign up
       :status:`todo` User can haz cheezburger

   Note that "done" and "tested" are intentionally made distinct.

The extension is partially based on sphinx.ext.todo_.

.. _sphinx.ext.todo: http://sphinx.pocoo.org/ext/todo.html

"""
import os
from docutils.parsers.rst import roles, directives
from docutils import nodes, utils
from sphinx.environment import NoUri
from sphinx.locale import _
from sphinx.util.compat import Directive, make_admonition
from sphinx.util.osutil import copyfile


CSS_FILE = 'requirements.css'


def status_role(name, rawtext, text, lineno, inliner, options=None, content=[]):
    status = utils.unescape(text)
    options = options or {}
    options.setdefault('classes', [])
    options['classes'] += ['status', status]
    node = nodes.emphasis(rawtext, status, **options)
    return [node], []


class req_node(nodes.Admonition, nodes.Element): pass
class reqlist(nodes.General, nodes.Element): pass


class ReqlistDirective(Directive):

    def run(self):
        return [reqlist('')]


class ReqDirective(Directive):

    # this enables content in the directive
    has_content = True

    option_spec = {
        'status': unicode,
#        'done': directives.flag,
#        'important': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env


        targetid = "req-%d" % env.new_serialno('req')
        targetnode = nodes.target('', '', ids=[targetid])

        #
        # TODO:
        #   * add config var to define whether the status should be displayed
        #     (e.g. always / never / if explicitly given)
        #
        # insert a large garden gnome^W^W^W^W requirement status
        status = self.options.get('status', 'undecided')
        status_text = ':status:`'+status+'`'
        self.content[0] = status_text +' '+ self.content[0]

        # TODO: replace admonition with a paragraph
        ad = make_admonition(req_node, self.name, [_('Requirement')], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)

        ad[0].line = self.lineno
        return [targetnode] + ad


def process_reqs(app, doctree):
    # collect all reqs in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    if not hasattr(env, 'reqs_all_reqs'):
        env.reqs_all_reqs = []
    for node in doctree.traverse(req_node):
        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        env.reqs_all_reqs.append({
            'docname': env.docname,
            'lineno': node.line,
            'req': node.deepcopy(),
            'target': targetnode,
        })

def process_req_nodes(app, doctree, fromdocname):
    # Replace all reqlist nodes with a list of the collected reqs.
    # Augment each req with a backlink to the original location.
    env = app.builder.env

    if not hasattr(env, 'reqs_all_reqs'):
        env.reqs_all_reqs = []

    for node in doctree.traverse(reqlist):
        content = []

        # TODO: group (and maybe even filter) by docname

        for req_info in env.reqs_all_reqs:

            # (Recursively) resolve references in the req content
            req_entry = req_info['req']
            env.resolve_references(req_entry, req_info['docname'],
                                   app.builder)

            para = nodes.paragraph(classes=['req-source'])
            # collect the first paragraph from the requirement
            try:
                para.extend(req_entry.children[1])
            except IndexError:
                para += nodes.Text(_('(empty spec)'))

            # Create a reference
            refnode = nodes.reference('', '', internal=True)
            innernode = nodes.emphasis(u'→', u'→')
            try:
                refnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, req_info['docname'])
                refnode['refuri'] += '#' + req_info['target']['refid']
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            refnode.append(nodes.Text(' '))
            refnode.append(innernode)
            para += refnode

            content.append(para)

        node.replace_self(content)

def purge_reqs(app, env, docname):
    if not hasattr(env, 'reqs_all_reqs'):
        return
    env.reqs_all_reqs = [req for req in env.reqs_all_reqs
                          if req['docname'] != docname]

def visit_req_node(self, node):
    self.visit_admonition(node)

def depart_req_node(self, node):
    self.depart_admonition(node)

def add_stylesheet(app):
    app.add_stylesheet(CSS_FILE)

def copy_stylesheet(app, exception):
    if app.builder.name != 'html' or exception:
        return
    app.info('Copying requirements stylesheet... ', nonl=True)
    dest = os.path.join(app.builder.outdir, '_static', CSS_FILE)
    source = os.path.join(os.path.abspath(os.path.dirname(__file__)), CSS_FILE)
    copyfile(source, dest)
    app.info('done')

def setup(app):
    app.add_role('status', status_role)
    app.add_node(reqlist)
    app.add_node(req_node,
                 html=(visit_req_node, depart_req_node),
                 latex=(visit_req_node, depart_req_node),
                 text=(visit_req_node, depart_req_node),
                 man=(visit_req_node, depart_req_node),
                 texinfo=(visit_req_node, depart_req_node))

    app.add_directive('requirement', ReqDirective)
    app.add_directive('reqlist', ReqlistDirective)
    app.connect('doctree-read', process_reqs)
    app.connect('doctree-resolved', process_req_nodes)
    app.connect('env-purge-doc', purge_reqs)
    app.connect('builder-inited', add_stylesheet)
    app.connect('build-finished', copy_stylesheet)
