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
import textwrap

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
    options.order('pdf')
    paths = _get_paths(options)
    latex_dir = paths.builddir / options.builder
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
    
    paths = _get_and_create_paths(options)
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

def _get_and_create_paths(options):
    """Retrieves and creates paths needed to run sphinx.

    Returns a Bundle with the required values filled in.
    """
    paths = _get_paths(options)
    paths.builddir.mkdir()
    paths.outdir.mkdir()
    paths.doctrees.mkdir()
    return paths

def _get_paths(options):
    """Retrieves paths needed to run sphinx.
    
    Returns a Bundle with the required values filled in.
    """
    opts = options
    
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    
    builddir = docroot / opts.get("builddir", ".build")
    
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
    
    # Where are doctrees cached?
    doctrees = opts.get('doctrees', '')
    if not doctrees:
        doctrees = builddir / "doctrees"
    else:
        doctrees = path(doctrees)

    return Bunch(locals())


def adjust_line_widths(lines, break_lines_at, line_break_mode):
    broken_lines = []
    for l in lines:
        # apparently blank line
        if not l.strip() or len(l) <= break_lines_at:
            broken_lines.append(l)
            continue

        if line_break_mode == 'break':
            while l:
                part, l = l[:break_lines_at], l[break_lines_at:]
                broken_lines.append(part)

        elif line_break_mode == 'wrap':
            broken_lines.extend( textwrap.fill(l, width=break_lines_at).splitlines() )

        elif line_break_mode == 'fill':
            prefix = l[:len(l)-len(l.lstrip())]
            broken_lines.extend( textwrap.fill(l, width=break_lines_at,
                                               subsequent_indent=prefix).splitlines() )

        elif line_break_mode == 'continue':
            while l:
                part, l = l[:break_lines_at], l[break_lines_at:]
                if l:
                    part = part + '\\'
                broken_lines.append(part)

        elif line_break_mode == 'truncate':
            broken_lines.append( l[:break_lines_at] )

        else:
            raise ValueError('Unrecognized line_break_mode "%s"' % line_break_mode)

    return broken_lines
    


def run_script(input_file, script_name, 
               interpreter='python',
               include_prefix=True, 
               ignore_error=False, 
               trailing_newlines=True,
               break_lines_at=0,
               line_break_mode='break',
               ):
    """Run a script in the context of the input_file's directory, 
    return the text output formatted to be included as an rst
    literal text block.
    
    Arguments:
    
     input_file
       The name of the file being processed by cog.  Usually passed as cog.inFile.
     
     script_name
       The name of the Python script living in the same directory as input_file to be run.
       If not using an interpreter, this can be a complete command line.  If using an
       alternate interpreter, it can be some other type of file.
     
     include_prefix=True
       Boolean controlling whether the :: prefix is included.
     
     ignore_error=False
       Boolean controlling whether errors are ignored.  If not ignored, the error
       is printed to stdout and then the command is run *again* with errors ignored
       so that the output ends up in the cogged file.
     
     trailing_newlines=True
       Boolean controlling whether the trailing newlines are added to the output.
       If False, the output is passed to rstrip() then one newline is added.  If
       True, newlines are added to the output until it ends in 2.

     break_lines_at=0
       Integer indicating the length where lines should be broken and
       continued on the next line.  Defaults to 0, meaning no special
       handling should be done.

     line_break_mode='break'
       Name of mode to break lines.

         break
           Insert a hard break
         continue
           Insert a hard break with a backslash
         wrap
           Use textwrap.fill() to wrap
       
    """
    rundir = path(input_file).dirname()
    if interpreter:
        cmd = '%(interpreter)s %(script_name)s' % vars()
    else:
        cmd = script_name
    real_cmd = 'cd %(rundir)s; %(cmd)s 2>&1' % vars()
    try:
        output_text = sh(real_cmd, capture=True, ignore_error=ignore_error)
    except Exception, err:
        print '*' * 50
        print 'ERROR run_script(%s) => %s' % (real_cmd, err)
        print '*' * 50
        output_text = sh(real_cmd, capture=True, ignore_error=True)
        print output_text
        print '*' * 50
        if not ignore_error:
            raise
    if include_prefix:
        response = '\n::\n\n'
    else:
        response = ''
#     response += '\t$ %(cmd)s\n\n\t' % vars()

    command_line = adjust_line_widths(['\t$ %s' % cmd],
                                      break_lines_at - 1 if break_lines_at else 73,
                                      'continue')
        
    lines = []
    lines.extend(command_line)
    lines.append('') # a blank line
    lines.extend(output_text.splitlines()) # the output

    # Deal with lines that might be too long
    if break_lines_at:
        lines = adjust_line_widths(lines, break_lines_at, line_break_mode)
                
    response += '\n\t'.join(lines)
    if trailing_newlines:
        while not response.endswith('\n\n'):
            response += '\n'
    else:
        response = response.rstrip()
        response += '\n'
    return response

# Stuff commonly used symbols into the builtins so we don't have to
# import them in all of the cog blocks where we want to use them.
__builtins__['run_script'] = run_script
#__builtins__['sh'] = sh
