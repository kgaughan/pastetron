"""
Common code used in my setup.py files.
"""

from __future__ import with_statement

import os.path
import sys


def read(*filenames):
    """Read files relative to the executable."""
    files = []
    for filename in filenames:
        full_path = os.path.join(os.path.dirname(sys.argv[0]), filename)
        with open(full_path, 'r') as fh:
            files.append(fh.read())
    return "\n\n".join(files)


def read_requirements(requirements_path):
    """Read a requirements file, stripping out the detritus."""
    requirements = []
    to_ignore = ('#', 'svn+', 'git+', 'bzr+', 'hg+')
    with open(requirements_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line == '' or line.startswith(to_ignore):
                continue
            if line.startswith('-r '):
                requirements += read_requirements(
                    os.path.realpath(
                        os.path.join(
                            os.path.dirname(requirements_path),
                            line.split(' ', 1)[1].lstrip())))
            else:
                requirements.append(line)
    return requirements
