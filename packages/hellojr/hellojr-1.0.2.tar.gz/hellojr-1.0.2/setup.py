#!/usr/bin/env python

import os
import setuptools
from distutils.core import setup


setup(name='hellojr',
  version=os.getenv('VERSION', '1.0.0'),
  description='Python packaging demonstration',
  author='Jason Reid',
  author_email='jason@reid.pro',
  maintainer='Jason Reid',
  maintainer_email='jason@reid.pro',
  url='https://gitlab.com/JRCode/python-pkg-hello',
  packages=['hellojr'],
  license='MIT License',
  entry_points={
    'console_scripts': [
      'hellojr=hellojr.command:cli',
    ],
  },
  python_requires='>=3.6',
  install_requires=[
    'click',
    'flask',
  ],
  extras_require={
    'dev': [
      'babel',
      'nose',
      'flake8',
      'coverage',
      'sphinx',
      'recommonmark',
      'twine',
      'wheel',
    ]
  },
  keywords=[
    'packaging',
    'testing',
    'documentation',
    'code coverage',
    'code quality',
    'lint',
    'localization'
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Natural Language :: French',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Documentation',
    'Topic :: Software Development :: Localization',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Quality Assurance',
    'Typing :: Typed',
  ],
)
