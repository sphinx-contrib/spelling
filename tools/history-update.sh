#!/usr/bin/env bash

set -x

git remote -v

git branch -a

# We only look at the files that have changed in the current PR, to
# avoid problems when the template is changed in a way that is
# incompatible with existing documents.
if git log --name-only --pretty= "origin/master.." -- \
        | grep -q '^docs/source/history.rst$'; then
    echo "Found a change to history file."
    exit 0
fi

echo "PRs must include a change in docs/source/history.rst"
exit 1
