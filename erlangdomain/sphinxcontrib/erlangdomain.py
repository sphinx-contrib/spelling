# -*- coding: utf-8 -*-
"""
    sphinxcontrib.erlangdomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Erlang domain.

    :copyright: Copyright 2007-2010 by SHIBUKAWA Yoshiki
    :license: BSD, see LICENSE for details.
"""

import re
import string

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType, Index
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, TypedField


# RE to split at word boundaries
wsplit_re = re.compile(r'(\W+)')

# REs for Erlang signatures
erl_func_sig_re = re.compile(
    r'''^ ([\w.]*:)?             # module name
          (\w+)  \s*             # thing name
          (?: \((.*)\)           # optional: arguments
           (?:\s* -> \s* (.*))?  #           return annotation
          )? $                   # and nothing more
          ''', re.VERBOSE)


erl_macro_sig_re = re.compile(
    r'''^ ([\w.]*:)?             # module name
          ([A-Z]\w+) $           # thing name
          ''', re.VERBOSE)


erl_record_sig_re = re.compile(
    r'''^ ([\w.]*:)?             # module name
          (\#\w+) $              # thing name
          ''', re.VERBOSE)


erl_paramlist_re = re.compile(r'([\[\],])')  # split at '[', ']' and ','


class ErlangObject(ObjectDescription):
    """
    Description of a Erlang language object.
    """

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument'),
                   typerolename='type', typenames=('type',)),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype',)),
    ]

    def _add_signature_prefix(self, signode):
        if self.objtype != 'function':
            sig_prefix = self.objtype + ' '
            signode += addnodes.desc_annotation(sig_prefix, sig_prefix)

    def needs_arglist(self):
        return self.objtype == 'function'

    def handle_signature(self, sig, signode):
        if sig.startswith('#'):
            return self._handle_record_signature(sig, signode)
        elif sig[0].isupper():
            return self._handle_macro_signature(sig, signode)
        return self._handle_function_signature(sig, signode)

    def _resolve_module_name(self, signode, modname, name):
        # determine module name, as well as full name
        env_modname = self.options.get(
            'module', self.env.temp_data.get('erl:module', 'erlang'))
        if modname:
            fullname = modname + name
            signode['module'] = modname[:-1]
        else:
            fullname = env_modname + ':' + name
            signode['module'] = env_modname
        signode['fullname'] = fullname
        self._add_signature_prefix(signode)
        name_prefix = signode['module'] + ':'
        signode += addnodes.desc_addname(name_prefix, name_prefix)
        signode += addnodes.desc_name(name, name)
        return fullname

    def _handle_record_signature(self, sig, signode):
        m = erl_record_sig_re.match(sig)
        if m is None:
            raise ValueError
        modname, name = m.groups()
        return self._resolve_module_name(signode, modname, name)

    def _handle_macro_signature(self, sig, signode):
        m = erl_macro_sig_re.match(sig)
        if m is None:
            raise ValueError
        modname, name = m.groups()
        return self._resolve_module_name(signode, modname, name)

    def _handle_function_signature(self, sig, signode):
        m = erl_func_sig_re.match(sig)
        if m is None:
            raise ValueError
        modname, name, arglist, retann = m.groups()

        fullname = self._resolve_module_name(signode, modname, name)

        if not arglist:
            if self.needs_arglist():
                # for callables, add an empty parameter list
                signode += addnodes.desc_parameterlist()
            if retann:
                signode += addnodes.desc_returns(retann, retann)
            if self.objtype == 'function':
                return fullname + '/0'
            return fullname
        signode += addnodes.desc_parameterlist()

        stack = [signode[-1]]
        counters = [0, 0]
        for token in erl_paramlist_re.split(arglist):
            if token == '[':
                opt = addnodes.desc_optional()
                stack[-1] += opt
                stack.append(opt)
            elif token == ']':
                try:
                    stack.pop()
                except IndexError:
                    raise ValueError
            elif not token or token == ',' or token.isspace():
                pass
            else:
                token = token.strip()
                stack[-1] += addnodes.desc_parameter(token, token)
                if len(stack) == 1:
                    counters[0] += 1
                else:
                    counters[1] += 1
        if len(stack) != 1:
            raise ValueError
        if not counters[1]:
            fullname = '%s/%d' % (fullname, counters[0])
        else:
            fullname = '%s/%d..%d' % (fullname, counters[0], sum(counters))
        if retann:
            signode += addnodes.desc_returns(retann, retann)
        return fullname

    def _get_index_text(self, name):
        if self.objtype == 'function':
            return _('%s (Erlang function)') % name
        elif self.objtype == 'macro':
            return _('%s (Erlang macro)') % name
        elif self.objtype == 'record':
            return _('%s (Erlang record)') % name
        else:
            return ''

    def add_target_and_index(self, name, sig, signode):
        if name not in self.state.document.ids:
            signode['names'].append(name)
            signode['ids'].append(name)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            if self.objtype =='function':
                finv = self.env.domaindata['erl']['functions']
                fname, arity = name.split('/')
                if '..' in arity:
                    first, last = map(int, arity.split('..'))
                else:
                    first = last = int(arity)
                for arity_index in range(first, last+1):
                    if fname in finv and arity_index in finv[fname]:
                        self.env.warn(
                            self.env.docname,
                            ('duplicate Erlang object description'
                             'of %s, ') % name +
                            'other instance in ' +
                            self.env.doc2path(oinv[name][0]),
                            self.lineno)
                    arities = finv.setdefault(fname, {})
                    arities[arity_index] = (self.env.docname, name)
            else:
                oinv = self.env.domaindata['erl']['objects']
                if name in oinv:
                    self.env.warn(
                        self.env.docname,
                        'duplicate Erlang object description of %s, ' % name +
                        'other instance in ' + self.env.doc2path(oinv[name][0]),
                        self.lineno)
                oinv[name] = (self.env.docname, self.objtype)

        indextext = self._get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext, name, name))


class ErlangModule(Directive):
    """
    Directive to mark description of a new module.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'platform': lambda x: x,
        'synopsis': lambda x: x,
        'noindex': directives.flag,
        'deprecated': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        noindex = 'noindex' in self.options
        env.temp_data['erl:module'] = modname
        env.domaindata['erl']['modules'][modname] = \
            (env.docname, self.options.get('synopsis', ''),
             self.options.get('platform', ''), 'deprecated' in self.options)
        targetnode = nodes.target('', '', ids=['module-' + modname], ismod=True)
        self.state.document.note_explicit_target(targetnode)
        ret = [targetnode]
        # XXX this behavior of the module directive is a mess...
        if 'platform' in self.options:
            platform = self.options['platform']
            node = nodes.paragraph()
            node += nodes.emphasis('', _('Platforms: '))
            node += nodes.Text(platform, platform)
            ret.append(node)
        # the synopsis isn't printed; in fact, it is only used in the
        # modindex currently
        if not noindex:
            indextext = _('%s (module)') % modname
            inode = addnodes.index(entries=[('single', indextext,
                                             'module-' + modname, modname)])
            ret.append(inode)
        return ret


class ErlangCurrentModule(Directive):
    """
    This directive is just to tell Sphinx that we're documenting
    stuff in module foo, but links to module foo won't lead here.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        if modname == 'None':
            env.temp_data['erl:module'] = None
        else:
            env.temp_data['erl:module'] = modname
        return []


class ErlangXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['erl:module'] = env.temp_data.get('erl:module')
        if not has_explicit_title:
            title = title.lstrip(':')   # only has a meaning for the target
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                colon = title.rfind(':')
                if colon != -1:
                    title = title[colon+1:]
        return title, target


class ErlangModuleIndex(Index):
    """
    Index subclass to provide the Erlang module index.
    """

    name = 'modindex'
    localname = l_('Erlang Module Index')
    shortname = l_('modules')

    def generate(self, docnames=None):
        content = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        modules = sorted(self.domain.data['modules'].iteritems(),
                         key=lambda x: x[0].lower())
        # sort out collapsable modules
        prev_modname = ''
        num_toplevels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue

            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ''

            # we stripped the whole module name?
            if not modname:
                modname, stripped = stripped, ''

            entries = content.setdefault(modname[0].lower(), [])

            package = modname.split(':')[0]
            if package != modname:
                # it's a submodule
                if prev_modname == package:
                    # first submodule - make parent a group head
                    entries[-1][1] = 1
                elif not prev_modname.startswith(package):
                    # submodule without parent in list, add dummy entry
                    entries.append([stripped + package, 1, '', '', '', '', ''])
                subtype = 2
            else:
                num_toplevels += 1
                subtype = 0

            qualifier = deprecated and _('Deprecated') or ''
            entries.append([stripped + modname, subtype, docname,
                            'module-' + stripped + modname, platforms,
                            qualifier, synopsis])
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules
        collapse = len(modules) - num_toplevels < num_toplevels

        # sort by first letter
        content = sorted(content.iteritems())

        return content, collapse


class ErlangDomain(Domain):
    """Erlang language domain."""
    name = 'erl'
    label = 'Erlang'
    object_types = {
        'function': ObjType(l_('function'), 'func'),
        'macro':    ObjType(l_('macro'),    'macro'),
        'record':   ObjType(l_('record'),   'record'),
        'module':   ObjType(l_('module'),   'mod'),
    }

    directives = {
        'function':      ErlangObject,
        'macro':         ErlangObject,
        'record':        ErlangObject,
        'module':        ErlangModule,
        'currentmodule': ErlangCurrentModule,
    }
    roles = {
        'func' :  ErlangXRefRole(),
        'macro':  ErlangXRefRole(),
        'record': ErlangXRefRole(),
        'mod':    ErlangXRefRole(),
    }
    initial_data = {
        'objects': {},    # fullname -> docname, objtype
        'functions' : {}, # fullname ->  arity -> (targetname, docname)
        'modules': {},    # modname -> docname, synopsis, platform, deprecated
    }
    indices = [
        ErlangModuleIndex,
    ]

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]
        for modname, (fn, _, _, _) in self.data['modules'].items():
            if fn == docname:
                del self.data['modules'][modname]

    def _find_obj(self, env, modname, name, objtype, searchorder=0):
        """
        Find a Python object for "name", perhaps using the given module and/or
        classname.
        """
        if not name:
            return None, None
        if ":" not in name:
            name = "%s:%s" % (modname, name)

        if name in self.data['objects']:
            return name, self.data['objects'][name][0]

        if '/' in name:
            fname, arity = name.split('/')
            arity = int(arity)
        else:
            fname = name
            arity = -1
        if fname not in self.data['functions']:
            return None, None

        arities = self.data['functions'][fname]
        if arity == -1:
            arity = min(arities)
        if arity in arities:
             docname, targetname = arities[arity]
             return targetname, docname
        return None, None

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        if typ == 'mod' and target in self.data['modules']:
            docname, synopsis, platform, deprecated = \
                self.data['modules'].get(target, ('','','', ''))
            if not docname:
                return None
            else:
                title = '%s%s%s' % ((platform and '(%s) ' % platform),
                                    synopsis,
                                    (deprecated and ' (deprecated)' or ''))
                return make_refnode(builder, fromdocname, docname,
                                    'module-' + target, contnode, title)
        else:
            modname = node.get('erl:module')
            searchorder = node.hasattr('refspecific') and 1 or 0
            name, obj = self._find_obj(env, modname, target, typ, searchorder)
            if not obj:
                return None
            else:
                return make_refnode(builder, fromdocname, obj, name,
                                    contnode, name)

    def get_objects(self):
        for refname, (docname, type) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(ErlangDomain)
