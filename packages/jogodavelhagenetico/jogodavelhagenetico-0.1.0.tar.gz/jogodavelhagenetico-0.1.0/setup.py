#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="jogodavelhagenetico",
    license="Apache License 2.0",
    version='0.1.0',
    author='Eduardo S. Pereira',
    author_email='pereira.somoza@gmail.com',
    packages=find_packages("src"),
    package_dir={"":"src/"},
    package_data={"":["modelo/*.pkl", "modelo/*.npy"]},
    description="Genetic Algorithm to play tic tac toe",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/duducosmos/jogodavelhagenetico",
    include_package_data=True,
    zip_safe=False,
    install_requires=["numpy", "pathos", "matplotlib", "pygenec"],
    entry_points = {"console_scripts":["jogodavelha = velhaapp.__main__:main"]},
)

print("\nExtra pack in windows: pip install windows-curses\n")
