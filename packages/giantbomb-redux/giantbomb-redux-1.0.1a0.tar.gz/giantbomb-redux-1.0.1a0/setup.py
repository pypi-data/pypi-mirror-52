#!/usr/bin/env python

import os, sys
from setuptools import setup
from giantbomb import giantbomb

def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name = "giantbomb-redux",
    version = giantbomb.__version__,
    author = giantbomb.__author__,
    author_email = "hidde@hiddejansen.com",
    description = ("A Python wrapper for the Giantbomb API."),
    license = "MIT",
    keywords = "giantbomb api wrapper",
    url = "https://github.com/ganonmaster/GiantBomb-redux",
    packages=['giantbomb'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['requests>=2.22.0', 'dacite>=1.0.2'],
    python_requires=">=3.7"
)
