=========
 Running
=========

To process a document with the spell checker, use ``sphinx-build`` and
specify ``spelling`` as the builder name using the ``-b`` option.  The
output includes the headings from the document and any misspelled
words.  If suggestions are enabled, they are shown on the same line as
the misspelling. A log of the words in each input file not found in
the dictionary is saved to the file ``<input>.spelling`` under the
build directory.

.. code-block:: console

   $ tox -e spelling -r
   spelling create: .../sphinxcontrib-spelling/.tox/spelling
   spelling installdeps: .[docs]
   spelling develop-inst: .../sphinxcontrib-spelling
   spelling installed: -f /Users/dhellmann/.pip/wheelhouse,alabaster==0.7.12,Babel==2.8.0,certifi==2020.6.20,chardet==3.0.4,docutils==0.16,dulwich==0.20.5,idna==2.10,imagesize==1.2.0,importlib-metadata==1.7.0,Jinja2==2.11.2,MarkupSafe==1.1.1,packaging==20.4,pbr==5.4.5,pyenchant==3.1.1,Pygments==2.6.1,pyparsing==2.4.7,pytz==2020.1,PyYAML==5.3.1,reno==3.1.0,requests==2.24.0,six==1.15.0,snowballstemmer==2.0.0,Sphinx==3.2.0,sphinxcontrib-applehelp==1.0.2,sphinxcontrib-devhelp==1.0.2,sphinxcontrib-htmlhelp==1.0.3,sphinxcontrib-jsmath==1.0.1,sphinxcontrib-qthelp==1.0.3,sphinxcontrib-serializinghtml==1.1.4,-e git+git@github.com:sphinx-contrib/spelling.git@b0b3e2a8c935701cfcbbc76ea1aa501a03ae4e22#egg=sphinxcontrib_spelling,urllib3==1.25.10,zipp==3.1.0
   spelling run-test-pre: PYTHONHASHSEED='1632297322'
   spelling run-test: commands[0] | sphinx-build -W -j auto -b spelling -d docs/build/doctrees docs/source docs/build/spelling
   Running Sphinx v3.2.0
   Initializing Spelling Checker 5.2.1.dev2
   Ignoring wiki words
   Ignoring acronyms
   Adding package names from PyPI to local dictionary…
   Ignoring Python builtins
   Ignoring importable module names
   Adding contents of .../sphinxcontrib-spelling/docs/source/spelling_wordlist.txt to custom word list
   Adding contents of .../sphinxcontrib-spelling/docs/source/spelling_people.txt to custom word list
   Looking for custom word list in /var/folders/5q/8gk0wq888xlggz008k8dr7180000hg/T/tmphsetrn0s/spelling_wordlist.txt
   building [mo]: targets for 0 po files that are out of date
   building [spelling]: all documents
   updating environment: [new config] 6 added, 0 changed, 0 removed
   reading sources... [ 16%] customize
   reading sources... [ 33%] developers
   reading sources... [ 50%] history
   reading sources... [ 66%] index
   reading sources... [ 83%] install
   reading sources... [100%] run

   waiting for workers...
   scanning .../sphinxcontrib-spelling/releasenotes/notes for current branch release notes
   got versions ['5.2.0']
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [ 16%] customize
   Extending local dictionary for customize
   writing output... [ 33%] developers
   Extending local dictionary for developers
   writing output... [ 50%] history
   Extending local dictionary for history
   writing output... [ 66%] index
   Extending local dictionary for index
   index.rst:17:speel:["Peel", "peel", "spell", "spiel", "Speer", "speed", "steel", "sepal", "spill", "spoil", "spool", "speller", "Pele", "supple", "Perl", "spew", "spree", "suppl", "repel", "spells", "spiels", "spleen", "peal", "seal", "seep", "sell", "Aspell", "Ispell", "sleep", "spell's", "spiel's"]:I can't speel.
   Writing .../sphinxcontrib-spelling/docs/build/spelling/index.spelling
   writing output... [ 83%] install
   Extending local dictionary for install
   writing output... [100%] run


   Warning, treated as error:
   Found 1 misspelled words
   ERROR: InvocationError for command .../sphinxcontrib-spelling/.tox/spelling/bin/sphinx-build -W -j auto -b spelling -d docs/build/doctrees docs/source docs/build/spelling (exited with code 2)
   __________________________________________________ summary ___________________________________________________
   ERROR:   spelling: commands failed
