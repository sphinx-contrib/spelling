#!/usr/bin/env python3

import os
import pathlib

import pytest


def require_git_repo(f):
    return pytest.mark.skipif(
        not (pathlib.Path(os.getcwd()) / '.git').is_dir(),
        reason='Not a git repo')(f)
