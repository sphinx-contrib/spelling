==========
Exceltable
==========
Module ``sphinxcontrib.exceltable`` is an extension for Sphinx_, that adds support for including spreadsheets, or part
of them, into Sphinx document.

This is document describes :ref:`how to install <setup>`, :ref:`use <usage>` and :ref:`contribute to the development <devel>` of
the :mod:`sphinxcontrib.exceltable` module.

.. contents::
   :local:

.. _setup:

Setup
=====
Here you can find the minimum steps for installation and usage of the module:

#. Install module along with its dependencies using `pip`, as follows. Alternatively, download the package and
   install it manually with command ``python setup.py install``::

     pip install sphinxcontrib.exceltable

   .. NOTE:: Module depends on Sphinx_ and xlrd_ which are installed automatically.

#. Start new Sphinx powered documentation project (unless you already have one)::

     sphinx-quickstart

#. Configure directive of your choice into Sphinx :file:`conf.py`
   configuration file.

   .. code-block:: python

     # Add ``sphinxcontrib.exceltable`` into extension list
     extensions = ['sphinxcontrib.exceltable']

#. Place directive/role in your document (:ref:`see usage -section <usage>` for :ref:`options <option>`
   and :ref:`examples <example>`):

   .. code-block:: rst

      My document
      ===========
      The contents of the setup script:

    .. exceltable:: Table caption
       :file: path/to/document.xls
       :header: 1
       :selection: A1:B3

   .. NOTE::

      Some notes about the parameters (see :ref:`options <option>` for full description):

      - file: path to excel document, relative to the document where where it is being defined.
      - header: whether first line in spreadsheet should be considered as table header
      - selection: cells to include in the table

#. Build the document::

     sphinx-build -b html doc dist/html

#. That's it!

.. _usage:

Usage
=====
This section gives some further information about all the possibilities of the module.

.. contents::
   :local:


.. _option:

Options
-------
Define ``exceltable`` -directive into your document. The path to document is
given with ``file`` option, and it is relative to RST -document path.
The directive argument is reserved for the optional table caption.

.. code-block:: rst

    Show part of the excel -document as a table within document:

    .. exceltable:: caption
       :file: path/to/document.xls
       :header: 1
       :selection: A1:B2
       :sheet: 1


    See further information about the possible parameters from documentation.

Following options and arguments are available. Directive has no content:

**caption** (optional argument)
  Optional table can be provided next to directive definition.
  If caption is not provided, no caption is set for the table.

  .. code-block:: rst

     .. exceltable:: Caption for the table
        :file: document.xls

**file** (required)
  Relative path (based on document) to excel -document. Compulsory option.
  Use forward slash also in Windows environments.

  .. code-block:: rst

     .. exceltable::
        :file: path/to/document.xls

**selection** (optional)
  Selection defines from and to the selection reaches. If value is not defined,
  the whole data from sheet is taken into table. Following definitons are supported:

  * Complete name selection: ``A1:B2``
  * Starting name selection: ``C4:``
  * Ending name selection: ``:C4`` (selecting all the cells til ``C4``)
  * Numeric selection: ``0,0:2,2`` (indexing start from 0 and first value denotes
    the column, next row)

  .. NOTE::

     * If the selection is bigger than the actual data, the biggest
       possible field (row and/or column) is taken
     * On the numeric selection, the order of values is: ``colindex,rowindex``,
       making the complete selection to be::

         start-c-indx,start-r-indx:end-c-indx,end-r-indx

**sheet** (optional)
  Defines the *name* or *index number* of the sheet. The index value is numeric
  and it starts from zero (0). The first sheet is also the default value if option
  is not defined. Examples:

  .. code-block:: rest

     .. exceltable::
        :file: document.xls
        :sheet: SheetName

     .. exceltable::
        :file: document.xls
        :sheet: 0

**header** (optional)
  Header option can used either for providing the header fields:

  .. code-block:: rest

     .. exceltable::
        :header: Name1, Name2, Name3
        :file: document.xls

  or as a numeric value, it defines the *number of rows* considerer header fields
  in the data:

  .. code-block:: rest

     .. exceltable::
        :header: 1
        :file: document.xls

  The default value is ``0``, meaning no header is generated/considered to be
  found from data

**widths**
  By default, the column widths are taken from the content (excel sheet): Directive
  counts relative sizes for the columns. However, it is also possible to define
  custom widths for the table:

  .. code-block:: rest

     .. exceltable:: Automatic column widths
        :file: document.xls
        :header: A,B,C

  .. code-block:: rest

     .. exceltable:: Manual column widths
        :file: document.xls
        :header: A,B,C
        :widths: 20,20,60

  .. NOTE::

     When defining the widths manually, remember following:

     * Separate the widths with comma (``,``)
     * The number of width values must match with the columns
     * The sum of the widths should be: 100


.. _example:

Examples
--------
This section shows few examples how the directive can be used and what are the
options with it. For a reference, :download:`see source Excel -document used with the
examples <example/cartoons.xls>`.

Directive definition:

  .. code-block:: rest

    .. exceltable:: Cartoon listing
       :file: example/cartoons.xls
       :header: 1

Output of the processed document:

  .. exceltable:: Cartoon listing
     :file: example/cartoons.xls
     :header: 1

Selection can be limited using ``selection`` option, we can take the sub-set of the data:

  .. code-block:: rest

    .. exceltable:: Cartoon listing (subset)
       :file: example/cartoons.xls
       :header: 1
       :selection: A1:B3

    .. exceltable:: Only entry dates
       :file: example/cartoons.xls
       :header: 1
       :selection: D1:


Output of the processed document:

  .. exceltable:: Cartoon listing
     :file: example/cartoons.xls
     :header: 1
     :selection: A1:B3

  .. exceltable:: Only entry dates
     :file: example/cartoons.xls
     :header: 1
     :selection: D1:

The sheet can be selected by using ``sheet`` -option. The value can be either
the *name of the sheet* or the *numeric index of the sheet*, starting from zero
(0,1,2...):

  .. code-block:: rest

    .. exceltable:: Sheet example
       :file: example/cartoons.xls
       :sheet: 1
       :selection: B2:C3

Output of the processed document:

  .. exceltable:: Sheet example
     :file: example/cartoons.xls
     :sheet: 1
     :selection: B2:C3


Index
=====

.. toctree::
   :maxdepth: 2
   :numbered:

   devel
   changelog
   glossary

.. toctree::
   :hidden:

   global

