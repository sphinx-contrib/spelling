.. -*- restructuredtext -*-

==========================
README for ConTeXt Builder
==========================

It's a ConTeXt builder for Sphinx. It is very primitive at present. It would
be a long time to implement full functions for the builder, since ConTeXt mkiv
is not stable.


Installing
==========

If you want to take a look and have a try, you can put the builder in your 
.extension directory. The conf.py needs some modification:

- Set the builder as a extension

     extensions = ['context']

- Set the config values

     context_documents = [
       ('index', 'document_name', u'Project Name',
        u'Your Name', 'manual'),
     ]

  It's the same with LaTeX builder's config setting.


Warning
=======

The ConTeXt builder do *not* support list, link, image, and so on. Actually
it only has some treatments on toctree and section, which are also very
primitive.

I'm kind of not knowing what to do with the builder. If you have any request,
please let me know. That will be a good start. 
