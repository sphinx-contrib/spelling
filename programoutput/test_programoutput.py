#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@googlemail.com>
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


from itertools import product

import pytest
from mock import Mock, MagicMock
from docutils.parsers.rst import directives
from docutils import nodes

from sphinxcontrib import programoutput


RUN_PROGRAMS_TESTDATA = dict(
    simple={},
    extraargs=dict(extraargs='foo "spam and eggs"'),
    prompt=dict(show_prompt=True),
    prompt_with_extraargs=dict(show_prompt=True,
                               extraargs='foo "spam and eggs"'),
    no_stderr=dict(hide_standard_error=True),
    shell=dict(use_shell=True),
    shell_with_prompt=dict(use_shell=True, show_prompt=True),
    shell_with_extraargs=dict(use_shell=True, show_prompt=True,
                              extraargs='foo "spam and eggs"')
    )


def pytest_generate_tests(metafunc):
    if metafunc.function is test_run_programs:
        for id, use_ansi in product(RUN_PROGRAMS_TESTDATA, (True, False)):
            params = RUN_PROGRAMS_TESTDATA[id]
            if use_ansi:
                id += ',ansi'
            args = dict(use_ansi=use_ansi, params=params)
            metafunc.addcall(funcargs=args, id=id)


def pytest_funcarg__nodecls(request):
    if request.getfuncargvalue('use_ansi'):
        from sphinxcontrib.ansi import ansi_literal_block
        return ansi_literal_block
    else:
        return nodes.literal_block


def pytest_funcarg__cache(request):
    cache = MagicMock()
    cache.__getitem__.return_value = 'some output'
    return cache


def pytest_funcarg__app(request):
    app = Mock()
    app.env = Mock()
    app.env.programoutput_cache = request.getfuncargvalue('cache')
    app.config = Mock()
    app.config.programoutput_use_ansi = request.getfuncargvalue('use_ansi')
    app.config.programoutput_prompt_template = '$ %(command)s\n%(output)s'
    return app


def pytest_funcarg__directive(request):
    state_machine = Mock()
    state_machine.get_source_and_line.return_value = (Mock(), Mock())
    return programoutput.ProgramOutputDirective(
        'program-output', ['some command'], {}, [], 1, 1, '',
        Mock(), state_machine)


def test_slice():
    assert programoutput._slice('2') == (2, None)
    assert programoutput._slice('2,2') == (2, 2)
    with pytest.raises(ValueError) as exc:
        assert programoutput._slice('')
    assert str(exc.value) == "invalid literal for int() with base 10: ''"
    with pytest.raises(ValueError) as exc:
        programoutput._slice('foo,2')
    assert str(exc.value) == "invalid literal for int() with base 10: 'foo'"
    with pytest.raises(ValueError) as exc:
        programoutput._slice('2,2,2')
    assert str(exc.value) == 'too many slice parts'


def test_program_output_directive():
    cls = programoutput.ProgramOutputDirective
    assert not cls.has_content
    assert cls.final_argument_whitespace
    assert cls.required_arguments == 1
    assert cls.option_spec == dict(
        shell=directives.flag,
        prompt=directives.flag,
        nostderr=directives.flag,
        ellipsis=programoutput._slice,
        extraargs=directives.unchanged)


def test_program_output_directive_run_command(directive):
    assert directive.run()[0]['command'] ==  'some command'

def test_program_output_directive_run_nostderr(directive):
    assert not directive.run()[0]['hide_standard_error']
    directive.options['nostderr'] = True
    assert directive.run()[0]['hide_standard_error']

def test_program_output_directive_run_extraargs(directive):
    assert directive.run()[0]['extraargs'] == ''
    directive.options['extraargs'] = 'foo bar'
    assert directive.run()[0]['extraargs'] == 'foo bar'

def test_program_output_directive_run_use_shell(directive):
    assert not directive.run()[0]['use_shell']
    directive.options['shell'] = True
    assert directive.run()[0]['use_shell']

def test_program_output_directive_run_ellipsis(directive):
    assert 'strip_lines' not in directive.run()[0].attributes
    directive.options['ellipsis'] = (2, 2)
    assert directive.run()[0]['strip_lines'] == (2, 2)

def test_program_output_directive_run_show_prompt(directive):
    assert not directive.run()[0]['show_prompt']
    directive.options['prompt'] = True
    assert directive.run()[0]['show_prompt']

def test_command_output_directive_run(directive):
    directive.name = 'command-output'
    assert directive.run()[0]['show_prompt']


def test_program_output_cache():
    cache = programoutput.ProgramOutputCache()
    cmd = ('python', '-c', 'import sys; '
           'sys.stdout.write("hello world"); '
           'sys.stderr.write("goodbye world")')
    assert (cmd, False, True) not in cache
    assert cache[(cmd, False, True)] == 'hello world'
    assert (cmd, False, True) in cache
    assert (cmd, False, False) not in cache
    assert cache[(cmd, False, False)] == 'goodbye worldhello world'
    assert (cmd, False, False) in cache
    cmd = ('python -c \'import sys; '
           'sys.stdout.write("hello world"); '
           'sys.stderr.write("goodbye world")\'')
    assert (cmd, True, False) not in cache
    assert cache[(cmd, True, False)] == 'goodbye worldhello world'
    assert (cmd, True, False) in cache


def _make_node(show_prompt=False, hide_standard_error=False,
               use_shell=False, ellipsis=None, extraargs=None):
    node = programoutput.program_output()
    node['command'] = ("hello 'eggs with spam'")
    node['show_prompt'] = show_prompt
    node['hide_standard_error'] = hide_standard_error
    node['use_shell'] = use_shell
    if ellipsis:
        node['strip_lines'] = ellipsis
    if extraargs:
        node['extraargs'] = extraargs
    return node

def test_run_programs(app, cache, use_ansi, nodecls, params):
    paragraph = nodes.paragraph()
    paragraph.append(_make_node(**params))
    programoutput.run_programs(app, paragraph)
    if params.get('show_prompt'):
        output = "$ hello 'eggs with spam'\nsome output"
    else:
        output = 'some output'
    node = paragraph[0]
    assert node.astext() == output
    assert isinstance(node, nodecls)
    if params.get('use_shell'):
        cmd = "hello 'eggs with spam'"
        if params.get('extraargs'):
            cmd += ' foo "spam and eggs"'
    else:
        cmd = ('hello', 'eggs with spam')
        if params.get('extraargs'):
            cmd += ('foo', 'spam and eggs')
    cache_key = (cmd, params.get('use_shell', False),
                 params.get('hide_standard_error', False))
    cache.__getitem__.assert_called_with(cache_key)


def test_init_cache():
    app = Mock()
    # no mock object here, because we need a conservative __getattr__, which
    # only returns, what really is defined
    app.env = type('obj', (object,), {})()
    assert not hasattr(app.env, 'programoutput_cache')
    programoutput.init_cache(app)
    assert hasattr(app.env, 'programoutput_cache')
    cache = app.env.programoutput_cache
    programoutput.init_cache(app)
    assert app.env.programoutput_cache is cache


def test_setup():
    app = Mock()
    programoutput.setup(app)
    assert app.add_config_value.call_args_list == [
        (('programoutput_use_ansi', False, 'env'), {}),
        (('programoutput_prompt_template',
          '$ %(command)s\n%(output)s', 'env'), {})]
    assert app.add_directive.call_args_list == [
        (('program-output', programoutput.ProgramOutputDirective), {}),
        (('command-output', programoutput.ProgramOutputDirective), {})]
    assert app.connect.call_args_list == [
        (('builder-inited', programoutput.init_cache), {}),
        (('doctree-read', programoutput.run_programs), {})]



def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
