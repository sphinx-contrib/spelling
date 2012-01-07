==============
 Installation
==============

Installing sphinxcontrib-sqltable
=================================

1. Install the extension with pip: ``pip install sphinxcontrib-sqltable``

Configuration
=============

1. Add ``'sphinxcontrib.sqltable'`` to the ``extensions`` list in ``conf.py``.

  ::

    extensions = [ 'sphinxcontrib.sqltable' ]

2. Set ``sqltable_connection_string`` in ``conf.py`` to point to the
   database to be used for the queries.  See also :ref:`config-options`.

.. _install-options:
