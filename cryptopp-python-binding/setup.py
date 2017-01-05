#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

setup(name="Python Crypto++ binding",
    ext_modules=[
        Extension("cryptopp", ["crypto.cpp"],
        libraries = ["boost_python3"],
        extra_compile_args=['-std=c++11', '-fprofile-arcs', '-ftest-coverage', '-coverage'],
        extra_link_args=['-std=c++11', '-fprofile-arcs']
        )
    ])
