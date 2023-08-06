# Copyright (c) 2011, SD Elements. See LICENSE.txt for details.

import os
import sys
import subprocess
import setuptools
from distutils.core import setup, Command

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()


class Test(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'testing/manage.py', 'test'])
        raise SystemExit(errno)

setuptools.setup(name="django-security_2.0",
      description='A collection of tools to help secure a Django project. update 2.1.4. mod for pwdExpiry',
      long_description=readme,
      long_description_content_type="text/markdown",
      maintainer="T",
      maintainer_email="",
      version="1.0.1",
      packages=["security", "security.south_migrations",
                "security.migrations", "security.auth_throttling"],
      url='https://github.com/dai-ictgeo/django-security',
      classifiers=[
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Framework :: Django :: 1.9',
          'Framework :: Django :: 1.10',
          'Framework :: Django :: 1.11',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Security',
      ],
      install_requires=[
          'django>=1.8',
          'ua_parser==0.7.1',
      ],
      cmdclass={'test': Test})
