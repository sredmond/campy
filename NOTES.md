# Notes

This file tracks weird notes and observations that have come up during development. The notes aren't necessarily a problem or bug, but just something to watch, such as an odd implementation note, a reminder, or anything else. Apparently strange behavior with the C++ libraries should be (eventually) reported to their current maintainer. 

## Scratch Space

- All objects already have an ID and type, so no need to track that data.
- Make sure project includes relevant features from the plain ole Java version.
- Consider making `GEvent`s actually use class hierarchies instead of event type enums.
- `WINDOW_CLOSING` v. `WINDOW_CLOSED`
- add attribute descriptors to properties
- setFillColor should also setFilled ??
- Consider forwarding all Java method attribute lookups to snake case, with/without deprecations?

## Apparent Problems with the C++ Library

When adding a note, please append your username and the date.

- `GWindow.getScreenHeight` uses the width of screen, not the height (sredmond ????)
- `Platform.setValue` the string command is GetValue not SetValue (sredmond ????)
- Possibly no `GWindow::setVisible` in C++ libs? (sredmond 2017-10-21)
- `void addItem(std::string item)` in C++ libs should probably accept const& (sredmond 2017-10-22)
- line 106 of gbufferedimage should have x,y comments (sredmond 2017-11-02)
- `SparseGrid` in `sparsegrid.py` `fill` method should not fill everything when fill is called, just keep a ref to the filled item (or a copy?)
- `countDiffPixels` should be decomposed
- `GLabel` doesn't recompute ascent/descent in C++ after changing text (sredmond 2017-12-07)
- `GLabel` C++ platform doesn't urlencode the font, where GInteractor `setFont` does (sredmond 2017-12-07)
- `GCompound_Add` in C++ version for some reason gets status with a very cryptic comment (all it says is `  // JL`)
- How can we be divorced from the 'project' entity of e.g. QTCreator?

## How to Rebuild Documentation

Run the following script to rebuild the documentation, and then commit the changes to Github to have them reflected to the hosted Github Pages.

```
(campy-dev)$ cd $(git rev-parse --show-toplevel)
(campy-dev)$ ./makedocs.sh
```

There are a few more steps for the first time that documentation is ever built in the repository. These steps are saved as reference for other projects.
```
(campy-dev)$ cd $(git rev-parse --show-toplevel)
(campy-dev)$ cd docs-src/
(campy-dev) docs-src$ sphinx-quickstart  # Enable all extensions when prompted.
(campy-dev) docs-src$ cd ..
(campy-dev)$ sphinx-apidoc --separate -o docs-src/ campy/
```

## Technical Overview

Stanford publishes a JAR file that listens on stdin for text commands, such as `GWindow.create`, and runs the appropriate command from a Java backend. Thus, any program that can send the right text commands can emulate the behavior of the ACM libraries.

### Package Organization
```
├── debug  # Tools and scripts for debugging this implementation
├── docs  # Documentation.
├── examples  # Example CS106 programs written using this library.
├── campy  # The library itself.
│   ├── datastructures  # Collections, such as `Lexicon` and `SparseGrid`
│   ├── graphics  # `GWindow`, `GOval`, `GBufferedImage`, etc.
│   ├── gui  # `GInteractor`
│   ├── io  # String and File IO helpers.
│   ├── misc  # Miscellaneous modules.
│   ├── private  # Private, implementation specific modules.
│   ├── system  # `error`
│   └── util  # Utility modules.
└── test  # One-off testing scripts for validation.
```

### Testing

Very few modules have been thoroughly tested, so the internals of this library may break at any time. The API is not frozen and may change without warning.



## An Incomplete CHANGELOG

- All `GInteractor` will now generate a :class:`GActionEvent` on interaction regardless of whether their action command is nonempty.

## Pushing to PyPI

First, bump the version number in `setup.py` and `campy/__version__.py`

Then, ensure you have `twine` installed and are in the project's root directory.

```
$ python setup.py publish
```

To publish to TestPyPI instead, use `python setup.py publish --test`.

If you want to check the validity of the built package, use the following steps:

```
$ python setup.py sdist bdist_wheel
$ twine check dist/*
$ check-manifest
```

If there are lingering build files, you might have to run `python setup.py clean --all` first.

Then, upload to TestPyPI or real PyPI, supplying the username and password of this project's owner.

```
# Upload to TestPyPI.
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# (OR) Upload to real PyPI.
$ twine upload dist/*
```

Distribution files (`.tar.gz` or `.whl`) which have been uploaded to PyPI are stored there indefinitely. Distribution files uploaded to TestPyPI are periodically cleared. So, it's fine to clear `dist/*` whenever you like.

If your `~/.pypirc` is out-of-date, you may get a weird message that your connection was refused. In this case, read the information on the [updated PyPI upload endpoint](https://packaging.python.org/guides/migrating-to-pypi-org/) and modify your config files accordingly.

Check that the package has been successfully pushed by visiting [TestPyPI](https://test.pypi.org/project/campy/) or [real PyPI](https://pypi.org/project/campy/).