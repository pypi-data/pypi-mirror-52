# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "click",
    "xlsxhelper",
]

setup(
    name="xlsx-split",
    version="0.1.2",
    description="Create new file for every row in excel sheet, with support of header and footer replication. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["xlsx-split"],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["xlsx_split"],
    entry_points={
        "console_scripts": [
            "xlsx-split = xlsx_split:main",
        ]
    },
)