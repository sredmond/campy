# TODO

A non-exhaustive list of tasks and modules to do.

## Administrative
- Choose and standardize a logging framework.
- Choose and standardize a testing framework.
- Rewrite CONTIBUTING/CONTRIBUTORS.
- Update README and STYLE guides.
- Canonicalize backend API.
- (Optional) Python2 compatibility.

## Data Structures

### Documented

### Complete
```
├── grid.h
├── collections.h
├── basicstack/queue.h
├── lexicon.h
```

### In Progress
```
├── basicgraph.c
├── basicgraph.h
├── graph.h
├── linkedlist.h
├── priorityqueue.h
├── sparsegrid.h
```

### Untouched
```
├── collections.h
```
- Also: need to think of a good solution to deep copying of objects

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

## Graphics

### Documented

### Complete
```
├── goptionpane.cpp
├── goptionpane.h
├── gtypes.cpp
├── gtypes.h
├── gtimer.cpp
├── gtimer.h
├── gevents.cpp
├── gevents.h
├── gfilechooser.cpp
├── gfilechooser.h
├── gobjects.cpp
├── gobjects.h
├── gwindow.cpp
└── gwindow.h
```

### In Progress
```
├── gbufferedimage.cpp
├── gbufferedimage.h
├── ginteractors.cpp
├── ginteractors.h
```

### Untouched
```
├── gtable.cpp
├── gtable.h
├── gtextarea.cpp
├── gtextarea.h
```


### Removed

## IO

### Documented

### Complete
```
├── base64.cpp
├── base64.h
├── bitstream.cpp
├── bitstream.h
├── simpio.cpp
├── simpio.h
```

### In Progress
```
├── console.cpp
├── console.h
├── filelib.cpp
├── filelib.h
├── tokenscanner.cpp
├── tokenscanner.h
```

### Untouched
```
├── plainconsole.cpp
├── plainconsole.h
├── server.cpp (pure python?)
├── server.h
```

### Removed
```
├── urlstream.cpp  # Use `requests` or `urlparse`
└── urlstream.h    # Use `requests` or `urlparse`
```

## Private

### Complete

### In Progress
```
├── init.h
```

### Untouched
```
├── consolestreambuf.h
├── echoinputstreambuf.h
├── forwardingstreambuf.h
├── limitoutputstreambuf.h
├── platform.cpp
├── platform.h
```

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

### Documented

### Complete
```
├── error.cpp
├── error.h
```

### In Progress

### Untouched
```
├── exceptions.cpp
├── exceptions.h
```

### Removed
```
├── call_stack.h            # Exceptions have stack traces
├── call_stack_gcc.cpp      # Exceptions have stack traces
├── call_stack_windows.cpp  # Exceptions have stack traces
└── stack_exception.h       # Exceptions have stack traces
```

## Util

### Documented
```
├── direction.cpp
├── direction.h
```

### Complete
```
├── gmath.cpp
├── gmath.h
├── note.cpp
├── note.h
├── observable.cpp
├── observable.h
├── point.cpp
├── point.h
├── random.cpp
├── random.h
├── sound.cpp
├── sound.h
├── timer.cpp
└── timer.h
```

### In Progress
```
--- decorators.py
├── strlib.cpp
├── strlib.h
├── recursion.cpp
├── recursion.h
```

### Untouched

### Removed
```
├── foreach.h    # CPP-specific
├── regexpr.cpp  # Use `re`
├── regexpr.h    # Use `re`
```


## Other Project Ideas
- `trace`: log all outputs from the flags?
- `sharing`: publicize/share code
- `debug/decorators`: debugging/development tools, dump args
- `positivity`: positive thoughts
- `BasicQueue/BasicStack`: list-backed opaque queue/stack
- `timer` to execute a function every n seconds
- `multiprocessing.Queue` for events to backend.
- `linter`: autolint code
- `submission-tools`: aggregate submission tools for stanford teachers
- `autograder-tools`: aggregate autograding tools for stanford teachers

## Come Back To
- All objects already have an ID and type, so no need to track that data.
- Make sure project includes relevant features from the plain ole Java version.
- Consider making `GEvent`s actually use class hierarchies instead of event type enums.
- `WINDOW_CLOSING` v. `WINDOW_CLOSED`
- add attribute descriptors to properties
- setFillColor should also setFilled
- Consider forwarding all Java method attribute lookups to snake case, with/without deprecations?