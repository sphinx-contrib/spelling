# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012, Sebastian Wiesner <lunaryorn@googlemail.com>
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

import pytest
from sphinx.errors import SphinxWarning
from docutils.nodes import literal_block, system_message

from sphinxcontrib.programoutput import Command


def assert_output(doctree, output):
    __tracebackhide__ = True
    literal = doctree.next_node(literal_block)
    assert literal
    assert literal.astext() == output


def assert_cache(app, cmd, output, use_shell=False,
                 hide_standard_error=False, returncode=0,
                 working_directory=None):
    cache = app.env.programoutput_cache
    working_directory = working_directory or app.srcdir
    working_directory = os.path.normpath(os.path.realpath(
        working_directory))
    cache_key = Command(cmd, use_shell, hide_standard_error,
                        working_directory)
    assert cache == {cache_key: (returncode, output)}


@pytest.mark.with_content('.. program-output:: echo eggs')
def test_simple(doctree, app):
    assert_output(doctree, 'eggs')
    assert_cache(app, 'echo eggs', 'eggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam with eggs")'""")
def test_with_spaces(doctree, app):
    """
    Test for command splitting with spaces involved.  Do *not* use ``echo`` for
    this test, because ``echo`` handles multiple arguments just as well as
    single arguments.
    """
    assert_output(doctree, 'spam with eggs')
    assert_cache(app, 'python -c \'print("spam with eggs")\'',
                 'spam with eggs')


@pytest.mark.with_content('.. program-output:: python -V')
def test_standard_error(doctree, app):
    output = 'Python {0}.{1}.{2}'.format(*sys.version_info)
    assert_output(doctree, output)
    assert_cache(app, 'python -V', output)


@pytest.mark.with_content("""\
.. program-output:: python -V
   :nostderr:""")
def test_standard_error_disabled(doctree, app):
    assert_output(doctree, '')
    assert_cache(app, 'python -V', '', hide_standard_error=True)


@pytest.mark.with_content("""\
.. program-output:: python -c 'import os; print(os.getcwd())'""")
def test_working_directory_defaults_to_srcdir(doctree, app, srcdir):
    output = str(srcdir.realpath())
    assert_output(doctree, output)
    assert_cache(app, "python -c 'import os; print(os.getcwd())'", output,
                 working_directory=str(srcdir))


@pytest.mark.with_content("""\
.. program-output:: python -c 'import os; print(os.getcwd())'
   :cwd: /""")
def test_working_directory_relative_to_srcdir(doctree, app, srcdir):
    output = str(srcdir.realpath())
    assert_output(doctree, output)
    assert_cache(app, "python -c 'import os; print(os.getcwd())'", output,
                 working_directory=str(srcdir))


@pytest.mark.with_content("""\
.. program-output:: python -c 'import os; print(os.getcwd())'
   :cwd: .""")
def test_working_directory_relative_to_document(doctree, app, srcdir):
    contentdir = srcdir.join('content')
    output = str(contentdir.realpath())
    assert_output(doctree, output)
    assert_cache(app, "python -c 'import os; print(os.getcwd())'", output,
                 working_directory=str(contentdir))


@pytest.mark.with_content("""\
.. program-output:: echo "${PWD}"
   :shell:
   :cwd: .""")
def test_working_directory_with_shell(doctree, app, srcdir):
    contentdir = srcdir.join('content')
    output = str(contentdir.realpath())
    assert_output(doctree, output)
    assert_cache(app, 'echo "${PWD}"', output, use_shell=True,
                 working_directory=str(contentdir))


@pytest.mark.with_content('.. program-output:: echo "${HOME}"')
def test_no_expansion_without_shell(doctree, app):
    assert_output(doctree, '${HOME}')
    assert_cache(app, 'echo "${HOME}"', '${HOME}')


@pytest.mark.with_content("""\
.. program-output:: echo "${HOME}"
   :shell:""")
def test_expansion_with_shell(doctree, app):
    assert_output(doctree, os.environ['HOME'])
    assert_cache(app, 'echo "${HOME}"', os.environ['HOME'], use_shell=True)


@pytest.mark.with_content("""\
.. program-output:: echo "spam with eggs"
   :prompt:""")
def test_prompt(doctree, app):
    assert_output(doctree, """\
$ echo "spam with eggs"
spam with eggs""")
    assert_cache(app, 'echo "spam with eggs"', 'spam with eggs')


@pytest.mark.with_content('.. command-output:: echo "spam with eggs"')
def test_command(doctree, app):
    assert_output(doctree, """\
$ echo "spam with eggs"
spam with eggs""")
    assert_cache(app, 'echo "spam with eggs"', 'spam with eggs')


@pytest.mark.with_content('.. command-output:: echo spam')
@pytest.mark.confoverrides(
    programoutput_prompt_template='>> {command}\n<< {output}')
def test_command_non_default_prompt(doctree, app):
    assert_output(doctree, '>> echo spam\n<< spam')
    assert_cache(app, 'echo spam', 'spam')


@pytest.mark.with_content("""\
.. program-output:: echo spam
   :extraargs: with eggs""")
def test_extraargs(doctree, app):
    assert_output(doctree, 'spam with eggs')
    assert_cache(app, 'echo spam with eggs', 'spam with eggs')


@pytest.mark.with_content('''\
.. program-output:: echo
   :shell:
   :extraargs: "${HOME}"''')
def test_extraargs_with_shell(doctree, app):
    assert_output(doctree, os.environ['HOME'])
    assert_cache(app, 'echo "${HOME}"', os.environ['HOME'], use_shell=True)


@pytest.mark.with_content("""\
.. program-output:: echo spam
   :prompt:
   :extraargs: with eggs""")
def test_extraargs_with_prompt(doctree, app):
    assert_output(doctree, '$ echo spam\nspam with eggs')
    assert_cache(app, 'echo spam with eggs', 'spam with eggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 2""")
def test_ellipsis_stop_only(doctree, app):
    assert_output(doctree, 'spam\nwith\n...')
    assert_cache(app, 'python -c \'print("spam\\nwith\\neggs")\'',
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: -2""")
def test_ellipsis_negative_stop(doctree, app):
    assert_output(doctree, 'spam\n...')
    assert_cache(app, """python -c 'print("spam\\nwith\\neggs")'""",
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 1, 2""")
def test_ellipsis_start_and_stop(doctree, app):
    assert_output(doctree, 'spam\n...\neggs')
    assert_cache(app, """python -c 'print("spam\\nwith\\neggs")'""",
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'print("spam\\nwith\\neggs")'
   :ellipsis: 1, -1""")
def test_ellipsis_start_and_negative_stop(doctree, app):
    assert_output(doctree, 'spam\n...\neggs')
    assert_cache(app, """python -c 'print("spam\\nwith\\neggs")'""",
                 'spam\nwith\neggs')


@pytest.mark.with_content("""\
.. program-output:: python -c 'import sys; sys.exit(1)'""")
def test_unexpected_return_code(app):
    with pytest.raises(SphinxWarning) as excinfo:
        app.build()
    exc_message = 'WARNING: Unexpected return code 1 from command {0!r}\n'.format(
        "python -c 'import sys; sys.exit(1)'")
    assert str(excinfo.value) == exc_message


@pytest.mark.with_content("""\
.. program-output:: python -c 'import sys; sys.exit(1)'
   :shell:""")
def test_shell_with_unexpected_return_code(app):
    with pytest.raises(SphinxWarning) as excinfo:
        app.build()
    exc_message = 'WARNING: Unexpected return code 1 from command {0!r}\n'.format(
        "python -c 'import sys; sys.exit(1)'")
    assert str(excinfo.value) == exc_message


@pytest.mark.with_content("""\
.. program-output:: python -c 'import sys; print("foo"); sys.exit(1)'
   :returncode: 1""")
def test_expected_non_zero_return_code(doctree, app):
    assert_output(doctree, 'foo')
    assert_cache(app, 'python -c \'import sys; print("foo"); sys.exit(1)\'',
                 'foo', returncode=1)


@pytest.mark.with_content("""\
.. command-output:: python -c 'import sys; sys.exit(1)'
   :returncode: 1""")
@pytest.mark.confoverrides(
    programoutput_prompt_template='> {command}\n{output}\n[{returncode}]>')
def test_prompt_with_return_code(doctree, app):
    assert_output(doctree, """\
> python -c 'import sys; sys.exit(1)'

[1]>""")
    assert_cache(app, "python -c 'import sys; sys.exit(1)'", '',
                 returncode=1)


@pytest.mark.with_content(".. program-output:: 'spam with eggs'")
@pytest.mark.ignore_warnings
def test_non_existing_executable(doctree, srcdir):
    # check that a proper error message appears in the document
    message = doctree.next_node(system_message)
    assert message
    srcfile = str(srcdir.join('content').join('doc.rst'))
    assert message['source'] == srcfile
    assert message['line'] == 4
    if sys.version_info[0] < 3:
        msgtemplate = ("{0}:4: (ERROR/3) Command {1!r} failed: "
                       "[Errno 2] No such file or directory")
    else:
        msgtemplate = ("{0}:4: (ERROR/3) Command {1!r} failed: "
                       "[Errno 2] No such file or directory: {1}")
    assert message.astext() == msgtemplate.format(srcfile, "'spam with eggs'")


@pytest.mark.with_content("""\
.. program-output:: echo spam
   :cwd: ./subdir""")
@pytest.mark.ignore_warnings
def test_non_existing_working_directry(doctree, srcdir):
    # check that a proper error message appears in the document
    message = doctree.next_node(system_message)
    assert message
    srcfile = str(srcdir.join('content').join('doc.rst'))
    assert message['source'] == srcfile
    assert message['line'] == 4
    msgtemplate = ("{0}:4: (ERROR/3) Command {1!r} failed: "
                   "[Errno 2] No such file or directory: {2!r}")
    if sys.version_info[0] < 3:
        filename = srcdir.join('content').realpath().join('subdir')
    else:
        # Python 3 breaks the error message here :(
        filename = 'echo'
    msg = msgtemplate.format(srcfile, 'echo spam', str(filename))
    assert message.astext() == msg
