# -*- coding: utf-8 -*-
"""
    sphinxcontrib.adadomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Ada domain.

    :copyright: Copyright 2010 by Tero Koskinen
    :license: BSD, see LICENSE for details.

    Some parts of the code copied from erlangdomain by SHIBUKAWA Yoshiki.
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

# REs for Ada function signatures
ada_func_sig_re = re.compile(
    r'''^function\s+([\w.]*\.)?
                   (\w+)\s*
                   (\((.*)\))?\s*
                   return\s+(\w+)\s*
                   (is\s+abstract)?;$
          ''', re.VERBOSE)

ada_proc_sig_re = re.compile(
    r'''^procedure\s+([\w.]*\.)?
                   (\w+)\s*
                   (\((.*)\))?\s*
                   (is\s+abstract)?\s*;$
              ''', re.VERBOSE)

ada_type_sig_re = re.compile(
    r'''^type\s+(\w+)\s+is(.*);$''', re.VERBOSE)

ada_paramlist_re = re.compile(r'(;)')

class AdaObject(ObjectDescription):
    """
    Description of an Ada language object.
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

    def needs_arglist(self):
        return self.objtype == 'function' or self.objtype == 'procedure'

    def _resolve_module_name(self, signode, modname, name):
        env_modname = self.options.get(
            'module', self.env.temp_data.get('ada:module', 'ada'))
        if modname:
            fullname = modname + name
            signode['module'] = modname[:-1]
        else:
            fullname = env_modname + '.' + name
            signode['module'] = env_modname

        signode['fullname'] = fullname
        name_prefix = signode['module'] + '.'
        signode += addnodes.desc_addname(name_prefix, name_prefix)
        signode += addnodes.desc_name(name, name)
        return fullname

    def _handle_function_signature(self, sig, signode):
        m = ada_func_sig_re.match(sig)
        if m is None:
            print "m did not match the function"
            raise ValueError

        modname, name, dummy, arglist, returntype, abstract = m.groups()
        print "DEBUG: modname %s name %s arglist %s" % (modname, name, arglist)

        fullname = self._resolve_module_name(signode, modname, name)
        print "DEBUG: fullname %s" % fullname

        if not arglist:
            if self.needs_arglist():
                # for functions and procedures, add an empty parameter list
                new_node = addnodes.desc_parameterlist()
                new_node.child_text_separator = '; '
                signode += new_node
            if returntype:
                signode += addnodes.desc_returns(returntype, returntype)
            return fullname

        signode += nodes.Text(' ')

        new_node = addnodes.desc_parameterlist()
        new_node.child_text_separator = '; '
        signode += new_node

        stack = [signode[-1]]
        counters = [0, 0]
        for token in string.split(arglist, ';'):
            pieces = string.split(token, ':')
            name = pieces[0].strip()
            stack[-1] += addnodes.desc_parameter(name, name + " : " + pieces[1].strip())

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
        if returntype:
            signode += addnodes.desc_returns(returntype,returntype)
        return fullname


        
    def _handle_procedure_signature(self, sig, signode):
        print "DEBUG: _handle_procedure_signature"
        m = ada_proc_sig_re.match(sig)
        if m is None:
            print "m did not match"
            raise ValueError

        modname, name, dummy, arglist, abstract = m.groups()
        print "DEBUG: modname %s name %s arglist %s" % (modname, name, arglist)

        fullname = self._resolve_module_name(signode, modname, name)
        print "DEBUG: fullname: %s" % fullname

        if not arglist:
            if self.needs_arglist():
                # for functions and procedures, add an empty parameter list
                newnode = addnodes.desc_parameterlist()
                newnode.child_text_separator = '; '
                signode += newnode

        signode += nodes.Text(' ')

        newnode = addnodes.desc_parameterlist()
        newnode.child_text_separator = '; '
        signode += newnode

        stack = [signode[-1]]
        counters = [0, 0]
        for token in string.split(arglist, ';'):
            pieces = string.split(token, ':')
            name = pieces[0].strip()
            stack[-1] += addnodes.desc_parameter(name, name + " : " + pieces[1].strip())
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
        return fullname

    def _handle_type_signature(self, sig, signode):
        print "DEBUG: _handle_type_signature"
        m = ada_type_sig_re.match(sig)
        if m is None:
            print "m did not match"
            raise ValueError

        name, value = m.groups()
        fullname = self._resolve_module_name(signode, '', name)
        
        # signode += addnodes.desc_parameterlist()

        # stack = [signode[-1]]

        # signode += addnodes.desc_type(name, name + " is " + value)
        signode += addnodes.desc_type(name, '')

        return fullname


    def handle_signature(self, sig, signode):
        print "HANDLE: %s!" % sig
        if sig.startswith('function'):
            return self._handle_function_signature (sig, signode)
        elif sig.startswith('type'):
            return self._handle_type_signature (sig, signode)
        else: # sig.startswith('procedure'):
            return self._handle_procedure_signature (sig, signode)

    def _get_index_text(self, name):
        if self.objtype == 'function':
            return _('%s (Ada function)') % name
        elif self.objtype == 'procedure':
            return _('%s (Ada procedure)') % name
        elif self.objtype == 'type':
            return _('%s (Ada type)') % name
        else:
            return ''


    def add_target_and_index(self, name, sig, signode):
        print "DEBUG: add_target_and_index name = %s" % name
        pieces = string.split(name, '.')
        if name not in self.state.document.ids:
            signode['names'].append(name)
            signode['ids'].append(name)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            if self.objtype =='function':
                finv = self.env.domaindata['ada']['functions']
                fname, arity = name.split('/')
                if '..' in arity:
                    first, last = map(int, arity.split('..'))
                else:
                    first = last = int(arity)
                for arity_index in range(first, last+1):
                    if fname in finv and arity_index in finv[fname]:
                        self.env.warn(
                            self.env.docname,
                            ('duplicate Ada function description'
                             'of %s, ') % name +
                            'other instance in ' +
                            self.env.doc2path(finv[fname][arity_index][0]),
                            self.lineno)
                    arities = finv.setdefault(fname, {})
                    arities[arity_index] = (self.env.docname, name)
            if self.objtype == 'procedure':
                finv = self.env.domaindata['ada']['procedures']
                fname, arity = name.split('/')
                if '..' in arity:
                    first, last = map(int, arity.split('..'))
                else:
                    first = last = int(arity)
                for arity_index in range(first, last+1):
                    if fname in finv and arity_index in finv[fname]:
                        self.env.warn(
                            self.env.docname,
                            ('duplicate Ada procedure description'
                             'of %s, ') % name +
                            'other instance in ' +
                            self.env.doc2path(finv[fname][arity_index][0]),
                            self.lineno)
                    arities = finv.setdefault(fname, {})
                    arities[arity_index] = (self.env.docname, name)
            else:
                oinv = self.env.domaindata['ada']['objects']
                if name in oinv:
                    self.env.warn(
                        self.env.docname,
                        'duplicate Ada object description of %s, ' % name +
                        'other instance in ' + self.env.doc2path(oinv[name][0]),
                        self.lineno)
                oinv[name] = (self.env.docname, self.objtype)

        indextext = self._get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext, name, name))

        plain_name = pieces[-1]
        indextext = self._get_index_text(plain_name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext, name, plain_name))


class AdaModule(Directive):
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
        env.temp_data['ada:module'] = modname
        env.domaindata['ada']['modules'][modname] = \
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

class AdaCurrentModule(Directive):
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
            env.temp_data['ada:module'] = None
        else:
            env.temp_data['ada:module'] = modname
        return []

class AdaXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['ada:module'] = env.temp_data.get('ada:module')
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

class AdaModuleIndex(Index):
    """
    Index subclass to provide the Ada module index.
    """

    name = 'modindex'
    localname = l_('Ada Module Index')
    shortname = l_('Ada modules')

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

class AdaDomain(Domain):
    """Ada language domain."""
    name = 'ada'
    label = 'Ada'
    object_types = {
        'function':  ObjType(l_('function'),  'func'),
        'procedure': ObjType(l_('procedure'), 'proc'),
        'type':      ObjType(l_('type'),      'type'),
        'module':    ObjType(l_('module'),    'mod'),
    }

    directives = {
        'function':      AdaObject,
        'procedure':     AdaObject,
        'type':        AdaObject,
        'module':        AdaModule,
        'currentmodule': AdaCurrentModule,
    }
    roles = {
        'func':   AdaXRefRole(),
        'proc':   AdaXRefRole(),
        'type':   AdaXRefRole(),
        'mod':    AdaXRefRole(),
    }
    initial_data = {
        'objects': {},     # fullname -> docname, objtype
        'functions' : {},  # fullname -> arity -> (targetname, docname)
        'procedures' : {}, # fullname -> arity -> (targetname, docname)
        'modules': {},     # modname -> docname, synopsis, platform, deprecated
    }
    indices = [
        AdaModuleIndex,
    ]

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]
        for modname, (fn, _, _, _) in self.data['modules'].items():
            if fn == docname:
                del self.data['modules'][modname]
        for fullname, funcs in self.data['functions'].items():
            for arity, (fn, _) in funcs.items():
                if fn == docname:
                    del self.data['functions'][fullname][arity]
            if not self.data['functions'][fullname]:
                del self.data['functions'][fullname]
        for fullname, funcs in self.data['procedures'].items():
            for arity, (fn, _) in funcs.items():
                if fn == docname:
                    del self.data['procedures'][fullname][arity]
            if not self.data['procedures'][fullname]:
                del self.data['procedures'][fullname]

    def _find_obj(self, env, modname, name, objtype, searchorder=0):
        """
        Find a Ada object for "name", perhaps using the given module and/or
        classname.
        """
        print "_find_obj: modname %s name %s" % (modname, name)
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
        if fname in self.data['functions']:
            arities = self.data['functions'][fname]
        elif fname in self.data['procedures']:
            arities = self.data['procedures'][fname]
        else:
            return None, None

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
            modname = node.get('ada:module')
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
    app.add_domain(AdaDomain)
