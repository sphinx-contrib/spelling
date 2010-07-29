#!/usr/bin/env python
# -*- coding: utf-8 -*-

import py.test
from mock import Mock

from sphinxcontrib import programoutput
from docutils.parsers.rst import directives


def pytest_funcarg__app(request):
    app = Mock()
    app.env = type('obj', (object,), {})()
    return app


def test_slice():
    assert programoutput._slice('2') == (2, None)
    assert programoutput._slice('2,2') == (2, 2)
    with py.test.raises(ValueError) as exc:
        assert programoutput._slice('')
    assert str(exc.value) == "invalid literal for int() with base 10: ''"
    with py.test.raises(ValueError) as exc:
        programoutput._slice('foo,2')
    assert str(exc.value) == "invalid literal for int() with base 10: 'foo'"
    with py.test.raises(ValueError) as exc:
        programoutput._slice('2,2,2')
    assert str(exc.value) == 'too many slice parts'


def pytest_funcarg__directive(request):
    state_machine = Mock()
    state_machine.get_source_and_line.return_value = (Mock(), Mock())
    return programoutput.ProgramOutputDirective(
        'program-output', ['some command'], {}, [], 1, 1, '',
        Mock(), state_machine)


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


def test_init_cache(app):
    assert not hasattr(app.env, 'programoutput_cache')
    programoutput.init_cache(app)
    assert hasattr(app.env, 'programoutput_cache')
    cache = app.env.programoutput_cache
    programoutput.init_cache(app)
    assert app.env.programoutput_cache is cache


def test_setup(app):
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
