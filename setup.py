"""CAMPY provides Stanford's graphical libraries in Python.

This setup.py file is modified from:
- https://packaging.python.org/guides/distributing-packages-using-setuptools/
- https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open  # Default to text mode with universal newlines.

# Load the text of the README file.
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    README_TEXT = f.read()

setup(
    # The name of this project, as registered on PyPI.
    # You can install this package:
    #     $ pip install campy
    # It lives on PyPI at https://pypi.org/project/campy/
    name='campy',

    # Project versions, compliant with PEP440.
    # TODO(sredmond): Single-source the project version.
    # https://packaging.python.org/guides/single-sourcing-package-version/
    version="0.0.1.dev9",

    description="Stanford's introductory libraries in Python, including the ACM graphical libraries.",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://campy.sredmond.io',

    # Author details.
    author='Sam Redmond',
    author_email='sredmond@stanford.edu',

    # Project license.
    license='MIT',

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

    # Publicly visible project keywords.
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
    },

    # Include data files in the package.
    # TODO(sredmond): Include spl.jar if SPL support is installed, somehow.
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
)
