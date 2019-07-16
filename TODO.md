# TODO

A non-exhaustive list of tasks and modules to do.

## Scratch Space

- Possibly, remove the ability to set a GObject's location at creation time?

Finish the rest of the interactors <-- fairly straightforward
Adding interactors to regions <-- MWE, but needs to be woven in.
GImage and GBufferedImage <-- easy but requires an image buffering layer

Actual key events + modifiers <-- easy but tedious
Properly treat fonts <-- super annoying

- `stanford-karel`, `popup-console`, and `simpio` are spun off into their own projects.

## Administrative

### PyPI
- Update README for PyPI.
  - Add an example to the README.
- Reupload to PyPI.

### Infrastructure
- Rewrite informational print statements as logging messages.

### Branding
- Redesign logo to custom image.

## Data Structures

### Tested
- `shuffle`

### Documented

### Reasonably Complete

- `basicqueue`
- `basicstack`
- `grid`
- `lexicon`

### In Progress

- `basicgraph`
- `graph`
- `linkedlist`
- `priorityqueue`
- `sparsegrid`

### Untouched

- `collections`

### Structural
- What is a good way to deep-copy objects?

### Removed

```
├── dawglexicon.cpp  # Deprecated
├── dawglexicon.h    # Deprecated
├── deque.h          # Use `collections.deque`
├── hashcode.cpp     # Python's `hash()`
├── hashcode.h       # Python's `hash()`
├── hashmap.h        # Use builtin `dict`
├── hashset.h        # Use builtin `set`
├── linkedhashmap.h  # Use `collections.OrderedDict`
├── linkedhashset.h  # Use `collections.OrderedDict`
├── pqueue.h         # Deprecated
├── map.h            # Use `dict`
├── queue.h          # Use `collections.deque`
├── set.h            # Use `set`
├── shuffle.cpp      # Use `random.shuffle`
├── shuffle.h        # Use `random.shuffle`
├── stack.h          # Use `list`
├── stack.h          # Use `list`
├── stl.h            # CPP-specific
└── vector.h         # Use `list`
```

## Graphics / GUI

### Tested

### Documented

- `gwindow`

### Reasonably Complete

- `goptionpane`
- `gtypes`
- `gtimer`
- `gevents`
- `gfilechooser`
- `gobjects`

### In Progress

- `gbufferedimage`
- `ginteractors`

### Untouched

- `gtable`
- `gtextarea`

### Removed

## IO

### Tested

- `base64helper`
- `bitstream`

### Documented

### Reasonably Complete

### In Progress

- `console`
- `filelib`
- `tokenscanner`

### Untouched

- `plainconsole`
- `server`

### Removed

- `urlstream`  # Use `requests` or `urlparse`

## Private

### Tested

### Documented

### Complete

### In Progress

- tk backend
- java backend

### Untouched

- `consolestreambuf`
- `echoinputstreambuf`
- `forwardingstreambuf`
- `limitoutputstreambuf`
- `platform`

### Removed

```
├── foreachpatch.h  # CPP-specific
├── randompatch.h   # Solved by `random` 
├── static.h        # CPP-specific
├── tokenpatch.h    # CPP-specific
├── tplatform.h     # Unused 2017/05/05 
├── version.cpp     # Package has version info
└── version.h       # Package has version info
```

## System

### Tested

- `error`

### Documented

### Reasonably Complete

### In Progress

### Untouched

- `exceptions`

### Removed

```
├── call_stack.h            # Exceptions have stack traces
├── call_stack_gcc.cpp      # Exceptions have stack traces
├── call_stack_windows.cpp  # Exceptions have stack traces
└── stack_exception.h       # Exceptions have stack traces
```

## Util

### Tested

- `direction`

### Documented

### Reasonably Complete

- `gmath`
- `note`
- `observable`
- `point`
- `random`
- `sound`
- `timer`

### In Progress

- `decorators`
- `strlib`
- `recursion`

### Untouched

### Removed

```
├── foreach.h    # CPP-specific
├── regexpr.cpp  # Use `re`
├── regexpr.h    # Use `re`
```

## Other Project Ideas
- `trace`: log all outputs from the callstack
- `sharing`: freeze/publicize/share code
- `debug/decorators`: debugging/development tools, argument dumping.
- `linter`: autolint code
- `submit`: automatically allow students to submit to paperless.
- `submission-tools`: aggregate submission tools for stanford teachers
- `autograder-tools`: aggregate autograding tools for stanford teachers

## Prerelease Checklist
- Merge feature set with newly-developed C++/Java features.