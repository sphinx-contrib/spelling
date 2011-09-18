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

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import os
import sys
from subprocess import CalledProcessError

import pytest
from docutils.nodes import literal_block


def assert_output(doctree, output):
    __tracebackhide__ = True
    literal = doctree.next_node(literal_block)
    assert literal
    assert literal.astext() == output


def assert_cache(cache, cmd, output, use_shell=False,
                 hide_standard_error=False):
    if isinstance(cmd, list):
        cmd = tuple(cmd)
    cache_key = (cmd, use_shell, hide_standard_error)
    assert cache[cache_key] == output


@pytest.mark.with_content('.. program-output:: echo eggs')
def test_simple(doctree, cache):
    assert_output(doctree, 'eggs')
    assert_cache(cache, ['echo', 'eggs'], 'eggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam with eggs")'""")
def test_with_spaces(doctree, cache):
    """
    Test for command splitting with spaces involved.  Do *not* use ``echo`` for
    this test, because ``echo`` handles multiple arguments just as well as
    single arguments.
    """
    assert_output(doctree, 'spam with eggs')
    assert_cache(cache, ['python', '-c', 'print("spam with eggs")'],
                 'spam with eggs')


@pytest.mark.with_content('.. program-output:: python -V')
def test_standard_error(doctree, cache):
    output = 'Python {0}.{1}.{2}'.format(*sys.version_info)
    assert_output(doctree, output)
    assert_cache(cache, ['python', '-V'], output)


@pytest.mark.with_content("""\
.. program-output:: python -V
   :nostderr:""")
def test_standard_error_disabled(doctree, cache):
    assert_output(doctree, '')
    assert_cache(cache, ['python', '-V'], '', hide_standard_error=True)


@pytest.mark.with_content('.. program-output:: echo "${VIRTUAL_ENV}"')
def test_no_expansion_without_shell(doctree, cache):
    assert_output(doctree, '${VIRTUAL_ENV}')
    assert_cache(cache, ['echo', '${VIRTUAL_ENV}'], '${VIRTUAL_ENV}')


@pytest.mark.with_content("""\
.. program-output:: echo "${VIRTUAL_ENV}"
   :shell:""")
def test_expansion_with_shell(doctree, cache):
    assert_output(doctree, os.environ['VIRTUAL_ENV'])
    assert_cache(cache, 'echo ${VIRTUAL_ENV}', os.environ['VIRTUAL_ENV'],
                 use_shell=True)


@pytest.mark.with_content("""\
.. program-output:: echo "spam with eggs"
   :prompt:""")
def test_prompt(doctree, cache):
    assert_output(doctree, """\
$ echo "spam with eggs"
spam with eggs""")
    assert_cache(cache, ['echo', 'spam with eggs'], 'spam with eggs')


@pytest.mark.with_content('.. command-output:: echo "spam with eggs"')
def test_command(doctree, cache):
    assert_output(doctree, """\
$ echo "spam with eggs"
spam with eggs""")
    assert_cache(cache, ['echo', 'spam with eggs'], 'spam with eggs')


@pytest.mark.with_content('.. command-output:: echo spam')
@pytest.mark.confoverrides(programoutput_prompt_template='>> %(command)s\n<< %(output)s')
def test_command_non_default_prompt(doctree, cache):
    assert_output(doctree, '>> echo spam\n<< spam')
    assert_cache(cache, ['echo', 'spam'], 'spam')


@pytest.mark.with_content("""\
.. program-output:: echo spam
   :extraargs: with eggs""")
def test_extraargs(doctree, cache):
    assert_output(doctree, 'spam with eggs')
    assert_cache(cache, ['echo', 'spam', 'with', 'eggs'], 'spam with eggs')


@pytest.mark.with_content('''\
.. program-output:: echo
   :shell:
   :extraargs: "${VIRTUAL_ENV}"''')
def test_extraargs_with_shell(doctree, cache):
    assert_output(doctree, os.environ['VIRTUAL_ENV'])
    assert_cache(cache, 'echo "${VIRTUAL_ENV}"', os.environ['VIRTUAL_ENV'],
                 use_shell=True)


@pytest.mark.with_content("""\
.. program-output:: echo spam
   :prompt:
   :extraargs: with eggs""")
def test_extraargs_with_prompt(doctree, cache):
    assert_output(doctree, '$ echo spam\nspam with eggs')
    assert_cache(cache, ['echo', 'spam', 'with', 'eggs'], 'spam with eggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 2""")
def test_ellipsis_stop_only(doctree, cache):
    assert_output(doctree, 'spam\nwith\n...')
    assert_cache(cache, ['python', '-c', r'print("spam\nwith\neggs")'],
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: -2""")
def test_ellipsis_negative_stop(doctree, cache):
    assert_output(doctree, 'spam\n...')
    assert_cache(cache, ['python', '-c', r'print("spam\nwith\neggs")'],
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 1, 2""")
def test_ellipsis_start_and_stop(doctree, cache):
    assert_output(doctree, 'spam\n...\neggs')
    assert_cache(cache, ['python', '-c', r'print("spam\nwith\neggs")'],
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 1, -1""")
def test_ellipsis_start_and_negative_stop(doctree, cache):
    assert_output(doctree, 'spam\n...\neggs')
    assert_cache(cache, ['python', '-c', r'print("spam\nwith\neggs")'],
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'import sys; sys.exit(1)'""")
def test_non_zero_return_code(app):
    with pytest.raises(CalledProcessError) as excinfo:
        app.build()
    exc = excinfo.value
    assert exc.cmd == ('python', '-c', 'import sys; sys.exit(1)')
    assert exc.returncode == 1


@pytest.mark.with_content("""\
.. program-output:: python -c 'import sys; sys.exit(1)'
   :shell:""")
def test_shell_non_zero_return_code(app):
    with pytest.raises(CalledProcessError) as excinfo:
        app.build()
    exc = excinfo.value
    assert exc.cmd == "python -c 'import sys; sys.exit(1)'"
    assert exc.returncode == 1
