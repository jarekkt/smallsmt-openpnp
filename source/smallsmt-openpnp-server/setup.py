#!/usr/bin/env python

from distutils.core import setup

setup(name='PySmallSmt',
      version='1.0',
      description='Python server for SmallSmt Pick&Place machines',
      author='Jaroslaw Karwik',
      author_email='jaroslaw.karwik@gmail.com',
      url='http://www.kartech.org',
      py_modules=['commserial','commsocekts','mainwindow','openpnp','smallsmt','smallsmtprotocol','smallsmt-openpnp-server'],
      install_requires=['pyqt5','jsonpickle'],
     )