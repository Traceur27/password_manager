#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

setup(name="Python Crypto++ binding",
    ext_modules=[
        Extension("cryptopp", ["crypto.cpp"],
        libraries = ["boost_python3", "cryptopp"],
        extra_compile_args=['-std=c++11'],
        )
    ])
