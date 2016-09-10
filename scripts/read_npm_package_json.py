#!/usr/bin/env python

#######################
# Usage:
#
# cat package.json | python scripts/read_npm_package_json.py
#
#######################

import json
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

for folder in ('checker', 'third_party'):
    path = os.path.join(os.path.dirname(dir_path), folder)
    sys.path.append(path)

from checker.processors import NpmProcessor

package_json = json.load(sys.stdin)

for name, version in package_json['dependencies'].items():
    processor = NpmProcessor(repo=name, version=version)

    license, _ = processor.get_license()

    print(u"{}: {}".format(name, license))
