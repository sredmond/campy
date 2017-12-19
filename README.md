# Python Wrapper for Stanford Portable Graphics Library

This project provides a Python client to the Stanford Portable Graphics Library.

Therefore, users of this library can write Python code to interact with `GOval`s, `GWindow`s, and most everything else.

## Documentation

Documentation is available at to.be.hosted.somewhere.com. Raw HTML files can be found in `docs/_build/html`.

## Technical Overview

Stanford publishes a JAR file that listens on stdin for text commands, such as `GWindow.create`, and runs the appropriate command from a Java backend. Thus, any program that can send the right text commands can emulate the behavior of the ACM libraries.

### Package Organization
```
├── debug  # Tools and scripts for debugging this implementation
├── docs  # Documentation.
├── examples  # Example CS106 programs written using this library.
├── spgl  # The library itself.
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

