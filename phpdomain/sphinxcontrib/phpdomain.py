# -*- coding: utf-8 -*-
"""
    sphinx.domains.php
    ~~~~~~~~~~~~~~~~~~~

    The PHP domain.

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
    r'''^ ([\w.]*\.)?            # class name(s)
          (\$?\w+\??!?)  \s*     # thing name
          (?: \((.*)\)           # optional: arguments
           (?:\s* -> \s* (.*))?  #           return annotation
          )? $                   # and nothing more
          ''', re.VERBOSE)


php_paramlist_re = re.compile(r'([\[\],])')  # split at '[', ']' and ','

separators = {
  'method':'::', 'function':'', 'class':'', 'namespace':'\\',
  'global':'', 'const':'::', 'attr': '::$'
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
              names=('rtype',)),
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

        if self.objtype == 'global':
            add_module = False
            modname = None
            classname = None
            fullname = name
        elif classname:
            add_module = False
            if name_prefix and name_prefix.startswith(classname):
                fullname = name_prefix + name
                # class name is given again in the signature
                name_prefix = name_prefix[len(classname):].lstrip('.')
            else:
                separator = separators[self.objtype]
                fullname = classname + separator + name_prefix + name
        else:
            add_module = True
            if name_prefix:
                classname = name_prefix.rstrip('.')
                fullname = name_prefix + name
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
            signode += addnodes.desc_addname(name_prefix, name_prefix)
        # exceptions are a special case, since they are documented in the
        # 'exceptions' module.
        elif add_module and self.env.config.add_module_names:
            if self.objtype == 'global':
                nodetext = ''
                signode += addnodes.desc_addname(nodetext, nodetext)
            else:
                modname = self.options.get(
                    'namespace', self.env.temp_data.get('php:namespace'))
                if modname and modname != 'exceptions':
                    nodetext = modname + separators[self.objtype]
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
        return self.objtype.endswith('method') or self.objtype.startswith('attr')

    def add_target_and_index(self, name_cls, sig, signode):
        if self.objtype == 'global':
            modname = ''
        else:
            modname = self.options.get(
                'namespace', self.env.temp_data.get('php:namespace'))
        separator = separators[self.objtype]
        if self._is_class_member():
            if signode['class']:
                prefix = modname and modname + '::' or ''
            else:
                prefix = modname and modname + separator or ''
        else:
            prefix = modname and modname + separator or ''
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

    def before_content(self):
        # needed for automatic qualification of members (reset in subclasses)
        self.clsname_set = False

    def after_content(self):
        if self.clsname_set:
            self.env.temp_data['php:class'] = None



class PhpGloballevel(PhpObject):
    """
    Description of an object on global level (functions, constants, data).
    """

    def get_signature_prefix(self, sig):
        """
        Adds class prefix for constants created inside classes
        """
        if self.class_name:
            return self.class_name + '::'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'global':
            return _('%s (global variable)') % name_cls[0]
        elif self.objtype == 'const' and self.class_name != '':
            return _('%s (class constant)') % (name_cls[0])
        elif self.objtype == 'const':
            return _('%s (global constant)') % name_cls[0]
        else:
            return ''

class PhpNamespacelevel(PhpObject):
    """
    Description of an object on namespace level (functions, global vars).
    """

    def needs_arglist(self):
        return self.objtype == 'function'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'function':
            if not modname:
                return _('%s() (global function)') % name_cls[0]
            return _('%s() (namespace function in %s)') % (name_cls[0], modname)
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
        elif self.objtype == 'exception':
            return name_cls[0]
        else:
            return ''

    def before_content(self):
        PhpObject.before_content(self)
        if self.names:
            self.env.temp_data['php:class'] = self.names[0][0]
            self.clsname_set = True

class PhpClassmember(PhpObject):
    """
    Description of a class member (methods, attributes).
    """

    def get_signature_prefix(self, sig):
        if self.objtype == 'attr':
            return _('property ')
        return ''

    def needs_arglist(self):
        return self.objtype == 'method'

    def get_index_text(self, modname, name_cls):
        name, cls = name_cls
        add_modules = self.env.config.add_module_names

        if self.objtype == 'method' or self.objtype == 'attr':
            try:
                clsname, propname = php_rsplit(name)
            except ValueError:
                propname = name
                clsname = None
        
        if self.objtype == 'method':
            if modname and clsname is None:
                return _('%s() (in namespace %s)') % (name, modname)
            elif modname and add_modules:
                return _('%s() (%s\\%s method)') % (propname, modname, clsname)
            else:
                return _('%s() (%s method)') % (propname, clsname)
        elif self.objtype == 'attr':
            if modname and clsname is None:
                return _('$%s (in namespace %s)') % (name, modname)
            elif modname and add_modules:
                return _('$%s (%s\\%s property)') % (propname, modname, clsname)
            else:
                return _('$%s (%s property)') % (propname, clsname)
        else:
            return ''

class PhpNamespace(PhpObject):
    pass


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
        'attr': ObjType(l_('attribute'), 'attr', 'obj')
        # 'exception': ObjType(l_('exception'), 'exc', 'obj'),
        # 'namespace': ObjType(l_('namespace'), 'ns', 'obj'),
    }

    directives = {
        'function': PhpNamespacelevel,
        'global': PhpGloballevel,
        'const': PhpGloballevel,
        'class': PhpClasslike,
        'method': PhpClassmember,
        'attr': PhpClassmember
        # 'exception': PhpClasslike,
        # 'namespace': PhpNamespace,
    }

    # roles = {
    #         'func':  RubyXRefRole(fix_parens=False),
    #         'global':RubyXRefRole(),
    #         'class': RubyXRefRole(),
    #         'exc':   RubyXRefRole(),
    #         'meth':  RubyXRefRole(fix_parens=False),
    #         'attr':  RubyXRefRole(),
    #         'const': RubyXRefRole(),
    #         'mod':   RubyXRefRole(),
    #         'obj':   RubyXRefRole(),
    #     }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
        'namespaces': {},  # namespace -> docname, synopsis
    }
    # indices = [
    #         RubyModuleIndex,
    #     ]

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]
        for ns, (fn, _, _, _) in self.data['namespaces'].items():
            if fn == docname:
                del self.data['namespaces'][ns]

    def get_objects(self):
        for ns, info in self.data['namespaces'].iteritems():
            yield (ns, ns, 'namespace', info[0], 'namespace-' + ns, 0)
        for refname, (docname, type) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(PhpDomain)