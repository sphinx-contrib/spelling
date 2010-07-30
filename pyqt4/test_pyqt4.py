#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sphinx.locale
from mock import Mock

from sphinxcontrib import pyqt4


# mock translator to return messages unchanged
sphinx.locale.translator = Mock()
sphinx.locale.translator.ugettext = lambda m: m


def pytest_funcarg__app(request):
    return Mock()


def pytest_funcarg__env(request):
    return Mock()


def pytest_funcarg__signal(request):
    env = request.getfuncargvalue('env')
    state = Mock()
    state.document.settings.env = env
    state_machine = Mock()
    state_machine.get_source_and_line.return_value = (Mock(), Mock())
    signal = pyqt4.PyQt4Signal('signal', [], {}, [], 1, 1, '', state,
                               state_machine)
    signal.env = env
    return signal


def test_signal_needs_arglist(signal):
    assert signal.needs_arglist()


def test_signal_get_signature_prefix(signal):
    assert signal.get_signature_prefix('') == 'PyQt4 signal '
    assert signal.get_signature_prefix('foo') == 'PyQt4 signal '


def test_signal_get_index_text_with(signal, env):
    env.config.add_module_names = True
    assert signal.get_index_text('', ('say', None)) == \
           'say()'
    assert signal.get_index_text('hello', ('say', None)) == \
           'say() (in module hello)'
    assert signal.get_index_text('', ('World.say', None)) == \
           'say() (World signal)'
    assert signal.get_index_text('', ('World.say', None)) == \
           'say() (World signal)'
    env.config.add_module_names = False
    assert signal.get_index_text('', ('say', None)) == \
           'say()'
    assert signal.get_index_text('hello', ('say', None)) == \
           'say() (in module hello)'
    assert signal.get_index_text('', ('World.say', None)) == \
           'say() (World signal)'
    assert signal.get_index_text('', ('World.say', None)) == \
           'say() (World signal)'


def test_domain_attributes():
    domain = pyqt4.PyQt4Domain
    assert domain.name == 'pyqt4'
    assert domain.label == 'PyQt4'
    assert 'signal' in domain.object_types
    assert domain.directives['signal'] is pyqt4.PyQt4Signal
    assert 'signal' in domain.roles
    # make sure, that we copied attributes from base class
    base = domain.__bases__[0]
    assert 'signal' not in base.object_types
    assert 'signal' not in base.directives
    assert 'signal' not in base.roles


def test_setup(app):
    pyqt4.setup(app)
    assert app.add_domain.called
    app.add_domain.assert_called_with(pyqt4.PyQt4Domain)


def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
