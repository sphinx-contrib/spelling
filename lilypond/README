.. -*- restructuredtext -*-

=============================
README for Lilypond Extension
=============================

It's a extension for including Lilypond music notes. The extension is made 
by modifying mathbase.py and pngmath.py. Most codes are copied and pasted
with some tiny changes. 


Functionalities
===============

- A new role 'lily'. the 'lily' role can input a standalone music markup.
  For example, a G clef can be inserted by ::

     :lily:`\musicglyph #"clefs.G"`

  The purpose of the 'lily' role is writing music comments or learning notes.
  So only one markup is allowed.

- A new directive 'lily'. The 'lily' directive can input a piece of music
  script, for example, ::

     .. lily::
   
        \relative c'' {
          c4 a d c
        }


Installing
==========

- A new config 'pnglily_fontsize', which can be used to set fontsize of
  'lily' role and 'lily' directive. ::

     pnglily_fontsize = ['6', '-3']

  The first value is for 'lily' role setting in absolute fontsize. The
  second value is for 'lily' directive setting in relative fontsize. 
