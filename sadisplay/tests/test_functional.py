# -*- coding: utf-8 -*-
import os
import tempfile
import shutil
import glob
from sphinx.application import Sphinx

_fixturedir = os.path.join(os.path.dirname(__file__), 'fixture')
_fakecmd = os.path.join(os.path.dirname(__file__), 'fakecmd.py')

_tempdir = _srcdir = _outdir = None


def setup():
    global _tempdir, _srcdir, _outdir
    _tempdir = tempfile.mkdtemp()
    _srcdir = os.path.join(_tempdir, 'src')
    _outdir = os.path.join(_tempdir, 'out')
    os.mkdir(_srcdir)


def teardown():
    shutil.rmtree(_tempdir)


def readfile(fname):
    f = open(os.path.join(_outdir, fname), 'rb')
    try:
        return f.read()
    finally:
        f.close()


def runsphinx(text, builder, confoverrides):
    f = open(os.path.join(_srcdir, 'index.rst'), 'w')
    try:
        f.write(text.encode('utf-8'))
    finally:
        f.close()
    app = Sphinx(_srcdir, _fixturedir, _outdir, _outdir, builder,
                 confoverrides)
    app.build()


def with_runsphinx(builder, confoverrides={'plantuml': _fakecmd}):
    def wrapfunc(func):
        def test():
            src = '\n'.join(l[4:] for l in func.__doc__.splitlines()[2:])
            os.mkdir(_outdir)
            try:
                runsphinx(src, builder, confoverrides)
                func()
            finally:
                os.unlink(os.path.join(_srcdir, 'index.rst'))
                shutil.rmtree(_outdir)
        test.func_name = func.func_name
        return test
    return wrapfunc


@with_runsphinx('html')
def test_buildhtml_simple():
    """Generate simple HTML

    .. sadisplay::
        :module: model
    """

    files = glob.glob(os.path.join(_outdir, '_images', 'plantuml-*.png'))
    assert len(files) == 1
    assert '<img src="_images/plantuml' in readfile('index.html')

    content = readfile(files[0])
    assert u'Admin' in content
    assert u'User' in content
    assert u'Address' in content


@with_runsphinx('html')
def test_buildhtml_as_link():
    """Generate simple HTML with link

    .. sadisplay::
        :module: model
        :link:
    """

    files = glob.glob(os.path.join(_outdir, '_images', 'plantuml-*.png'))
    assert len(files) == 1
    assert '<a href="_images/plantuml' in readfile('index.html')

    content = readfile(files[0])
    assert u'Admin' in content
    assert u'User' in content
    assert u'Address' in content


@with_runsphinx('latex')
def test_buildlatex_simple():
    """Generate simple LaTeX

    .. sadisplay::
       :module: model
       :exclude: Admin
    """
    files = glob.glob(os.path.join(_outdir, 'plantuml-*.png'))
    assert len(files) == 1
    assert r'\includegraphics{plantuml-' in \
            readfile('plantuml_fixture.tex')

    content = readfile(files[0])
    assert u'Admin' not in content
    assert u'User' in content
    assert u'Address' in content
