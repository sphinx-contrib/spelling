#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re, string, shutil

no_fn_re = re.compile(r'[^a-zA-Z0-9_-]')

def die(msg):
    print msg
    sys.exit(1)

if not os.path.isdir('_template'):
    die('Please run this script from its directory.')

print 'Creating a new sphinx-contrib package'
name = raw_input('Name: ')
author = raw_input('Author name: ')
author_email = raw_input('E-mail: ')

if not name or not author:
    die('Please give name and author name.')
if no_fn_re.sub('', name) != name:
    die('Please only use alphanumerics, underscore and dash in the name.')
if os.path.exists(name):
    die('A subdirectory or file with that name already exists.')

shutil.copytree('_template', name)

def templated(filename):
    fp = open(os.path.join('_template', filename), 'r')
    tmp = string.Template(fp.read())
    fp.close()
    fp = open(os.path.join(name, 'setup.py'), 'w')
    fp.write(tmp.safe_substitute(**globals()))
    fp.close()

templated('setup.py')
templated('README')

print 'Created new package in directory', name
