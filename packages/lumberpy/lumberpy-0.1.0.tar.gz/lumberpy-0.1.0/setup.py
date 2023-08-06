#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["Click>=6.0", "coloredlogs==10.0"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Grey Rook GmbH",
    author_email="f.elsner@greyrook.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Lumberpy is an easily configurable python3 module for advanced logging use cases",
    entry_points={"console_scripts": ["lumberpy=lumberpy.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="lumberpy",
    name="lumberpy",
    packages=find_packages(include=["lumberpy"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.com/GreyRook/lumberpy",
    version="0.1.0",
    zip_safe=False,
)
