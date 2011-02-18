Release checklist
=================

- Update version number in `doc/conf.py` and `setup.py`.
- Update date in CHANGES.rst and make sure new features and bug fixes are mentioned.
- Build and zip the docs with `sphinx-build -W -b html doc html && cd html && zip -r doxylink-doc.zip *`.
- Commit sources with updated version numbers `hg commit`.
- Tag new version `hg tag doxylink-1.1` (or whatever the version is).
- Upload new version to PyPI `python setup.py sdist upload`
- Update the online documentation. Go to http://pypi.python.org/pypi/sphinxcontrib-doxylink and login. Click the 'releases' link near the top. At the bottom of the page, upload the `doxylink-doc.zip` from the `html` directory.
