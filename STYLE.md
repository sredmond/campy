# Style Guide

---

This style guide is for contributors to this library. If you are a student who uses these libraries for a school course, this style guide is not intended for you.

---

Every major open-source project has its own style guide: a set of conventions (sometimes arbitrary) about how to write code for that project. It is much easier to understand a large codebase when all the code in it is in a consistent style. 'Style' covers a lot of ground, from 'use snake_case for variable names' to 'avoid trivial getters and setters' to 'beautiful is better than ugly.'

## Code Formatting

Unless otherwise mentioned (see below), this project follows the [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/) for formatting Python code. That is, running `find . -name "*.py" | xargs pycodestyle` from the project root should result in zero output (admittedly, there are 3572 violations at the time of writing).

## Documentation

### Header Comments

Each code file should have a header comment containing a student-focused overview of the module's main purpose. We encourage the use of Sphinx constructs (code references, links, etc). Each sufficiently complicated module's header comment shoudl contain sample usage, showing a minimum viable use case for the module's exported functionality.

### Function Comments

Function comments should be written to be compatible with Sphinx. Specifically, we do not use numpy-style docstrings, Google-style docstrings, or Javadoc-style docstrings.

## Design Philosophy

When in doubt, feature design and structure should be driven by the needs of the students that will use this library, rather than by elegance of implementation.

## Weird Things We Do (and Why)

- Module-level symbols that should not be visible to the student are either prefixed with a leading underscore, so that students do not see the symbols on tab-complete. In particular, `import bar` in `foo.py` should be replaced with `import bar as _bar`. Even though this violates standard Python import conventions, it hides these symbols from tab-completion tools and student eyes. TODO(sredmond): Wouldn't it be better to only export a collection of module-level symbols with `__all__`?
- Write [numeric dates](https://xkcd.com/1179/) using ISO 8601 format (YYYY-MM-DD) in comments and documentation.

## Modifying the Style Guide

If you have any complaints or suggestions about this style guide, please open an issue to begin a discussion.

## Credit
Introductory phrasing taken from [Google's Style Guides](https://github.com/google/styleguide).
