#!/bin/bash

git_project=$(git remote get-url origin | cut -f2 -d: | sed 's/.git//')
pr_url_base="https://github.com/${git_project}/pull/"

git log --merges --pretty="format:- %s %b" $(git describe --abbrev=0).. \
    | sed -E \
          -e 's#Merge pull request ##g' \
          -e 's# from [^[:space:]]+##' \
          -e 's|#([[:digit:]]+)|`#\1 <'${pr_url_base}'\1>`__|g'
echo
