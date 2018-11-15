#!/usr/bin/env python

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='UrlShortener',
      version='1.0',
      description='Url Shortener Library',
      author='Guillaume Hottin',
      packages=['url_shortener'],
      install_requires=requirements,
     )