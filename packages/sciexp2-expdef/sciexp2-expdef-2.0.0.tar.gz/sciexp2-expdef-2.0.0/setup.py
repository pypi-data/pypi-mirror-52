#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from distutils.core import setup


def run(base):
    version_file = os.path.join(base, "sciexp2", "expdef", "__init__.py")
    with open(version_file) as f:
        code = compile(f.read(), version_file, 'exec')
        version = {}
        exec(code, {}, version) #, global_vars, local_vars)

    with open(os.path.join(base, ".requirements.txt"), "r") as f:
        reqs = [line[:-1] for line in f.readlines()]

    opts = dict(name="sciexp2-expdef",
                version=version["__version__"],
                description="Experiment definition framework for SciExp²",
                long_description="""\
SciExp²-ExpDef provides a framework for easing the workflow of creating and
executing experiments, focused on *design-space exploration*.

It is divided into the following main pieces:

- Launchgen: Aids in defining experiments as a permutation of different
  parameters in the design space. It creates the necessary files to run these
  experiments (configuration files, scripts, etc.), which you define as
  templates that get substituted with the specific parameter values of each
  experiment.

- Launcher: Takes the files of launchgen and runs these experiments on different
  execution platforms like regular local scripts or cluster jobs. It takes care
  of tracking their correct execution, and allows selecting which experiments to
  run (e.g., those with specific parameter values, or those that were not
  successfully run yet).
""",
                author="Lluís Vilanova",
                author_email="llvilanovag@gmail.com",
                url="https://sciexp2-expdef.readthedocs.io/",
                license="GNU General Public License (GPL) version 3 or later",
                classifiers=[
                    "Development Status :: 4 - Beta",
                    "Environment :: Console",
                    "Intended Audience :: Science/Research",
                    "License :: OSI Approved :: GNU General Public License (GPL)",
                    "Programming Language :: Python",
                    "Topic :: Scientific/Engineering",
                ],
                packages=["sciexp2", "sciexp2.common", "sciexp2.expdef", "sciexp2.expdef.system"],
                package_data={"sciexp2": ["expdef/templates/*.dsc", "expdef/templates/*.tpl"]},
                scripts=["launcher"],
                requires=reqs,
                platforms="any",
    )

    setup(**opts)

if __name__ == "__main__":
    run(os.path.dirname(sys.argv[0]))
