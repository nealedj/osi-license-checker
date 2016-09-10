#!/usr/bin/env python

#######################
# Usage:
#
# cat requirements.txt | python scripts/read_pypi_requirements.py
#
#######################

import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

for folder in ('checker', 'third_party'):
    path = os.path.join(os.path.dirname(dir_path), folder)
    sys.path.append(path)

from checker.processors import PyPiProcessor, GitHubProcessor
import requirements

for dependency in requirements.parse(sys.stdin):
    if dependency.vcs == 'git':
        processor = GitHubProcessor(dependency.uri)

    else:
        version = None
        if dependency.specs:
            # get last version specfied
            _, version = dependency.specs[-1]

        processor = PyPiProcessor(repo=dependency.name, version=version)

    license, _ = processor.get_license()

    print(u"{}: {}".format(dependency.name, license))
