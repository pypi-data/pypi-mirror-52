#! /usr/bin/env python3

import imp
import os
import sys
import subprocess

NAME = 'OASYS1-COMSYL'
VERSION = '1.0.11'
ISRELEASED = False

DESCRIPTION = 'oasys-comsyl: Oasys widgets for COMSYL'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'M. Sanchez del Rio, M. Glass'
AUTHOR_EMAIL = 'srio@esrf.eu'
URL = 'https://github.com/oasys-kit/oasys-comsyl'
DOWNLOAD_URL = 'https://github.com/oasys-kit/oasys-comsyl'
LICENSE = 'MIT'

KEYWORDS = (
    'application',
    'COMSYL',
    'Oasys',
    'Orange',
    'comsyl',
)

CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Science/Research',
)


SETUP_REQUIRES = (
                  'setuptools',
                  )

INSTALL_REQUIRES = (
                    'setuptools',
                    'comsyl'
                   )

if len({'develop', 'release', 'bdist_egg', 'bdist_rpm', 'bdist_wininst',
        'install_egg_info', 'build_sphinx', 'egg_info', 'easy_install',
        'upload', 'test'}.intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        install_requires=INSTALL_REQUIRES
    )
else:
    extra_setuptools_args = dict()

from setuptools import find_packages, setup

PACKAGES = find_packages(
                         exclude = ('*.tests', '*.tests.*', 'tests.*', 'tests'),
                         )

PACKAGE_DATA = {"orangecontrib.comsyl.widgets.applications":["icons/*.png", "icons/*.jpg"],
}


NAMESPACE_PACAKGES = ["orangecontrib","orangecontrib.comsyl", "orangecontrib.comsyl.widgets"]


ENTRY_POINTS = {
    'oasys.addons' : ("COMSYL = orangecontrib.comsyl", ),
    'oasys.widgets' : (
        "COMSYL = orangecontrib.comsyl.widgets.applications",
    ),
}

if __name__ == '__main__':
    setup(
          name = NAME,
          version = VERSION,
          description = DESCRIPTION,
          long_description = LONG_DESCRIPTION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          url = URL,
          download_url = DOWNLOAD_URL,
          license = LICENSE,
          keywords = KEYWORDS,
          classifiers = CLASSIFIERS,
          packages = PACKAGES,
          package_data = PACKAGE_DATA,
          #py_modules = PY_MODULES,
          setup_requires = SETUP_REQUIRES,
          install_requires = INSTALL_REQUIRES,
          #extras_require = EXTRAS_REQUIRE,
          #dependency_links = DEPENDENCY_LINKS,
          entry_points = ENTRY_POINTS,
          namespace_packages=NAMESPACE_PACAKGES,
          include_package_data = True,
          zip_safe = False,
          )
