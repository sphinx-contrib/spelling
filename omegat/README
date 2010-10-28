==============
OmegaT adapter
==============

:author: SHIBUKAWA Yoshiki <yoshiki at shibu.jp>

.. warning::

   Sphinx 1.1 is under developing.
   This extension supposes patched version now.
   http://bitbucket.org/shibu/sphinx_i18n/

About
=====

This is the OmegaT adapter for Sphinx 1.1 or above.
Sphinx 1.1 will deliver i18n feature.
This extension accelarate this feature with OmegaT.
OmegaT is the best open source tool for translators.

OmegaT
======

OmegaT is a free translation memory application written in Java. 
It is a tool for professional translators.

This extension generate OmegaT porject file. OmegaT gets original
sentenses via po filter. 

URLs
====

:OmegaT: http://www.omegat.org/
:PyPI: http://pypi.python.org/pypi/sphinxcontrib-omegat
:Detail Document: http://packages.python.org/sphinxcontrib-omegat

Install
=======

.. code-block::

   easy_install -U sphinxcontrib-omegat

Workflow
========

Preparation
-----------

After installing, prepare the source project(sphinx).
Then, edit ``conf.py`` to enable OmegaT connection.

Of course, you should install OmegaT 2.2 or above.

.. codo-block:: python

   # add extension
   extensions = ['sphinxcontrib.omegat']

   # path setting
   omegat_project_path = '_build/sphinx_trans_jp'
   omegat_translated_path = '_build/translated'

   # OmegaT output path should be included the dirs which sphinx searchs
   locale_dirs = [omegat_translated_path]

   # You need language option.
   language = 'ja'

Generate Source Project
-----------------------

Create OmegaT project.

.. code-block:: bash

   $ sphinx-build -b omegat . .

Then, launch OmegaT and edit translation project.

Generate Message Catalog
------------------------

Before this, check OmegaT settings. See ``Options`` - ``File Filters..``.
You should set ``.po``'s encoding 'UTF-8' (both input/output).

Select ``Project`` - ``Create Translated Documents`` to generate 
translated ``.po`` file. After that, create compiled message catalog.

.. code-block:: bash

   $ sphinx-build -b msgfmt . .

Build Document
--------------

You prepared your message catalog! Congraturations!
You can build your document as usual.

.. code-block:: bash

   $ make html


Contribution
============

If you notify bugs or has any request, send e-mail to me(yoshiki or shibu.jp)
or report it to issue tracker at http://bitbucket.org/birkenfeld/sphinx-contrib/

