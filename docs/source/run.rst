=========
 Running
=========

To process a document with the spell checker, use ``sphinx-build`` and
specify ``spelling`` as the builder name using the ``-b`` option.  The
output includes the headings from the document and any misspelled
words.  If suggestions are enabled, they are shown on the same line as
the misspelling. A log of all the words not found in the dictionary is
saved to the file ``spelling/output.txt`` under the build directory.

::

    $ make spelling
    sphinx-build -W -b spelling -d build/doctrees   source build/spelling
    Running Sphinx v1.0.7
    Initializing Spelling Checker
    loading pickled environment... done
    building [spelling]: all documents
    updating environment: 1 added, 2 changed, 0 removed
    reading sources... [ 33%] history
    reading sources... [ 66%] index
    reading sources... [100%] run

    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [ 20%] developers
    writing output... [ 40%] history
    writing output... [ 60%] index
    writing output... [ 80%] install
    (line  28) PyEnchant ["Penchant"]
    writing output... [100%] run

    Spelling checker messages written to ./docs/build/spelling/output.txt
    build finished with problems.
    make: *** [spelling] Error 1

