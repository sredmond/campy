## Data Structures

### Complete
├── grid.h

### In Progress
├── basicgraph.cpp
├── basicgraph.h
├── graph.h
├── lexicon.cpp
├── lexicon.h
├── linkedlist.h
├── priorityqueue.h
├── sparsegrid.h

### Untouched
├── collections.h

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

### Complete
├── goptionpane.cpp
├── goptionpane.h
├── gtypes.cpp
├── gtypes.h
├── gtimer.cpp
├── gtimer.h

### In Progress
├── gbufferedimage.cpp
├── gbufferedimage.h
├── gevents.cpp
├── gevents.h
├── gfilechooser.cpp
├── gfilechooser.h

### Untouched
├── ginteractors.cpp
├── ginteractors.h
├── gobjects.cpp
├── gobjects.h
├── gtable.cpp
├── gtable.h
├── gtextarea.cpp
├── gtextarea.h

├── gwindow.cpp
└── gwindow.h

### Removed 

## IO

### Complete
├── base64.cpp
├── base64.h
├── bitstream.cpp
├── bitstream.h
├── simpio.cpp
├── simpio.h

### In Progress
├── console.cpp
├── console.h
├── filelib.cpp
├── filelib.h
├── tokenscanner.cpp
├── tokenscanner.h

### Untouched
├── plainconsole.cpp
├── plainconsole.h
├── server.cpp
├── server.h

### Removed 
├── urlstream.cpp  # Use `requests` or `urlparse`
└── urlstream.h    # Use `requests` or `urlparse`

## Private

### Complete

### In Progress
├── init.h

### Untouched
├── consolestreambuf.h
├── echoinputstreambuf.h
├── forwardingstreambuf.h
├── limitoutputstreambuf.h
├── platform.cpp
├── platform.h

### Removed 
├── foreachpatch.h  # CPP-specific
├── randompatch.h   # Solved by `random` 
├── static.h        # CPP-specific
├── tokenpatch.h    # CPP-specific
├── tplatform.h     # Unused 2017/05/05 
├── version.cpp     # Package has version info
└── version.h       # Package has version info

## System

### Complete
├── error.cpp
├── error.h

### In Progress

### Untouched
├── exceptions.cpp
├── exceptions.h

### Removed
├── call_stack.h            # Exceptions have stack traces
├── call_stack_gcc.cpp      # Exceptions have stack traces
├── call_stack_windows.cpp  # Exceptions have stack traces
└── stack_exception.h       # Exceptions have stack traces

## Util

### Complete
├── direction.cpp
├── direction.h
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

### In Progress
├── strlib.cpp
├── strlib.h
├── recursion.cpp
├── recursion.h

### Untouched

### Removed 
├── foreach.h    # CPP-specific
├── regexpr.cpp  # Use `re`
├── regexpr.h    # Use `re`
