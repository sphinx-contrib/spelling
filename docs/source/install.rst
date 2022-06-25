.. spelling:word-list::

   sphinxcontrib

==============
 Installation
==============

1. Install the extension with pip: ``pip install sphinxcontrib-spelling``

2. Add ``'sphinxcontrib.spelling'`` to the ``extensions`` list in
   ``conf.py``.

   .. code-block:: python

      extensions = [ 'sphinxcontrib.spelling' ]

3. Then pass ``"spelling"`` as the builder argument to ``sphinx-build``.

   .. code-block:: shell-session

      $ sphinx-build -b spelling docs/source docs/build
