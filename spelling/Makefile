# Default target is to show help
help:
	@echo "sdist          - Source distribution"
	@echo "html           - HTML documentation"
	@echo "spelling       - Check spelling of documentation"
	@echo "upload         - upload a new release to PyPI"
	@echo "installwebsite - deploy web version of docs"
	@echo "develop        - install development version"
	@echo "test           - run the test suite"


.PHONY: sdist
sdist: html
	python setup.py sdist

.PHONY: upload
upload: html
	python setup.py sdist upload

# Documentation
.PHONY: html
html:
	(cd docs && $(MAKE) html)

.PHONY: spelling
spelling:
	(cd docs && $(MAKE) spelling)

installwebsite: html
	(cd docs/build/html && rsync --rsh=ssh --archive --delete --verbose . www.doughellmann.com:/var/www/doughellmann/DocumentRoot/docs/sphinxcontrib.spelling/)

# Register the new version on pypi
.PHONY: register
register:
	python setup.py register

# Testing
.PHONY: test
test:
	tox

develop:
	python setup.py develop
