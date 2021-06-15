#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages, setup

requirements = [
    "gpflow>=2.1",
    "numpy<1.20",  # numpy 1.20 does not handle symbolic tensors correctly (c.f. https://github.com/tensorflow/models/issues/9706).
    "scipy",
    "tensorflow-probability>=0.10.1",
    "tensorflow>=2.2.0",
]

with open("README.md", "r") as file:
    long_description = file.read()

with open("VERSION", "r") as file:
    version = file.read().strip()

setup(
    name="gpflux",
    version=version,
    author="Secondmind Labs",
    author_email="gpflux@secondmind.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="GPflux: Deep GP library",
    license="Apache License 2.0",
    keywords="Deep-Gaussian-processes",
    install_requires=requirements,
    packages=find_namespace_packages(include=["gpflux*"]),
    package_data={"gpflux": ["py.typed"]},
    project_urls={
        "Source on GitHub": "https://github.com/secondmind-labs/GPflux",
        "Documentation": "https://secondmind-labs.github.io/GPflux/",
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
