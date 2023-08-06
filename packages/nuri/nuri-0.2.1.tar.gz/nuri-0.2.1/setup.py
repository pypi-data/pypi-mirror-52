#!/usr/bin/env python
from distutils.core import setup
import os,nuri.__init__
from glob import glob

#del os.link
setup(
    name="nuri",
    version=nuri.__version__,
    author="Vincent Dumont",
    author_email="vincentdumont@gmail.com",
    packages=["nuri"],
    dependency_links=['git+https://gitlab.com/citymag/analysis/mlpy.git'],
    scripts = glob('bin/*'),
    url="http://citymag.gitlab.io/nuri/",
    description="Urban Magnetometry Software",
    install_requires=['gwpy']
)
