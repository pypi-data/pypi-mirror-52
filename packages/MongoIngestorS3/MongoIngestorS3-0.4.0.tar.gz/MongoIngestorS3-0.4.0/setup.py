#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'MongoIngestorS3'
DESCRIPTION = 'Library that allows you to ingest data from mongo database into an s3 bucket'
URL = 'https://github.com/MihailButnaru/MongoIngestorS3'
EMAIL = 'butnarum@hotmail.com'
AUTHOR = 'Mihail Butnaru'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.4.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'boto3',
    'pymongo'
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
 name = NAME,
 packages = find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
 version = about['__version__'],
 description = DESCRIPTION,
 author = AUTHOR,
 author_email = EMAIL,
 license = 'MIT',
 url = URL,
 install_requires = REQUIRED,
 download_url = 'https://github.com/MihailButnaru/MongoIngestorS3/archive/v1.1.tar.gz',
 classifiers = [],
 python_requires='>=3',
)
# setup(
#     name=NAME,
#     version=about['__version__'],
#     description=DESCRIPTION,
#     long_description=long_description,
#     author=AUTHOR,
#     author_email=EMAIL,
#     python_requires=REQUIRES_PYTHON,
#     url=URL,
#     packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
#     # If your package is a single module, use this instead of 'packages':
#     # py_modules=['mypackage'],

#     # entry_points={
#     #     'console_scripts': ['mycli=mymodule:cli'],
#     # },
#     install_requires=REQUIRED,
#     extras_require=EXTRAS,
#     include_package_data=True,
#     license='MIT',
#     classifiers=[
#         # Trove classifiers
#         # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: Implementation :: CPython',
#         'Programming Language :: Python :: Implementation :: PyPy'
#     ],
#     # $ setup.py publish support.
#     cmdclass={
#         'upload': UploadCommand,
#     },
# )
