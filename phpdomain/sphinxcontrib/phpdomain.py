# -*- coding: utf-8 -*-
"""
    sphinx.domains.php
    ~~~~~~~~~~~~~~~~~~~

    The PHP domain. Based off of the rubydomain by SHIBUKAWA Yoshiki

    :copyright: Copyright 2011 by Mark Story
    :license: BSD, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.compat import Directive
from sphinx.util.docfields import Field, GroupedField, TypedField



php_sig_re = re.compile(
    r'''^ ([\w.]*\:\:)?          # class name(s)
          (\$?\w+)  \s*          # thing name
          (?: \((.*)\)           # optional: arguments
          (?:\s* -> \s* (.*))?   # return annotation
          )? $                   # and nothing more
          ''', re.VERBOSE)


php_paramlist_re = re.compile(r'([\[\],])')  # split at '[', ']' and ','

NS = '\\'

separators = {
  'method':'::', 'function':NS, 'class':NS, 'namespace':NS,
  'global':'', 'const':'::', 'attr': '::$', 'exception': '',
  'staticmethod':'::', 'interface':NS
}

php_separator = re.compile(r"(\w+)?(?:[:]{2})?")


def php_rsplit(fullname):
    items = [item for item in php_separator.findall(fullname)]
    return ''.join(items[:-2]), ''.join(items[1:-1])


class PhpObject(ObjectDescription):
    """
    Description of a general PHP object.
    """
    option_spec = {
        'noindex': directives.flag,
        'module': directives.unchanged,
    }

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument'),
                   typerolename='obj', typenames=('paramtype', 'type')),
        TypedField('variable', label=l_('Variables'), rolename='obj',
                   names=('var', 'ivar', 'cvar'),
                   typerolename='obj', typenames=('vartype',)),
        GroupedField('exceptions', label=l_('Throws'), rolename='exc',
                     names=('throws', 'throw', 'exception', 'except'),
                     can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype', 'returntype')),
    ]

    def get_signature_prefix(self, sig):
        """
        May return a prefix to put before the object name in the signature.
        """
        return ''

    def needs_arglist(self):
        """
        May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """
        Transform a PHP signature into RST nodes.
        Returns (fully qualified name of the thing, classname if any).

        If inside a class, the current class name is handled intelligently:
        * it is stripped from the displayed name if present
        * it is added to the full name (return value) if not present
        """
        m = php_sig_re.match(sig)
        if m is None:
            raise ValueError

        name_prefix, name, arglist, retann = m.groups()

        if not name_prefix:
            name_prefix = ""

        # determine module and class name (if applicable), as well as full name
        modname = self.options.get(
            'namespace', self.env.temp_data.get('php:namespace'))

        classname = self.env.temp_data.get('php:class')
        separator = separators[self.objtype]

        if self.objtype == 'global' or self.objtype == 'function':
            add_module = False
            modname = None
            classname = None
            fullname = name
        else:
            add_module = True
            # name_prefix and a non-static method, means the classname was 
            # repeated. Trim off the <class>::
            if name_prefix and self.objtype != 'staticmethod':
                if name_prefix.startswith(classname):
                    name_prefix = name_prefix[len(classname):].rstrip('::')
                classname = classname.rstrip('::')
                fullname = name_prefix + classname + separator + name
            elif name_prefix:
                classname = classname.rstrip('::')
                fullname = name_prefix + name

            # Currently in a class, but not creating another class,
            elif classname and not self.objtype in ['class', 'exception', 'interface']:
                if not self.env.temp_data['php:in_class']:
                    name_prefix = classname + separator
                
                fullname = classname + separator + name
            else:
                classname = ''
                fullname = name

        signode['namespace'] = modname
        signode['class'] = self.class_name = classname
        signode['fullname'] = fullname

        sig_prefix = self.get_signature_prefix(sig)

        if sig_prefix:
            signode += addnodes.desc_annotation(sig_prefix, sig_prefix)

        if name_prefix:
            if modname and not self.env.temp_data['php:in_class']:
                name_prefix = modname + NS + name_prefix
            signode += addnodes.desc_addname(name_prefix, name_prefix)

        elif add_module and self.env.config.add_module_names:
            if self.objtype == 'global':
                nodetext = ''
                signode += addnodes.desc_addname(nodetext, nodetext)
            else:
                modname = self.options.get(
                    'namespace', self.env.temp_data.get('php:namespace'))

                if modname and not self.env.temp_data.get('php:in_class', False):
                    nodetext = modname + NS
                    signode += addnodes.desc_addname(nodetext, nodetext)

        signode += addnodes.desc_name(name, name)
        if not arglist:
            if self.needs_arglist():
                # for callables, add an empty parameter list
                signode += addnodes.desc_parameterlist()
            if retann:
                signode += addnodes.desc_returns(retann, retann)
            return fullname, name_prefix

        signode += addnodes.desc_parameterlist()

        stack = [signode[-1]]
        for token in php_paramlist_re.split(arglist):
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
        if len(stack) != 1:
            raise ValueError
        if retann:
            signode += addnodes.desc_returns(retann, retann)
        return fullname, name_prefix

    def get_index_text(self, modname, name):
        """
        Return the text for the index entry of the object.
        """
        raise NotImplementedError('must be implemented in subclasses')

    def _is_class_member(self):
        return self.objtype.startswith('method') or self.objtype.startswith('attr')

    def add_target_and_index(self, name_cls, sig, signode):
        if self.objtype == 'global':
            modname = ''
        else:
            modname = self.options.get(
                'namespace', self.env.temp_data.get('php:namespace'))
        separator = separators[self.objtype]
        if self._is_class_member():
            if signode['class']:
                prefix = modname and modname + NS or ''
            else:
                prefix = modname and modname + NS or ''
        else:
            prefix = modname and modname + NS or ''
        fullname = prefix + name_cls[0]

        # note target
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['php']['objects']
            if fullname in objects:
                self.env.warn(
                    self.env.docname,
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    self.lineno)
            objects[fullname] = (self.env.docname, self.objtype)

        indextext = self.get_index_text(modname, name_cls)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              fullname, fullname))



class PhpGloballevel(PhpObject):
    """
    Description of an object on global level (global variables).
    """

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'global':
            return _('%s (global variable)') % name_cls[0]
        else:
            return ''

class PhpNamespacelevel(PhpObject):
    """
    Description of an object on namespace level (functions, constants).
    """

    def needs_arglist(self):
        return self.objtype == 'function'

    def get_signature_prefix(self, sig):
        """
        Adds class prefix for constants created inside classes
        """
        if self.objtype == 'const':
            return _('constant ')
        if self.class_name and self.class_name != '':
            return self.class_name + '::'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'function':
            if not modname:
                return _('%s() (global function)') % name_cls[0]
            return _('%s() (function in %s)') % (name_cls[0], modname)
        elif self.objtype == 'const' and self.class_name != '':
            return _('%s (class constant)') % (name_cls[0])
        elif self.objtype == 'const':
            if not modname:
                return _('%s (global constant)') % (name_cls[0])
            return _('%s (constant in %s)') % (name_cls[0], modname)
        else:
            return ''


class PhpClasslike(PhpObject):
    """
    Description of a class-like object (classes, exceptions).
    """

    def get_signature_prefix(self, sig):
        return self.objtype + ' '

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'class':
            if not modname:
                return _('%s (class)') % name_cls[0]
            return _('%s (class in %s)') % (name_cls[0], modname)
        elif self.objtype == 'interface':
            if not modname:
                return _('%s (interface)') % name_cls[0]
            return _('%s (interface in %s)') % (name_cls[0], modname)
        elif self.objtype == 'exception':
            return name_cls[0]
        else:
            return ''

    def after_content(self):
        self.env.temp_data['php:in_class'] = False

    def before_content(self):
        self.env.temp_data['php:in_class'] = True
        if self.names:
            self.env.temp_data['php:class'] = self.names[0][0]

class PhpClassmember(PhpObject):
    """
    Description of a class member (methods, attributes).
    """

    def get_signature_prefix(self, sig):
        if self.objtype == 'attr':
            return _('property ')
        if self.objtype == 'staticmethod':
            return _('static ')
        return ''

    def needs_arglist(self):
        return self.objtype == 'method'

    def get_index_text(self, modname, name_cls):
        name, cls = name_cls
        add_modules = self.env.config.add_module_names

        if self.objtype.endswith('method') or self.objtype == 'attr':
            try:
                clsname, propname = php_rsplit(name)
            except ValueError:
                propname = name
                clsname = None

        if self.objtype.endswith('method'):
            if modname and clsname is None:
                return _('%s() (in namespace %s)') % (name, modname)
            elif modname and add_modules:
                return _('%s() (%s\\%s method)') % (propname, modname, clsname)
            else:
                return _('%s() (%s method)') % (propname, clsname)
        elif self.objtype == 'attr':
            if modname and clsname is None:
                return _('%s (in namespace %s)') % (name, modname)
            elif modname and add_modules:
                return _('%s (%s\\%s property)') % (propname, modname, clsname)
            else:
                return _('%s (%s property)') % (propname, clsname)
        else:
            return ''

class PhpNamespace(Directive):
    """
    Directive to start a new PHP namespace, which are similar to modules.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'synopsis': lambda x: x,
        'noindex': directives.flag,
        'deprecated': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        noindex = 'noindex' in self.options
        env.temp_data['php:namespace'] = modname
        env.temp_data['php:class'] = None
        env.domaindata['php']['namespaces'][modname] = (
            env.docname, self.options.get('synopsis', ''),
            'deprecated' in self.options)

        targetnode = nodes.target('', '', ids=['namespace-' + modname], ismod=True)
        self.state.document.note_explicit_target(targetnode)
        ret = [targetnode]

        # the synopsis isn't printed; in fact, it is only used in the
        # modindex currently
        if not noindex:
            indextext = _('%s (namespace)') % modname
            inode = addnodes.index(entries=[('single', indextext,
                                             'namespace-' + modname, modname)])
            ret.append(inode)
        return ret


class PhpXRefRole(XRefRole):
    """
    Provides cross reference links for PHP objects
    """
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            if title.startswith("::"):
                title = title[2:]
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                m = re.search(r"(?:\\|[:]{2})(.*)\Z", title)
                if m:
                    title = m.group(1)

        if not title.startswith("$"):
            refnode['php:namespace'] = env.temp_data.get('php:namespace')
            refnode['php:class'] = env.temp_data.get('php:class')

        return title, target

class PhpNamespaceIndex(Index):
    """
    Index subclass to provide the Php module index.
    """

    name = 'modindex'
    localname = l_('PHP Namespace Index')
    shortname = l_('namespaces')

    def generate(self, docnames=None):
        content = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        modules = sorted(self.domain.data['namespaces'].iteritems(),
                         key=lambda x: x[0].lower())
        # sort out collapsable modules
        prev_modname = ''
        num_toplevels = 0
        for modname, (docname, synopsis, deprecated) in modules:
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

            package = modname.split(NS)[0]
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
                            'namespace-' + stripped + modname, '',
                            qualifier, synopsis])
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules
        collapse = len(modules) - num_toplevels < num_toplevels

        # sort by first letter
        content = sorted(content.iteritems())

        return content, collapse

class PhpDomain(Domain):
    """PHP language domain."""
    name = 'php'
    label = 'PHP'
    object_types = {
        'function': ObjType(l_('function'), 'func', 'obj'),
        'global': ObjType(l_('global variable'), 'global', 'obj'),
        'const': ObjType(l_('const'), 'const', 'obj'),
        'method': ObjType(l_('method'), 'meth', 'obj'),
        'class': ObjType(l_('class'), 'class', 'obj'),
        'attr': ObjType(l_('attribute'), 'attr', 'obj'),
        'exception': ObjType(l_('exception'), 'exc', 'obj'),
        'namespace': ObjType(l_('namespace'), 'ns', 'obj'),
        'interface': ObjType(l_('interface'), 'interface', 'obj'),
    }

    directives = {
        'function': PhpNamespacelevel,
        'global': PhpGloballevel,
        'const': PhpNamespacelevel,
        'class': PhpClasslike,
        'method': PhpClassmember,
        'staticmethod': PhpClassmember,
        'attr': PhpClassmember,
        'exception': PhpClasslike,
        'namespace': PhpNamespace,
        'interface': PhpClasslike,
    }

    roles = {
        'func': PhpXRefRole(fix_parens=False),
        'global': PhpXRefRole(),
        'class': PhpXRefRole(),
        'exc': PhpXRefRole(),
        'meth': PhpXRefRole(fix_parens=False),
        'attr': PhpXRefRole(),
        'const': PhpXRefRole(),
        'ns': PhpXRefRole(),
        'obj': PhpXRefRole(),
        'interface': PhpXRefRole(),
    }

    initial_data = {
        'objects': {},  # fullname -> docname, objtype
        'namespaces': {},  # namespace -> docname, synopsis
    }
    indices = [
        PhpNamespaceIndex,
    ]

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]
        for ns, (fn, _, _) in self.data['namespaces'].items():
            if fn == docname:
                del self.data['namespaces'][ns]

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        if (typ == 'ns' or
            typ == 'obj' and target in self.data['namespaces']):
            docname, synopsis, deprecated = \
                self.data['namespaces'].get(target, ('','','', ''))
            if not docname:
                return None
            else:
                title = '%s%s' % (synopsis,
                                    (deprecated and ' (deprecated)' or ''))
                return make_refnode(builder, fromdocname, docname,
                                    'namespace-' + target, contnode, title)
        else:
            modname = node.get('php:namespace')
            clsname = node.get('php:class')
            searchorder = node.hasattr('refspecific') and 1 or 0
            name, obj = self.find_obj(env, modname, clsname,
                                      target, typ, searchorder)
            if not obj:
                return None
            else:
                return make_refnode(builder, fromdocname, obj[0], name,
                                    contnode, name)

    def find_obj(self, env, modname, classname, name, type, searchorder=0):
        """
        Find a PHP object for "name", perhaps using the given namespace and/or
        classname.
        """
        # skip parens
        if name[-2:] == '()':
            name = name[:-2]

        if not name:
            return None, None

        objects = self.data['objects']

        newname = None
        if searchorder == 1:
            if modname and classname and \
                     modname + NS + classname + '::' + name in objects:
                newname = modname + NS + classname + '::' + name
            elif modname and modname + NS + name in objects:
                newname = modname + NS + name
            elif modname and modname + NS + name in objects:
                newname = modname + NS + name
            elif classname and classname + '::' + name in objects:
                newname = classname + '.' + name
            elif classname and classname + '::$' + name in objects:
                newname = classname + '::$' + name
            elif name in objects:
                newname = name
        else:
            if name in objects:
                newname = name
            elif classname and classname + '::' + name in objects:
                newname = classname + '::' + name
            elif classname and classname + '::$' + name in objects:
                newname = classname + '::$' + name
            elif modname and modname + NS + name in objects:
                newname = modname + NS + name
            elif modname and classname and \
                     modname + NS + classname + '::' + name in objects:
                newname = modname + NS + classname + '::' + name
            elif modname and classname and \
                     modname + NS + classname + '::$' + name in objects:
                newname = modname + NS + classname + '::$' + name
            # special case: object methods
            elif type in ('func', 'meth') and '::' not in name and \
                 'object::' + name in objects:
                newname = 'object::' + name
        if newname is None:
            return None, None
        return newname, objects[newname]

    def get_objects(self):
        for ns, info in self.data['namespaces'].iteritems():
            yield (ns, ns, 'namespace', info[0], 'namespace-' + ns, 0)
        for refname, (docname, type) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(PhpDomain)
