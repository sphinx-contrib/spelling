#!/usr/bin/env python
"""Alternative integration of Sphinx and Paver.

To use this module, import it in your pavement.py file as 
``from sphinxcontrib import paverutils``,  then define 
option Bundles for "html" and/or "pdf" output using the options
described in the task help.

You can also develop your own tasks by calling ``run_sphinx()`` 
directly.
"""

__author__ = 'Doug Hellmann <doug.hellmann@gmail.com>'

from paver.easy import *
import sphinx


@task
def html(options):
    """Build HTML documentation using Sphinx. 
    
    This task uses the following options, searching first in the 
    "html" then "sphinx" section of the options.
    
    docroot
      the root under which Sphinx will be working.
      default: docs
    builddir
      directory under the docroot where the resulting files are put.
      default: build
    sourcedir
      directory under the docroot for the source files
      default: (empty string)
    doctrees
      the location of the cached doctrees
      default: $builddir/doctrees
    confdir
      the location of the sphinx conf.py
      default: $sourcedir
    outdir
      the location of the generated output files
      default: $builddir/$builder
    builder
      the name of the sphinx builder to use
      default: html
    template_args
      dictionary of values to be passed as name-value pairs to the HTML builder
      default: {}
    """
    run_sphinx(options, 'html')
    return


@task
def pdf(options):
    """Generate PDF output.
    
    Use Sphinx to produce LaTeX, then use external tools such as 
    TeXLive to convert the .tex file to a PDF.

    This task uses the following options, searching first in the 
    "pdf" then "sphinx" section of the options.

    docroot
      the root under which Sphinx will be working.
      default: docs
    builddir
      directory under the docroot where the resulting files are put.
      default: build
    sourcedir
      directory under the docroot for the source files
      default: (empty string)
    doctrees
      the location of the cached doctrees
      default: $builddir/doctrees
    confdir
      the location of the sphinx conf.py
      default: $sourcedir
    outdir
      the location of the generated output files
      default: $builddir/$builder
    builder
      the name of the sphinx builder to use
      default: pdf
    """
    run_sphinx(options, 'pdf')
    latex_dir = path(options.builddir) / 'latex'
    sh('cd %s; make' % latex_dir)
    return


def run_sphinx(options, *option_sets):
    """Helper function to run sphinx with common options.
    
    Pass the names of namespaces to be used in the search path
    for options.  The "sphinx" namespace is automatically added
    to the end of the list, so passing (options, 'html') causes
    the options to be configured with a search path of ('html', 'sphinx').
    This lets the caller invoke sphinx with different sets of
    options for different purposes.
    
    Supported options include:
    
    docroot
      the root under which Sphinx will be working.
      default: docs
    builddir
      directory under the docroot where the resulting files are put.
      default: build
    sourcedir
      directory under the docroot for the source files
      default: (empty string)
    doctrees
      the location of the cached doctrees
      default: $builddir/doctrees
    confdir
      the location of the sphinx conf.py
      default: $sourcedir
    outdir
      the location of the generated output files
      default: $builddir/$builder
    builder
      the name of the sphinx builder to use
      default: html
    template_args
      dictionary of values to be passed as name-value pairs to the HTML builder
      default: {}
    """
    if 'sphinx' not in option_sets:
        option_sets += ('sphinx',)
    kwds = dict(add_rest=False)
    
    # Set the search order of the options
    options.order(*option_sets, **kwds)
    
    paths = _get_paths(options)
    template_args = [ '-A%s=%s' % (name, value)
                      for (name, value) in getattr(options, 'template_args', {}).items() 
                      ]
    sphinxopts = ['', 
                  '-b', options.get('builder', 'html'), 
                  '-d', paths.doctrees, 
                  '-c', paths.confdir,
                  ]
    sphinxopts.extend(template_args)
    sphinxopts.extend([paths.srcdir, paths.outdir])
    dry("sphinx-build %s" % (" ".join(sphinxopts),), sphinx.main, sphinxopts)
    
    options.order()
    return


def _get_paths(options):
    """Retrieve and create the paths needed to run sphinx.
    
    Returns a Bundle with the required values filled in.
    """
    opts = options
    
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    
    builddir = docroot / opts.get("builddir", ".build")
    builddir.mkdir()
    
    srcdir = docroot / opts.get("sourcedir", "")
    if not srcdir.exists():
        raise BuildFailure("Sphinx source file dir (%s) does not exist" 
                            % srcdir)
    
    # Where is the sphinx conf.py file?
    confdir = path(opts.get('confdir', srcdir))
    
    # Where should output files be generated?
    outdir = opts.get('outdir', '')
    if outdir:
        outdir = path(outdir)
    else:
        outdir = builddir / opts.get('builder', 'html')
    outdir.mkdir()
    
    # Where are doctrees cached?
    doctrees = opts.get('doctrees', '')
    if not doctrees:
        doctrees = builddir / "doctrees"
    else:
        doctrees = path(doctrees)
    doctrees.mkdir()

    return Bunch(locals())
