#! /usr/bin/env python3

from distutils.core import setup

setup(name='AsyncTcpProxy',
      version='0.3.0',
      description='My Python Project Setup',
      author='Eric Tang',
      author_email='tangcongyuan@gmail.com',
      url='',
      packages=[
          'async_tcp_proxy',
          'async_tcp_proxy.proxy',
          'async_tcp_proxy.server',
      ],
     )

