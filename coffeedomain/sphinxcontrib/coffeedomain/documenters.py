from sphinx.util.docstrings import prepare_docstring
from sphinx.ext.autodoc import Documenter, members_option, bool_option, ModuleDocumenter as PyModuleDocumenter
from subprocess import Popen, PIPE
import os.path
import json
import re
 
from .domain import MOD_SEP

class StubObject(object):
    """
    A python object that takes the place of the coffeescript object being
    documented.
    """
    def __init__(self, type, data):
        """
        :param type: The type of CS object, possible types:
            * module
            * class
            * function
            * method
            * staticmethod
        :param data: Data for this object from the ``coffeedoc`` output.
        """
        self.type = type
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    @property
    def __doc__(self):
        return self['docstring']

    def __repr__(self):
        return "<StubObject for %s %s>" % (self.type, self['name'])

class CoffeedocDocumenter(Documenter):
    """
    Base class for documenters that use the output of ``coffeedoc``
    """
    priority = 20
    domain = 'coffee'

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return isinstance(member, StubObject) and member.type == cls.documents_type

    def parse_name(self):
        """
        Determine what module to import and what attribute to document.
        Returns True and sets *self.modname*, *self.objpath*, *self.fullname*,
        *self.args* and *self.retann* if parsing and resolving was successful.
        """
        self.fullname = self.name
        self.modname, path = self.name.split(MOD_SEP)
        self.real_modname = self.modname
        self.objpath = path.split('.')
        self.args = None
        self.retann = None
        return True
            
    def format_name(self):
        return self.modname + MOD_SEP + '.'.join(self.objpath)

    def get_object_members(self, want_all=False):
        members = []
        for type in self.sub_member_keys:
            for obj in self.object[type]:
                members.append((obj['name'], StubObject(type, obj)))
        return False, members

    @property
    def coffeedoc_module(self):
        filename= self.modname + '.coffee'
        return self._load_module(filename)

    def _load_module(self, filename):
        modules = self.env.temp_data.setdefault('coffee:coffeedoc-output', {})
        if filename in modules:
            return modules[filename]
        basedir = self.env.config.coffee_src_dir
        parser  = self.env.config.coffee_src_parser or 'commonjs'

        gencmd = ['coffeedoc', '--stdout', '--renderer', 'json', '--parser',
                  parser, filename]
        docgen = Popen(gencmd, cwd=basedir, stdout=PIPE, shell=True)
        (stdout, stderr) = docgen.communicate()
        data = json.loads(stdout)[0]
        data['path'] = data['path'].replace(basedir+'/', '')
        data['name'] = data['path'].replace('.coffee', MOD_SEP)
        modules[filename] = StubObject('module', data)
        return modules[filename]

    def import_object(self):
        raise NotImplemented("")

class ModuleDocumenter(CoffeedocDocumenter, PyModuleDocumenter):
    objtype = 'module'

    content_indent = u''
    titles_allowed = True

    documents_type = 'module'
    sub_member_keys = ('classes', 'functions')

    option_spec =  {
        'show-dependencies': bool_option
    }

    def import_object(self):
        self.object = self.coffeedoc_module
        return True

    def parse_name(self):
        """
        Determine what module to import and what attribute to document.
        Returns True and sets *self.modname*, *self.objpath*, *self.fullname*,
        *self.args* and *self.retann* if parsing and resolving was successful.
        """
        self.objpath = []
        self.fullname = self.modname = self.name
        return True

    def add_content(self, more_content, no_docstring=False):
        super(ModuleDocumenter, self).add_content(more_content, no_docstring=False)
        if self.options.get('show-dependencies') and self.object['deps']:
            self.add_line('*Dependencies:*', '<autodoc>')
            for localname, module in self.object['deps'].items():
                self.add_line('  * ``%s = require "%s"``' % (localname, module),
                              '<autodoc>')

class SubMember(object):
    option_spec = {
        'members': members_option
    }

    def find_parent_object(self):
        raise NotImplemented("")

    def _import_candidates(self, parent):
        return parent[self.documents_type]

    def import_object(self):
        parent = self.find_parent_object()
        if not parent:
            return None
        for data in self._import_candidates(parent):
            dpath = data['name'].split('.')
            if dpath == self.objpath[-1 * len(dpath):]:
                self.object = StubObject(self.documents_type, data)
                return True
        return False

class ModuleMember(SubMember):
    def find_parent_object(self):
        return self.coffeedoc_module

class ClassMember(SubMember):
    def find_parent_object(self):
        module = self.coffeedoc_module
        for data in module['classes']:
            cpath = data['name'].split('.')
            if cpath == self.objpath[:len(cpath)]:
                return data

class ClassDocumenter(ModuleMember, CoffeedocDocumenter):
    objtype = 'class'
    documents_type = 'classes'
    sub_member_keys = ('staticmethods', 'instancemethods')
    option_spec = {'inherited-members': bool_option}

    def add_directive_header(self, sig):
        super(ClassDocumenter, self).add_directive_header(sig)
        parent = self.object['parent']
        if parent:
            base = self.find_class_fqn(parent)
            self.add_line(u'   :parent: ' + base, '<autodoc>')

    def find_class_fqn(self, parent):
        module = self.coffeedoc_module
        # Module where the parent class came from
        modname = None
        if parent in [c['name'] for c in module['classes']]:
            modname = module['name']

        else:
            for (local_name, dep) in module['deps'].iteritems():
                if local_name.find(parent) >= 0:
                    if dep[0] == '.':
                        modname = self._relpath_modname(dep)
                    else:
                        modname = dep + MOD_SEP
                    break

        if modname:
            return (modname + parent)
        else:
            return parent

    def _relpath_modname(self, path):
        here = os.path.dirname(self.coffeedoc_module['path'])
        path = re.sub('(\\.js|\\.coffee)$', '', path)
        return os.path.normpath(os.path.join(here, path)) + MOD_SEP


class CodeDocumenter(CoffeedocDocumenter):
    sub_member_keys = ()

    def format_signature(self):
        return '(%s)' % ', '.join(self.object['params'])

class FunctionDocumenter(ModuleMember, CodeDocumenter):
    objtype = 'function'
    documents_type = 'functions'

class MethodDocumenter(ClassMember, CodeDocumenter):
    objtype = 'method'
    documents_type = 'instancemethods'

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        if isinstance(member, StubObject) and member.type == cls.documents_type:
            return True

class StaticMethodDocumenter(ClassMember, CodeDocumenter):
    objtype = 'staticmethod'
    documents_type = 'staticmethods'
