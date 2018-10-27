"""File:
"""
import traceback as _traceback

# Default indentation is four spaces.
_INDENT = '    '

def get_indent(indenter=_INDENT):
    return count_depth() * indenter

def count_depth():
    stack_frames = _traceback.extract_stack()
    # stack_frames = stack_frames[:-1-parent]  # Pop myself off the stack
    depth_fn = None # stack_frames[-1][2]
    count = 0

    for filename, lineno, fn_name, text in reversed(stack_frames):
        # 'wrapper' is the default wrapped name for lru_cache, but it doesn't
        # whitelist student functions named wrapper either.
        if fn_name in ('get_indent', 'count_depth', 'wrapper'):
            continue
        if not depth_fn:
            depth_fn = fn_name
            continue
        elif fn_name == depth_fn:
            count += 1
        else:
            break
    return count

def _test_recursion():
    import functools as _functools

    # TODO: This doesn't work with decorators currently.
    @_functools.lru_cache(maxsize=None)
    def fib(n):
        print('{}fib({}):'.format(get_indent(), n))
        return 1 if n <= 2 else fib(n-1) + fib(n-2)

    print(fib.__name__)

    fib(8)

if __name__ == '__main__':
    _test_recursion()
