.. -*- restructuredtext -*-

==========================
README for Sword Extension
==========================

Sword is a package for Bible research and study. The extension can call Sword
and insert Bible verses inline.


Functionalities
===============

The extension adds two roles: :sword: and :bible:.

- ``:bible:`` adds bible verse and key in text. for example ``:bible:`Ge 1:1``` 
  will insert ::

     1 In the beginning God created the heavens and the earth.[Genesis 1:1]

  The number '1' at the beginning of the line indicate the number of the verse
  in Bible book. It is necessary when use the role as ``:bible:`Ge 1:1-3```.

- ``:sword:`` adds a key to indicate relative part of the Bible. Although the
  verses does not display in the text directly, they can be shown in two ways:

  - Shown as tooltip. When you put cursor on the Bible key, such as
    [Genesis 1:1-3], the relative verses will be shown.
  - Shown as inline text. When you click the Bible key, the relative verses
    will be shown behind. If clicking it again, the verses will fold in.

  The two different ways cannot be used together.


Installing
==========

The extension needs one config in conf.py: ::

   sword_args = ['ASV', 'tooltip', 'mono']

- The first variable set Bible book for Sword. Some book don't support multiple
  key selection such as ``:bible:`Ge 1:1,3-5```. That's not a problem can be
  solved by the extension.
- The second variable chooses display style for ``:sword:``. Only two values are
  accepted: tooltip and folder.
- The third variable selects font family for ``:bible:``.

The extension has two extra files: sword_folder.js, which needs to be put in 
.static/ without change, and sword_folder.css, whose content should be better 
to add to your css template. 
