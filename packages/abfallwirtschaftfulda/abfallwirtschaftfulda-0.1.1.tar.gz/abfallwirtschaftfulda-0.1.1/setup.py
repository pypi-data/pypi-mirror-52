#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import io
import os
import re
import sys

from setuptools import find_packages, setup


def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("abfallwirtschaftfulda", "__version__.py")
    return re.search(regex, read(*path)).group("version")


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with io.open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Stephan Beier",
    author_email="stbkde@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Asynchronous Python client for Abfallwirtschaft Fulda.",
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0", "yarl"],
    keywords=["abfallwirtschaft fulda", "abfallkalender", "abfall", "garbage calendar", "garbage collection", "api", "async", "client"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="abfallwirtschaftfulda",
    packages=find_packages(include=["abfallwirtschaftfulda"]),
    test_suite="tests",
    url="https://gitlab.com/stbkde/python-abfallwirtschaftfulda",
    version=get_version(),
    zip_safe=False,
)
