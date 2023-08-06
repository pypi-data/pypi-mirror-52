#!/usr/bin/python3 -u
"""
Setup script for setuputils
Copyright (C) 2012-2013 by Peter A. Donis

Released under the Python Software Foundation License.
"""


name = "setuputils3"
version = "1.0.4"
description = "A utility to automate away boilerplate in Python 3 setup scripts."
startline = 3

author = "Peter A. Donis"
author_email = "peterdonis@alum.mit.edu"

license = "PSF"

dev_status = "Production"

classifiers = """
Environment :: Console
Intended Audience :: Developers
Intended Audience :: System Administrators
Operating System :: OS Independent
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Systems Administration
Topic :: Utilities
"""

py_modules = ["setuputils"]


if __name__ == '__main__':
    import sys
    import os
    from subprocess import call
    from distutils.core import setup
    from setuputils import convert_md_to_rst, setup_vars, long_description as make_long_description
    
    if "sdist" in sys.argv:
        convert_md_to_rst()
        call(['sed', '-i', 's/gitlab.com\/pdonis/pypi.org\/project/', 'README'])
    elif os.path.isfile("README.md"):
        long_description = make_long_description(globals(), filename="README.md")
    setup(**setup_vars(globals()))
