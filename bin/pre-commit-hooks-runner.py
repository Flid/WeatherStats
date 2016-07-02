#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess
import sys

pre_commit_scripts_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'pre-commit-scripts',
)

hooks = []
for f in os.listdir(pre_commit_scripts_dir):
    abspath = os.path.join(pre_commit_scripts_dir, f)
    if os.path.isfile(abspath) and os.access(abspath, os.X_OK):
        hooks.append(abspath)
hooks = sorted(hooks)

print 'Loaded %s hooks' % len(hooks)
for hook in hooks:
    print '.' * 80
    print 'Execute hook: %s' % os.path.basename(hook)
    try:
        subprocess.check_call(hook)
    except subprocess.CalledProcessError as e:
        sys.exit(1)
    print 'OK'
