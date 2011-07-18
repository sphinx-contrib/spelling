Display SqlAlchemy models
=========================

Rendering PlantUML_ diagrams or GraphViz_ directed graphs generated from
SqlALchemy models.

Most part of code based on sphinxcontrib-plantuml_ source code.

Install
-------

::

    pip install sphinxcontrib-sadisplay


Usage
-----

Add sadisplay to extensions list::

    extenstion = ['sphinxcontrib.sadisp', ]

Add options to conf.py::

    plantuml = 'java -jar plantuml.jar'.split()
    graphviz = 'dot -Tpng'.split()
    sadisplay_default_render = 'plantuml' 


Render image::

    .. sadisplay::
        :module: myapp.model.user, myapp.model.post


Render link to image (html only)::

    .. sadisplay::
        :module: myapp.model.user, myapp.model.post
        :link:
        :alt: My Schema
        :render: graphviz


.. _PlantUML: http://plantuml.sourceforge.net/
.. _GraphViz: http://www.graphviz.org/
.. _sphinxcontrib-plantuml: http://bitbucket.org/birkenfeld/sphinx-contrib
