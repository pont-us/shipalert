#!/usr/bin/env python3

import os.path
from setuptools import setup

cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, "README.adoc")) as fh:
    long_desc = fh.read()

setup(name="shipalert",
      version="1.0.1",
      description="Report whether a vessel is within a bounding box",
      long_description_content_type="text/asciidoc",
      long_description=long_desc,
      url="https://github.com/pont-us/tdmagsus",
      author="Pontus Lurcock",
      author_email="pont@talvi.net",
      license="GNU GPLv3+",
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3",
                   ],
      packages=["shipalert"],
      install_requires=["beautifulsoup4", "requests"],
      entry_points={"console_scripts":
                        ["shipalert=shipalert.shipalert:main"]
                    },
      zip_safe=False)
