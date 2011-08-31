Glossary
========

.. glossary::
  :sorted:

  directive
    Directives are extension blocks that provides certain
    functionality into document. A distinctive difference
    with :term:`roles <role>` is that the latter are in-line
    definitions.

    .. code-block:: rst

       RST document with directive:

       .. directivename:: optional argument
          :option1: opt value1
          :option2:

          content



  role
    In-line extensions. Usually used for defining part of the content:

    .. code-block:: rst

       Some text containing :rolename:`target-name` as well as
       other kind of :rolename:`targets <target-name>`

    .. code-block:: rst

       Copy the :file:`app.conf` to :directory:`/etc/`


  regexp
    Regular expression: a specific textual syntax used to match with the string.
    Powerful but somewhat complicated.

    See `further information from Wikipedia <http://en.wikipedia.org/wiki/Regular_expression>`_.

