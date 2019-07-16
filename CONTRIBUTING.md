# Contributing

We love pull requests! By contributing to this project, you agree to abide by the [Stanford Code of Conduct](https://adminguide.stanford.edu/chapter-1/subchapter-1/policy-1-1-1) as well as this project's [Code of Conduct][https://github.com/sredmond/campy/blob/master/CODE_OF_CONDUCT.md].

## Getting Started

Fork this repository, then clone it to your local machine:

```
$ git clone git@github.com:your-username/campy.git
```

Ideally, activate a virtual environment for developing this library.

```
$ # make a virtual environment
$ # activate the virtual environment
(campy-dev)$
```

Install the project source as a dependency, using the path to the folder that contains `campy`'s  `setup.py` file.

```
(campy-dev)$ pip install --editable "path/to/campy[dev,test]"
```

The `dev` and `test` extras install additional packages that help with software development.

For a reasonable development environment, additionally run `pip install jupyter` in the virtual environment to have access to the fancy `ipython` interactive interpreter.

Project maintainers who handle documentation and distribution should also install the following packages.

```
(campy-dev)$ pip install sphinx sphinx_rtd_theme twine "requests[security]"
```

## How You Can Help

The file `TODO.md` very roughly contains a list of tasks with which we need help. We greatly appreciate anything you can implement from that list.

## Style

Read the `STYLE.md` guide before beginning. Otherwise, we conform to PEP8.

### Logging

Use the `logging` standard library module for logging.

## Testing

We use `pytest` for unit tests and `tox` for Python version compatibility testing. Many of this library's components are graphical and interactive, but the interactive tests will only run if the environmental variable `CAMPY_TEST_PLATFORM` is set.

To run unit tests, simply run `pytest` from any folder that contains tests, such as the project root folder. To run version compatibility tests, run `tox` from the project root folder.

---

## Credit

This file is modelled on the CONTRIBUTING files from [puppet](https://github.com/puppetlabs/puppet/blob/master/CONTRIBUTING.md) and [factory_girl_rails](https://github.com/thoughtbot/factory_girl_rails/blob/master/CONTRIBUTING.md).
