#!/usr/bin/env python3
#
"""Try to build the Django documentation.
"""

import argparse
import os
import subprocess
import sys
import tempfile


def doit(*cmd, description='', cwd=None):
    print(f'\n[{description}]\nrunning: {" ".join(cmd)}')
    completed = subprocess.run(cmd, cwd=cwd)
    try:
        completed.check_returncode()
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f'command failed {description}') from err


def try_build(workdir, srcdir, django_repo):
    print(f'working in {workdir}')
    doit(
        'git', 'clone', '--depth', '1', django_repo, 'django',
        description='clone django',
        cwd=workdir,
    )
    djangodir = workdir + '/django'
    doit(
        'tox', '-e', 'docs', '--notest',
        description='build django docs virtualenv',
        cwd=djangodir,
    )
    doit(
        '.tox/docs/bin/pip', 'uninstall', '-y', 'sphinxcontrib-spelling',
        description='uninstall packaged sphinxcontrib-spelling',
        cwd=djangodir,
    )
    doit(
        '.tox/docs/bin/pip', 'install', srcdir,
        description='install sphinxcontrib-spelling from source',
        cwd=djangodir,
    )
    doit(
        'tox', '-e', 'docs',
        description='build django docs',
        cwd=djangodir,
    )


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False,
                        help='show full tracebacks')
    parser.add_argument('--src', help='source directory')
    parser.add_argument('--django-repo',
                        default='https://github.com/django/django.git')
    parsed = parser.parse_args(args)

    srcdir = parsed.src
    if not srcdir:
        srcdir = os.path.realpath(
            os.path.dirname(os.path.dirname(sys.argv[0]))
        )

    try:
        with tempfile.TemporaryDirectory() as dirname:
            try_build(dirname, srcdir, parsed.django_repo)
    except Exception as err:
        if parsed.debug:
            raise
        print(f'ERROR: {err}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
