#!/bin/bash
#
# Run the build mode specified by the BUILD variable, defined in
# .travis.yml. When the variable is unset, assume we should run the
# standard test suite.

rootdir=$(dirname $(dirname $0))

# Show the commands being run.
set -x

# Exit on any error.
set -e

case "$BUILD" in
    docs)
        export ENABLE_SPELLING=1;
        sphinx-build -W -b html docs/source docs/build;
        sphinx-build -b spelling docs/source docs/build;;
    linter)
        flake8 sphinxcontrib setup.py;;
    *)
        python setup.py test \
               --coverage \
               --coverage-package-name=sphinxcontrib.spelling \
               --slowest \
               --testr-args="$@";
        coverage report --show-missing;;
esac
