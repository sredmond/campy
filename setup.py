"""CAMPY provides Stanford's graphical libraries in Python.

This setup.py file is adapted from:
- https://packaging.python.org/guides/distributing-packages-using-setuptools/
- https://github.com/pypa/sampleproject
- https://github.com/navdeep-G/setup.py
"""
import io
import os
import shutil
import subprocess
import sys

# Always prefer setuptools over distutils.
from setuptools import setup, find_packages, Command

# The name of this project, as registered on PyPI.
# You can install this package:
#     $ pip install campy
# It lives on PyPI at https://pypi.org/project/campy/
PROJECT_NAME = 'campy'

# The absolute path to the directory containing this file.
HERE = os.path.abspath(os.path.dirname(__file__))

# Load the text of the README file as the long description.
with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    README_TEXT = f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
project_slug = PROJECT_NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(HERE, project_slug, '__version__.py')) as f:
    exec(f.read(), about)
VERSION = about['__version__']


class PublishCommand(Command):
    """Custom setup.py command for publishing the package to PyPI.

    This class, in conjunction with the cmdclass argument to setup.py, enables
    normal publication to PyPI via:

        $ python setup.py publish

    To publish to TestPyPI, run:

        $ python setup.py publish --test
    """
    description = 'Build and publish this package.'
    user_options = [
        ('test', 't', 'Whether to push to TestPyPI instead of PyPI.')
    ]

    @staticmethod
    def status(message):
        """Print a message in bold (on TTYs)."""
        if sys.stdout.isatty():
            print('\033[1m{0}\033[0m'.format(message))
        else:
            print(message)

    def run(self):
        self.status('Preparing v{}...'.format(VERSION))
        self.status('Removing previous builds...')
        try:
            shutil.rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building source and wheel distribution...')
        subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

        # Upload the package to PyPI or TestPyPI.
        if not self.test:
            self.status('Uploading the package to PyPI via Twine...')
            subprocess.check_call(['twine', 'upload', 'dist/*'])
        else:
            self.status('Uploading the package to TestPyPI via Twine...')
            subprocess.check_call(['twine', 'upload', '--repository-url=https://test.pypi.org/legacy/', 'dist/*'])

        # TODO(sredmond): Tag earlier versions of the library.
        self.status('Pushing git tags...')
        subprocess.check_call(['git', 'tag', 'v{}'.format(VERSION)])
        subprocess.check_call(['git', 'push', '--tags'])

    # Capture the command option --test in a boolean.
    def initialize_options(self):
        self.test = None

    def finalize_options(self):
        # Convert self.test, which by default counts repetitions, to a boolean.
        self.test = self.test is not None


# TODO(sredmond): Populate the rest of these fields with values from __version__.py.
setup(
    name=PROJECT_NAME,

    # Project versions should be compliant with PEP440.
    version=VERSION,

    description="Stanford's introductory libraries in Python, including the ACM graphical libraries.",
    long_description=README_TEXT,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://campy.sredmond.io',

    # Author details.
    author='Sam Redmond',
    author_email='sredmond@stanford.edu',

    # Project license.
    license='MIT',

    # Trove Classifiers
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        # Project License (should match the license above).
        'License :: OSI Approved :: MIT License',

        'Topic :: Education',
        'Topic :: Software Development :: User Interfaces',

        # Supported Python versions.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # Publicly-visible project keywords.
    keywords='Stanford teaching education intro introductory ACM graphics CS106A CS106B CS106X CS106AP Karel GObject GOval GRect GWindow',

    # Exported packages.
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Supported Python versions. Unlike the classifiers above, `pip install`
    # will check this and refuse to install the project if the version does not
    # match.
    python_requires='>=3.4, <4',

    # Run-time dependencies, installed by pip when this project is installed.
    install_requires=[],  # No dependencies. Woohoo!

    # Additional dependency groups.
    # Install these using the following syntax, for example:
    #     $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest', 'pycodestyle'],
        'test': ['tox', 'pytest', 'pytest-cov', 'coverage'],
        'with-pillow': ['Pillow'],
    },

    # Include data files in the package.
    # TODO(sredmond): Include spl.jar if SPL support is installed, somehow.
    # include_package_data=True,
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Executable scripts (as entry points, preferred to scripts), providing
    # cross-platform support with the appropriate executable for the target
    # platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # Additional URLs.
    project_urls={
        'Source': 'https://github.com/sredmond/campy/',
        'Bug Reports': 'https://github.com/sredmond/campy/issues',
        'Say Thanks!': 'http://saythanks.io/to/sredmond',
    },

    # Support custom subcommand handlers. Enables:
    #     $ python setup.py publish
    cmdclass={
        'publish': PublishCommand,
    },
)
