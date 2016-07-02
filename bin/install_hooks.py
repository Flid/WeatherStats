#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import sys


def main():
    if not os.path.exists('.git'):
        print 'Error: git root not found at %s' % os.getcwd()
        sys.exit(1)

    source_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest_dir = '.git/hooks'

    shutil.rmtree(os.path.join(dest_dir, 'pre-commit-scripts'), ignore_errors=True)

    shutil.copytree(
        os.path.join(source_dir, 'bin/pre-commit-scripts'),
        os.path.join(dest_dir, 'pre-commit-scripts'),
    )
    shutil.copy2(
        os.path.join(source_dir, 'bin/pre-commit-hooks-runner.py'),
        os.path.join(dest_dir, 'pre-commit'),
    )
    print 'Hooks installed to %s' % dest_dir


if __name__ == '__main__':
    main()
