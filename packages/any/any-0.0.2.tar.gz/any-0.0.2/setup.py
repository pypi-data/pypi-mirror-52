from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup, find_packages, Distribution

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="any",
    version="0.0.2",
    author="Anyscale Inc.",
    description=("Command Line Interface for Anyscale"),
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "any=any.scripts:main"
        ]
    },
    include_package_data=True,
    zip_safe=False)
