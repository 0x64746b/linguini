#!/usr/bin/env python

from distutils.core import setup

from linguini import __version__


setup(name='linguini',
      version=__version__,
      packages=['linguini'],
      scripts=['bin/linguini'],
      provides='linguini',
     )
