import hpe3parclient

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
  name='python-3parclient',
  version=hpe3parclient.version,
  description="HPE 3PAR HTTP REST Client",
  long_description=readme,
  author="Walter A. Boring IV",
  author_email="walter.boring@hpe.com",
  maintainer="Walter A. Boring IV",
  keywords=["hpe", "3par", "rest"],
  requires=['paramiko', 'eventlet', 'requests'],
  install_requires=['paramiko', 'eventlet', 'requests'],
  tests_require=["pytest", "pytest-runner", "pytest-testconfig",
                 "flask", "werkzeug", "requests", "pytest-cov"],
  license="Apache License, Version 2.0",
  packages=find_packages(),
  provides=['hpe3parclient'],
  url="http://packages.python.org/python-3parclient",
  classifiers=[
     'Development Status :: 5 - Production/Stable',
     'Intended Audience :: Developers',
     'License :: OSI Approved :: Apache Software License',
     'Environment :: Web Environment',
     'Programming Language :: Python',
     'Programming Language :: Python :: 2.6',
     'Programming Language :: Python :: 2.7',
     'Programming Language :: Python :: 3.6',
     'Programming Language :: Python :: 3.7',
     'Topic :: Internet :: WWW/HTTP',

     ]
  )
