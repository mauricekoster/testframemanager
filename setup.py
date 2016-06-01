#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='TestFrameExecutor',
      version='0.1',
      description='Execute TestFrame test scripts',
      packages=['SpreadsheetDOM'],
      py_modules=[ 'TestFrame', 'TestframeExecutor', 'TestFrameFactory' ],
      scripts=[ 'scripts/execute_testframe_script'],
      install_requires=['pyyaml', 'odfpy']
     )
