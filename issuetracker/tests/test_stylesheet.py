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

"""
    test_stylesheet
    ===============

    Test application of the CSS stylesheet to the HTML output.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import pytest


sip = pytest.importorskip('sip')
# no need for clumsy QString->unicode conversions, lets do that automatically
sip.setapi('QString', 2)
QtCore = pytest.importorskip('PyQt4.QtCore')
QtGui = pytest.importorskip('PyQt4.QtGui')
QtWebKit = pytest.importorskip('PyQt4.QtWebKit')


# Qt application setup and rendering takes time, these tests are slow
pytestmark = pytest.mark.slow


def pytest_funcarg__app(request):
    """
    Application with mocked lookup.
    """
    request.applymarker(pytest.mark.mock_lookup)
    return request.getfuncargvalue('app')


def pytest_funcarg__qt_app(request):
    """
    A QApplication to drive rendering tests.
    """
    return request.cached_setup(lambda: QtGui.QApplication([]), scope='module')


def pytest_funcarg__web_page(request):
    """
    Return a web page object for the rendered ``content``.
    """
    request.getfuncargvalue('qt_app')
    # keep the web page alive during execution of the current test.  Prevents
    # the python GC from cleaning the web_page object at the end of this
    # function and thus prevents segfaults when accessing elements in the page.
    web_page = request.cached_setup(QtWebKit.QWebPage, scope='function')
    main_frame = web_page.mainFrame()
    index_html_file = request.getfuncargvalue('index_html_file')
    # wait for "loadFinished" signal to make sure that the whole content is
    # parsed before we run the test.  see
    # http://www.developer.nokia.com/Community/Wiki/How_to_wait_synchronously_for_a_Signal_in_Qt
    loop = QtCore.QEventLoop()
    main_frame.loadFinished.connect(loop.quit)
    main_frame.load(QtCore.QUrl(unicode(index_html_file)))
    loop.exec_()
    return web_page


def pytest_funcarg__reference(request):
    """
    Return the issue reference element in the ``main_frame``.
    """
    web_page = request.getfuncargvalue('web_page')
    issue_element = web_page.mainFrame().findFirstElement('.xref.issue')
    if issue_element.isNull():
        raise ValueError('null element')
    return issue_element


def pytest_funcarg__text_decoration(request):
    """
    Return the ``text-decoration`` style property of the ``reference`` element.
    """
    reference = request.getfuncargvalue('reference')
    resolve_strategy = QtWebKit.QWebElement.CascadedStyle
    return reference.styleProperty('text-decoration', resolve_strategy)


@pytest.mark.with_issue(id='10', title='Eggs', closed=False, url='eggs')
def test_open_issue(text_decoration):
    """
    Test that an open issue is not struck through.
    """
    assert not text_decoration


@pytest.mark.with_issue(id='10', title='Eggs', closed=True, url='eggs')
def test_closed_issue(text_decoration):
    """
    Test that a closed issue is struck through.
    """
    assert text_decoration == 'line-through'
