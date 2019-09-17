#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='smallsmt_openpnp_server',
      version='1.8',
      description='Python server for SmallSmt Pick&Place machines',
      long_description=read('README.txt'),
      author='Jaroslaw Karwik',
      author_email='jaroslaw.karwik@gmail.com',
      url='http://www.kartech.org',
      packages=['smallsmt_openpnp_server'],
      install_requires=['pyqt5','jsonpickle'],
      license='MIT',
      classifiers = [
                  "Development Status :: 3 - Alpha",
                  "Topic :: Utilities",
                  "License :: OSI Approved :: MIT License",
                  "Programming Language :: Python :: 3.6"
              ],

)