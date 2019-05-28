#!/usr/bin/python

from setuptools import setup

setup( name='browse-and-backup',
  version='0.1.1',
  description='Automate the backup process for all CDP discoverable devices using GIT subsystem',
  maintainer_email='sergey.zelyukin@gmail.com',
  keywords='cisco cdp crawler backup git automation',
  license='Apache License, Version 2.0',
  dependency_links=[
    "git+https://github.com/sergeyzelyukin/cisco-telnet.git#egg=ciscotelnet"
    "git+https://github.com/sergeyzelyukin/cisco-telnet.git#egg=ciscomapper"
  ],
  classifiers=[
  'Programming Language :: Python',
  'Programming Language :: Python :: 2',
  'Programming Language :: Python :: 2.7',
  'Operating System :: POSIX :: Linux',
  'Topic :: System :: Networking',
  'Topic :: Network Automation',
  'Topic :: Utilities',
  'Intended Audience :: System Administrators',
  'Intended Audience :: Network Engineers',
  'License :: OSI Approved :: Apache Software License',
  'Development Status :: 4 - Beta'],
  )
