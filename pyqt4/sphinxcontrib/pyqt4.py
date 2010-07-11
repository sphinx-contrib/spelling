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
    sphinxcontrib.pyqt4
    ===================

    This extension provides a single directive for the python domain to
    document PyQt4 signals.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


from sphinx.locale import l_, _
from sphinx.domains import ObjType
from sphinx.domains.python import PythonDomain, PyClassmember, PyXRefRole


class PyQt4Signal(PyClassmember):
    def needs_arglist(self):
        return True

    def get_signature_prefix(self, sig):
        return 'signal '

    def get_index_text(self, modname, name_cls):
        name, cls = name_cls
        add_modules = self.env.config.add_module_names
        try:
            clsname, signame = name.rsplit('.', 1)
        except ValueError:
            if modname:
                return _('%s() (in module %s)') % (name, modname)
            else:
                return '%s()' % name
        if modname and add_modules:
            return _('%s() (%s.%s signal)') % (
                signame, modname, clsname)
        else:
            return _('%s() (%s signal)') % (signame, clsname)


class PyQt4Domain(PythonDomain):
    name = 'pyqt4'
    label = 'PyQt4'

    object_types = PythonDomain.object_types.copy()
    directives = PythonDomain.directives.copy()
    roles = PythonDomain.roles.copy()

    object_types['signal'] = ObjType(l_('signal'), 'sig', 'obj')
    directives['signal'] = PyQt4Signal
    roles['sig'] = PyXRefRole(fix_parens=True)


def setup(app):
    app.add_domain(PyQt4Domain)
