.. default-domain:: rst
.. highlight:: rest

:py:mod:`sphinxcontrib.programoutput` -- Include program output
==================================================================

.. py:module:: sphinxcontrib.programoutput
   :synopsis:  Include the output of programs into documents

This extension for Sphinx_ 1.0 allows to run programs during the build
process, including their output into the documentation.  It supports the
:py:mod:`sphinxcontrib.ansi` extension to turn colored output of programs in
pretty-formatted HTML.

The extension is available under the terms of the BSD license, see LICENSE_
for more information.


Installation
------------

This extension can be installed from the Python Package Index::

   pip install sphinxcontrib-programoutput

Alternatively, you can clone the sphinx-contrib_ repository from BitBucket,
and install the extension directly from the repository::

   hg clone http://bitbucket.org/birkenfeld/sphinx-contrib
   cd sphinx-contrib/programoutput
   python setup.py install


Usage
-----

The main directive is :dir:`program-output`:

.. directive:: program-output

   This directive accepts a single string as argument, which is the command
   to execute.  By default, this command string is split using the
   :py:mod:`shlex` modules, which mostly works like common Unix shells like
   ``bash`` or ``zsh``::

      .. program-output:: python -V

   The above snippet would render like this:

   .. program-output:: python -V

   However, special shell features like parameter expansion are not
   supported::

      .. program-output:: echo "$USER"

   .. program-output:: echo "$USER"

   To enable such shell features, use option ``shell``.  If this option is
   given, the command string is executed using ``/bin/sh -c``::

      .. program-output:: echo "$USER"
         :shell:

   .. program-output:: echo "$USER"
      :shell:

   By default, both standard output *and* standard error are captured and
   included in the document.  Use option ``nostderr`` to hide anything from
   the standard error stream of the invoked program.

   Using the option ``prompt`` you can include the command, that produced
   the output.  The result will mimic input on a shell prompt with the
   resulting output::

      .. program-output:: python -V
         :prompt:

   .. program-output:: python -V
      :prompt:

   The prompt can be configured using
   :confval:`programoutput_prompt_template`.  The directive
   :dir:`command-output` provides a convenient shortcut to this directive
   with ``prompt``.

   Sometimes the program may require options, you may not want to include in
   the prompt.  You can use the ``extraargs`` option for this purpose.  The
   value of this options is parsed just like the command itself, and
   afterwards appended to the command.  It will however never appear in the
   output, if ``prompt`` is specified.

   Lengthy output can be shortened using the ``ellipsis`` option.  This
   option accepts at most two comma-separated integers, which refer to lines
   in the output.  If the second integer is missing, it refers to the last
   line.  Everything in between these lines is replaced by a single ellipsis
   ``...``::

      .. program-output::  python --help
         :prompt:
         :ellipsis: 2

   .. program-output::  python --help
      :prompt:
      :ellipsis: 2

   Negative line numbers are counted from the last-line.  Thus specifying
   ``:ellipsis:  2, -2`` will remove anything except the first two and the
   last two lines::

      .. program-output::  python --help
         :prompt:
         :shell:
         :ellipsis: 2, -2

   .. program-output::  python --help
      :prompt:
      :shell:
      :ellipsis: 2, -2


.. directive:: command-output

   Just like :dir:`program-output`, but with ``prompt`` enabled.


Configuration
^^^^^^^^^^^^^

This extension understands the following configuration options:

.. confval:: programoutput_prompt_template

   A string with a template for the output of :dir:`command-output` and also
   :dir:`program-output`, if the option ``prompt`` is given.  The default value
   is ``'$ %(command)s\n%(output)s'``.  The key ``command`` is replaced with
   the command, the key ``output`` with the output of this command.

.. confval:: programoutput_use_ansi

   If ``True``, ANSI colour sequences in program output are interpreted.  To
   use this feature, the extension :py:mod:`sphinxcontrib.ansi` must be enabled
   and configured.  If missing or ``False``, these sequences are not
   interpreted, but appear in documentation unchanged.

Contribution
------------

Please contact the author or create an issue in the `issue tracker`_ of the
sphinx-contrib_ repository, if you have found any bugs or miss some
functionality (e.g. integration of some other issue tracker).  Patches are
welcome!


.. toctree::
   :maxdepth: 2
   :hidden:

   changes.rst


.. _`Sphinx`: http://sphinx.pocoo.org/
.. _`sphinx-contrib`: http://bitbucket.org/birkenfeld/sphinx-contrib
.. _`issue tracker`: http://bitbucket.org/birkenfeld/sphinx-contrib/issues
.. _LICENSE: http://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/LICENSE
