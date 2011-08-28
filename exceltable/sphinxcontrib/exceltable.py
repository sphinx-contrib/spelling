# -*- coding: utf-8 -*-
"""

:class:`XMLTableDirective` implements the ``exceltable`` -directive.

"""
__docformat__ = 'restructuredtext'
__author__ = 'Juha Mustonen'
__version__ = '1.0'

import os
import sys
import doctest
import re
import types
import logging
from datetime import datetime

# Import required docutils modules
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.tables import ListTable
from docutils import io, nodes, statemachine, utils, frontend
from docutils.utils import SystemMessagePropagation, Reporter

import sphinx

# Uses excelent module xlrd for reading Excel sheets
# Retrieve it from http://www.python-excel.org/
import xlrd

class Messenger(Reporter):
  def __init__(self, src='sphinxcontrib.xyz'):
    settings = frontend.OptionParser().get_default_values()

    settings.report_level = 1

    Reporter.__init__(self,
      src,
      settings.report_level,
      settings.halt_level,
      stream=settings.warning_stream,
      debug=settings.debug,
      encoding=settings.error_encoding,
      error_handler=settings.error_encoding_error_handler
    )

    self.log = logging.getLogger(src)

  def debug(self, *msgs):
    #return super(Messenger, self).debug(msg)
    pass

  def info(self, *msgs):
    #return super(Messenger, self).info(msg)
    pass

  def warning(self, *msgs):
    #super(Messenger, self).warning(msg)
    return literal_block(text=self._prepare(msgs))

  def error(self, *msgs):
    #super(Messenger, self).error(msg)
    text = self._prepare(msgs)
    #self.log.error(text)
    return literal_block(text=text)

  def _prepare(self, *msgs):
    return ' '.join([unicode(msg) for msg in msgs])


class DirectiveTemplate(Directive):
  """
  Template intended for directive development, providing
  few handy functions
  """

  def _get_directive_path(self, path):
    """
    Returns transformed path from the directive
    option/content
    """

    print 'org path: %s' % path

    source = self.state_machine.input_lines.source(
      self.lineno - self.state_machine.input_offset - 1)
    source_dir = os.path.dirname(os.path.abspath(source))
    path = os.path.normpath(os.path.join(source_dir, path))

    print 'chg path: %s' % path

    return utils.relative_path(None, path)



class ExcelTableDirective(ListTable, DirectiveTemplate):
  """
  ExcelTableDirective implements the directive.
  Directive allows to create RST tables from the contents
  of the Excel sheet. The functionality is very similar to
  csv-table (docutils) and xmltable (:mod:`sphinxcontrib.xmltable`).

  Example of the directive:

  .. code-block:: rest

    .. exceltable::
       :file: path/to/document.xls
       :header: 1

  """
  #required_arguments = 0
  #optional_arguments = 0
  has_content = False
  option_spec = {
    'file': directives.path,
    'selection': directives.unchanged_required,
    'encoding': directives.unchanged,
    'header': directives.unchanged,
    'sheet': directives.unchanged,
    'class': directives.class_option,
    'widths': directives.unchanged,
  }

  def run(self):
    """
    Implements the directive
    """
    # Get content and options
    file_path = self.options.get('file', None)
    selection = self.options.get('selection', 'A1:')
    sheet = self.options.get('sheet', '0')
    header = self.options.get('header', '0')
    col_widths = self.options.get('widths', None)

    # Divide the selection into from and to values
    if u':' not in selection:
      selection += ':'
    fromcell, tocell = selection.split(':')

    if not fromcell:
      fromcell = 'A1'

    if not tocell:
      tocell = None

    #print selection, fromcell, tocell

    if not file_path:
      return [self._report('file_path -option missing')]

    # Header option
    header_rows = 0
    if header and header.isdigit():
      header_rows = int(header)

    # Transform the path suitable for processing
    file_path = self._get_directive_path(file_path)

    print 'file path: %s' % file_path

    try:
      et = ExcelTable(open(file_path))
      table = et.create_table(fromcell=fromcell, tocell=tocell,
        nheader=header_rows, sheet=sheet)
    except Exception, e:
      return [msgr.error('Error occured while creating table: %s' % e)]
      pass

    #print table

    title, messages = self.make_title()
    #node = nodes.Element() # anonymous container for parsing
    #self.state.nested_parse(self.content, self.content_offset, node)

    # If empty table is created
    if not table:
      self._report('The table generated from queries is empty')
      return [nodes.paragraph(text='')]

    try:
      table_data = []

      # If there is header defined, set the header-rows param and
      # append the data in row =>. build_table_from_list handles the header generation
      if header and not header.isdigit():

        # Otherwise expect the header to be string with column names defined in
        # it, separating the values with comma
        header_rows = 1
        table_data.append([nodes.paragraph(text=hcell.strip()) for hcell in header.split(',')])

      # Put the given data in rst elements: paragraph
      for row in table['headers']:
        table_data.append([nodes.paragraph(text=cell['value']) for cell in row])

      # Iterates rows: put the given data in rst elements
      for row in table['rows']:
        row_data = []
        for cell in row:
          class_data = ['']
          # Node based on formatting rules
          # NOTE: rst does not support nested, use class attribute instead

          if cell['italic']:
            class_data.append('italic')

          if cell['bold']:
            node = nodes.strong(text=cell['value'])
          else:
            node = nodes.paragraph(text=cell['value'])

          # Add additional formatting as class attributes
          node['classes'] = class_data
          row_data.append([node])

          # FIXME: style attribute does not get into writer
          if cell['bgcolor']:
            rgb = [str(val) for val in cell['bgcolor']]
            node.attributes['style'] = 'background-color: rgb(%s);' % ','.join(rgb)

          #print node

        table_data.append(row_data)

      # If there is no data at this point, throw an error
      if not table_data:
        return [msgr.error('Selection did not return any data')]

      # Get params from data
      num_cols = len(table_data[0])

      # Get the widths for the columns:
      # 1. Use provided info, if available
      # 2. Use widths from the excelsheet
      # 3. Use default widths (equal to all)
      #
      # Get content widths from the first row of the table
      # if it fails, calculate default column widths
      if col_widths:
        col_widths = [int(width) for width in col_widths.split(',')]
      else:
        col_widths = [int(col['width']) for col in table['rows'][0]]
        col_width_total = sum(col_widths)
        col_widths = [int(width * 100/ col_width_total) for width in col_widths]

      # If still empty for some reason, use default widths
      if not col_widths:
        col_widths = self.get_column_widths(num_cols)

      stub_columns = 0

      # Sanity checks

      # Different amount of cells in first and second row (possibly header and 1 row)
      if type(header) is not int:
        if len(table_data) > 1 and len(table_data[0]) != len(table_data[1]):
          error = msgr.error('Data amount mismatch: check the directive data and params')
          return [error]

      self.check_table_dimensions(table_data, header_rows, stub_columns)

    except SystemMessagePropagation, detail:
        return [detail.args[0]]

    # Generate the table node from the given list of elements
    table_node = self.build_table_from_list(
      table_data, col_widths, header_rows, stub_columns)

    # Optional class parameter
    table_node['classes'] += self.options.get('class', [])

    if title:
      table_node.insert(0, title)

    #print table_node

    return [table_node] + messages

# TODO: Move away
msgr = Messenger('sphinxcontrib.exceltable')

class ExcelTable(object):
  """
  Class generates the list based table from
  the given excel-document, suitable for the directive.

  Class also implements the custom query format,
  is to use for the directive.::

    >>> import os
    >>> from sphinxcontrib import exceltable
    >>>
    >>> fo = open(os.path.join(os.path.dirname(exceltable.__file__),'../doc/example/cartoons.xls'), 'r+b')
    >>> et = exceltable.ExcelTable(fo)
    >>>
    >>> table = et.create_table(fromcell='A1', tocell='C4')
    >>> assert et.fromcell == (0, 0)
    >>> assert et.tocell == (2,3)
    >>>
    >>> table = et.create_table(fromcell='B10', tocell='B11', sheet='big')
    >>> assert et.fromcell == (1,9)
    >>> assert et.tocell == (1,10)

  """
  def __init__(self, fobj, encoding='utf-8'):
    """
    """
    assert type(fobj) is file, u'File object type expected, %s given' % type(fobj)

    self.file_object = fobj
    self.fromcell = (0, 0)
    self.tocell = (0, 0)

    # xlrd uses paths only
    # TODO: Add support for remote files
    self.book = xlrd.open_workbook(self.file_object.name,
      encoding_override=encoding,
      formatting_info=True)


  def create_table(self, fromcell=None, tocell=None, nheader=0, sheet=0):
    """
    Creates a table (as a list) based on given query and columns

    fromcell:
      The index of the cell where to begin. The default
      is from the beginning of the data set (0, 0).

    tocell:
      The index of the cell where to end the selection.
      Default is in the end of the data set.

    nheader:
      Number of lines which are considered as a header lines.
      Normally, the value is 0 (default) or 1.

    sheet:
      Name or index of the sheet as string/unicode. The index starts from the 0
      and is the default value. If numeric value is given, provide it in format::

        et.create_table(fromcell='A1', tocell='B2', sheet='2')

    """
    rows = []

    # Select sheet by given index or name
    if type(sheet) is int or sheet.isdigit():
      sh1 = self.book.sheet_by_index(int(sheet))
    else:
      sh1 = self.book.sheet_by_name(sheet)

    # Name selection, like: 'A1' or 'AB12'
    if type(fromcell) in [str, unicode]:
      match = re.match(r'(?P<chars>[A-Z]+)(?P<nums>[1-9]+[0-9]*)', fromcell)
      if match:
        parts = (match.group('chars'), int(match.group('nums')))
        fromcell = toindex(*parts)
      else:
        fromcell = tuple([int(num) for num in fromcell.split(u',')])

    # Name selection, like: 'A1' or 'AB12'
    if type(tocell) in [str, unicode]:
      match = re.match(r'(?P<chars>[A-Z]+)(?P<nums>[1-9]+[0-9]*)', tocell)
      if match:
        parts = (match.group('chars'), int(match.group('nums')))
        tocell = toindex(*parts)
      else:
        tocell = tuple([int(num) for num in tocell.split(u',')])

    if not fromcell:
      fromcell = (0, 0)

    # If ending cell is not given, calculate
    # it from rows and cols
    #print sh1.ncols, sh1.nrows
    #print (tocell[0] > (sh1.ncols -1)) or (tocell[1] > (sh1.nrows -1))
    maxrow_index = sh1.nrows -1
    maxcol_index = sh1.ncols -1
    if not tocell:
      tocell = (maxcol_index, maxrow_index)

    # If the value is bigger than the value, default to max value
    if tocell[0] > maxcol_index:
      tocell = (maxcol_index, tocell[1])

    # If the value is bigger than the value, default to max value
    if tocell[1] > maxrow_index:
      tocell = (tocell[0], maxrow_index)

    # Iterate columns
    rows = {'headers': [], 'rows': []}
    widths = []
    for rnum in range(fromcell[1], tocell[1]+1):

      # Iterate rows within column
      cols = []
      for cnum in range(fromcell[0], tocell[0]+1):
        cell = sh1.cell(rnum, cnum)
        width = sh1.computed_column_width(cnum)

        # Put data
        cell_data = {'type': 'row', 'width': width, 'value': self._get_value(cell)}

        # If header row
        if rnum < nheader:
          cell_data['type'] = 'header'

        # Get more format info for the cell
        cell_data.update(self._get_formatting(cell))

        cols.append(cell_data)

      # If first column is header, their all headers - i think
      if cols[0]['type'] == 'header':
        rows['headers'].append(cols)
      else:
        rows['rows'].append(cols)

    #widths_together = sum([cell['width'] for cols in rows])
    #print widths_together
    #widths = [round(val * 100.0 / widths_together) for val in widths]

    # Store into object for validation purposes
    self.fromcell = fromcell
    self.tocell = tocell

    return rows


  def _get_value(self, cell):
    """
    Returns the value of the xlrd Cell, based
    on type.
    """
    value = None

    # String
    if cell.ctype == xlrd.XL_CELL_TEXT:
      return unicode(cell.value)

   # Number: integer or float
    if cell.ctype == xlrd.XL_CELL_NUMBER:
      # There is no separation between integers
      # and other numbers. Show it as integer if
      # it seems like a one.
      # NOTE: float.is_integer is available only in python 2.6 and above
      if int(cell.value) == cell.value:
        return u'%s' % int(cell.value)
      return u'%s' % cell.value

    # Date type
    if cell.ctype == xlrd.XL_CELL_DATE:
      value = xlrd.xldate_as_tuple(cell.value, 0)

      date = datetime(
        year=value[0],
        month=value[1],
        day=value[2],
        hour=value[3],
        minute=value[4],
        second=value[5],
      )

      # Show more accurate value only if it exists
      if not value[1]:
        return u'%s' % value[0]
      elif value[3] and value[4] and value[5]:
        return unicode(date)
      else:
        # TODO: provide a way to define this
        return unicode(date.strftime('%Y-%m-%d'))

    # Boolean
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:
      if cell.value:
        return _(u'True')
      return _(u'False')

    # Error
    if cell.ctype == xlrd.XL_CELL_ERROR:
      return _(u'Error')

    return u''


  def _get_formatting(self, cell):
    """
    Returns some format related information
    about the given cell. The information is
    required/handy when creating the table

    cell:
      Cell object where to get formatting for

    Returns:
      dictionary containing the formatting information
    """
    format = {'bold':False, 'italic':False, 'bgcolor':None}

    xf = self.book.xf_list[cell.xf_index]
    font = self.book.font_list[xf.font_index]

    # Weight: 400 (normal), 700 (bold)
    if font.weight > 400:
      format['bold'] = True

    # Collect italic info
    if font.italic:
      format['italic'] = True

    # Get bg color
    bgcolor = self.book.colour_map[xf.background.background_colour_index]
    if bgcolor:
      format['bgcolor'] = bgcolor

    return format

def toindex(col, row):
  """
  Calculates the index number from
  the Excel column name. Examples:

    >>> from sphinxcontrib import exceltable
    >>> exceltable.toindex('A', 1)
    (0, 0)
    >>> exceltable.toindex('B', 10)
    (1, 9)
    >>> exceltable.toindex('Z', 2)
    (25, 1)
    >>> exceltable.toindex('AA', 27)
    (26, 26)
    >>> exceltable.toindex('AB', 1)
    (27, 0)

  .. NOTE::

     Following the naming in Excel/OOCalc,
     the row 'index' starts from the 1 and not from 0

  """
  a2z = 'ABCDEFGHIJLKMNOPQRSTUVWXYZ'

  total = 0
  mult = 0
  for char in col:
    total += (a2z.find(char) + (26 * mult))
    mult += 1

  return total, row-1


def toname(colx, rowy):
  """
  Opposite to `toindex`
  """
  colname = xlrd.colname(colx)
  return colname, rowy+1


def setup(app):
  """
  Extension setup, called by Sphinx
  """


  # Sphinx 5 support
  if '5' in sphinx.__version__.split('.'):
    app.add_directive('exceltable', ExcelTableDirective, 0, (0, 0, 0))
  else:
    app.add_directive('exceltable', ExcelTableDirective)

if __name__ == '__main__':
  _test()
