# Contributing

We love pull requests! By participating in this project, you agree to abide by the [Stanford Code of Conduct](https://adminguide.stanford.edu/chapter-1/subchapter-1/policy-1-1-1).

## Getting Started

Fork this repository, then clone it to your local machine:

```
$ git clone git@github.com:your-username/campy.git
```

Ideally, activate a virtual environment for developing this library. Install the project source as a dependency with:

```
$ pip install -e path/to/campy
```

This should be the path to the folder that contains `campy`'s `setup.py` file.

If you want a reasonable development environment, also run

```
$ pip install "ipython[all]" pytest tox
```

If you're going to be operating as a maintainer of the project, handling documentation and distribution, you'll also need some maintenance packages:

```
$ pip install sphinx sphinx_rtd_theme twine "requests[security]"
```

## What We Need Help With

We've compiled a list of tasks we need help with at `TODO.md`. Anything you can take off that list will be much appreciated.

## Style

Read the `STYLE.md` guide before beginning. Otherwise, we conform to PEP8.

## Logging

We use the standard library `logging` module to log useful events to the console.

## Testing

We use `pytest` for unit tests. Since many of the components of this library are interactive, each test file differentiates whether or not to run these tests by checking to see if CAMPY_TEST_PLATFORM is set.

### Running Unit Tests

```
(campy-dev)$ pytest

```

---

## Credit

This file is modelled on the CONTRIBUTING files from [puppet](https://github.com/puppetlabs/puppet/blob/master/CONTRIBUTING.md) and [factory_girl_rails](https://github.com/thoughtbot/factory_girl_rails/blob/master/CONTRIBUTING.md).

