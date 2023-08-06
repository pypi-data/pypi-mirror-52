#!/usr/bin/env python
from setuptools import setup, Extension



hasher = Extension('hasher',
					sources=[],
                    libraries=['hasher'])


setup(name='pymhash',
      version = '0.0.2',
      description = 'Python interface to a C++ library to calculate multiple MD5 hashes at same time.',
      author = 'Angelo Frangione',
      author_email = 'angelo.frangione@gmail.com',
      license = 'GPL-v2.0',
      py_modules=['pymhash'],
      install_requires = ['eventlet'],
      ext_modules = [hasher]
      )
