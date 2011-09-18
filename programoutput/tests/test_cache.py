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

import pytest

from sphinxcontrib.programoutput import ProgramOutputCache, Command


def pytest_funcarg__cache(request): # pylint: disable=W0613
    return ProgramOutputCache()


def assert_cache(cache, cmd, output, returncode=0):
    result = (returncode, output)
    assert not cache
    assert cache[cmd] == result
    assert cache == {cmd: result}


def test_simple(cache):
    assert_cache(cache, Command(['echo', 'spam']), 'spam')


def test_shell(cache):
    assert_cache(cache, Command('echo spam', shell=True), 'spam')


def test_hidden_standard_error(cache):
    cmd = ['python', '-c', 'import sys; sys.stderr.write("spam")']
    assert_cache(cache, Command(cmd, hide_standard_error=True), '')


def test_nonzero_return_code(cache):
    cmd = ['python', '-c', 'import sys; sys.exit(1)']
    assert_cache(cache, Command(cmd), '', returncode=1)


def test_nonzero_return_code_shell(cache):
    cmd = "python -c 'import sys; sys.exit(1)'"
    assert_cache(cache, Command(cmd, shell=True), '', returncode=1)


@pytest.mark.with_content('dummy content')
def test_cache_pickled(app, doctreedir):
    cmd = Command(['echo', 'spam'])
    result = (0, 'spam')
    assert app.env.programoutput_cache[cmd] == result
    app.build()
    pickled_env = doctreedir.join('environment.pickle').load()
    assert pickled_env.programoutput_cache == {cmd: result}
