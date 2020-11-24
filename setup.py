#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from knot import __version__, __name__

import pkg_resources

setup(
    name = __name__,
    version = __version__,
    packages = find_packages(),

    author = "Pierre Marijon",
    author_email = "pierre.marijon@inria.fr",
    description = "run Snakemake pipeline for analysis assembly output",
    long_description = open('Readme.md').read(),
    url = "https://gitlab.inria.fr/pmarijon/knot",
    
    install_requires = [str(requirement)
                        for requirement in pkg_resources.parse_requirements(open("requirements.txt"))],
    include_package_data = True,
    
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha"
    ],

    entry_points = {
        'console_scripts': [
            'knot = knot.__main__:main',
            'knot.path_search = knot.path_search.__main__:main',
            'knot.filter_tig = knot.filter_tig.__main__:main',
            'knot.sg_generation = knot.sg_generation.__main__:main',
            'knot.extremity_search = knot.extremity_search.__main__:main',
            'knot.analysis.classifications = knot.analysis.classifications:main',
            'knot.analysis.hamilton_path = knot.analysis.hamilton_path:main',
            'knot.analysis = knot.analysis.generate_report:main'
        ]
    }
)
