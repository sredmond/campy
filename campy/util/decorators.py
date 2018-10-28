import inspect as _inspect
import functools as _functools

## Decorators
def _bind_args(function, *args, **kwargs):
    """Returns an map from the names of function's arguments to values given by *args and **kwargs

    This is more or less an implementation of Python argument bind semantics, but it's not super accurate
    ¯\_(ツ)_/¯
        For example, it doesn't resolve any closure elements or anything, because ahh that's awful

    First, positional arguments are bound

    If you're a student reading this, you can ignore this implementation.

    Pre: *args and **kwargs represent valid parameters
    """
    argspec = _inspect.getfullargspec(function)
    sig = _inspect.Signature.from_function(function)
    ba = sig.bind(*args, **kwargs)
    bindings = ba.arguments.copy()
    # default values for keyword arguments
    if argspec.defaults:
        for var_name, default_value in zip(reversed(argspec.args), reversed(argspec.defaults)):
            if var_name not in bindings:
                bindings[var_name] = default_value
    # default values for keyword-only argument
    if argspec.kwonlydefaults:
        for var_name, default_value in argspec.kwonlydefaults.items():
            if var_name not in bindings:
                bindings[var_name] = default_value
    if argspec.varargs and argspec.varargs not in bindings:
        bindings[argspec.varargs] = tuple()
    if argspec.varkw and argspec.varkw not in bindings:
        bindings[argspec.varkw] = dict()
    return bindings

def print_args(function):
    """Decorate the given function to print out it's arguments and return val if not None

    """
    @_functools.wraps(function)
    def wrapper(*args, **kwargs):
        bound_arguments = _bind_args(function, *args, **kwargs)
        print("{name}({call})".format(
            name=function.__name__,
            call=', '.join("{}={}".format(arg, val) for arg, val in bound_arguments.items())
        ))
        retval = function(*args, **kwargs)
        if retval is not None:
            print("(return) {!r}".format(retval))
        return retval
    return wrapper

# def test_print_args():
#     @print_args
#     def all_together(x, y, z=1, *nums, indent=True, spaces=4, **options):
#         """The all_together function from Lab 3."""
#         pass

#     # all_together(2)
#     all_together(2, 5, 7, 8, indent=False)
#     all_together(2, 5, 7, 6, indent=None)
#     all_together()
#     # all_together(indent=True, 3, 4, 5)
#     # all_together(**{'indent': False}, scope='maximum')
#     all_together(dict(x=0, y=1), *range(10))
#     # all_together(**dict(x=0, y=1), *range(10))
#     # all_together(*range(10), **dict(x=0, y=1))
#     all_together([1, 2], {3:4})
#     all_together(8, 9, 10, *[2, 4, 6], x=7, spaces=0, **{'a':5, 'b':'x'})
#     all_together(8, 9, 10, *[2, 4, 6], spaces=0, **{'a':[4,5], 'b':'x'})
#     # all_together(8, 9, *[2, 4, 6], *dict(z=1), spaces=0, **{'a':[4,5], 'b':'x'})


def cache(function):
    function._cache = {}
    @_functools.wraps(function)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key in function._cache:
            return function._cache[key]
        retval = function(*args, **kwargs)
        function._cache[key] = retval
        return retval
    return wrapper

# @cache
# def fib(n):
#     return fib(n-1) + fib(n-2) if n > 2 else 1

def cache_challenge(max_size=None, eviction_policy='LRU'):
    assert eviction_policy in ['LRU', 'MRU', 'random']
    def decorator(function):
        function._cache = collections.OrderedDict()
        @_functools.wraps(function)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            if key in function._cache:
                # Before accessing this element, move it to the MRU side
                # of the list
                function._cache.move_to_end(key)
                return function._cache[key]
            retval = function(*args, **kwargs)

            # Check for eviction
            if max_size and len(function._cache) == max_size:
                if eviction_policy == 'LRU':
                    function._cache.popitem(last=False)
                elif eviction_policy == 'MRU':
                    function._cache.popitem(last=True)
                else:
                    randkey = random.choice(list(function._cache.keys()))
                    function._cache.pop(randkey)
            # Now that we know there's space, insert the element
            function._cache[key] = retval
            return retval
        return wrapper
    return decorator

# @cache_challenge(max_size=16, eviction_policy='LRU')
# def fib(n):
#     return fib(n-1) + fib(n-2) if n > 2 else 1


def enforce_types(function):
    expected = function.__annotations__
    if not expected:
        return function
    assert(all(map(lambda exp: type(exp) == type, expected.values())))
    @_functools.wraps(function)
    def wrapper(*args, **kwargs):
        bound_arguments = _bind_args(function, *args, **kwargs)
        for arg, val in bound_arguments.items():
            if arg in expected and not isinstance(val, expected[arg]):
                print("(Bad Argument Type!) argument '{arg}={val}': expected {exp}, received {r}".format(
                    arg=arg,
                    val=val,
                    exp=expected[arg],
                    r=type(val)
                ))

        retval = function(*args, **kwargs)

        # Check the return value
        if 'return' in expected and not isinstance(retval, expected['return']):
            print("(Bad Return Value!) return '{ret}': expected {exp}, received {r}".format(
                ret=retval,
                exp=expected['return'],
                r=type(retval)
            ))
        return retval
    return wrapper

# def test_enforce_types():
#     @enforce_types
#     def foo(a: int, b: str) -> bool:
#         if a == -1:
#             return 'Gotcha!'
#         return b[a] == 'X'

#     try:
#         foo(3, 'XYZXYZ')  # => True
#         foo(2, 'python')  # => False
#         foo(1, 4)  # prints "(Bad Argument Type!) argument b=4: expected <class 'str'>, received <class 'int'>" and then crashes
#         foo(-1, '')  # prints "(Bad Return Value!) return Gotcha!: expected <class 'bool'>, received <class 'str'>" and returns "Gotcha!"
#     except TypeError:
#         pass



def enforce_types_challenge(severity=1):
    assert severity in [0, 1, 2]
    if severity == 0:
        # Return a no-op decorator
        return lambda function: function

    def message(msg):
        if severity == 1:
            print(msg)
        else:
            raise TypeError(msg)

    def decorator(function):
        expected = function.__annotations__
        if not expected:
            return function
        assert(all(map(lambda exp: type(exp) == type, expected.values())))

        @_functools.wraps(function)
        def wrapper(*args, **kwargs):
            bound_arguments = _bind_args(function, *args, **kwargs)
            for arg, val in bound_arguments.items():
                if arg in expected and not isinstance(val, expected[arg]):
                    msg("(Bad Argument Type!) argument '{arg}={val}': expected {exp}, received {r}".format(
                        arg=arg,
                        val=val,
                        exp=expected[arg],
                        r=type(val)
                    ))

            retval = function(*args, **kwargs)

            # Check the return value
            if 'return' in expected and not isinstance(retval, expected['return']):
                msg("(Bad Return Value!) return '{ret}': expected {exp}, received {r}".format(
                    ret=retval,
                    exp=expected['return'],
                    r=type(retval)
                ))
            return retval
        return wrapper
    return decorator

def stylist(old, new, details):
    def stylist_decorator(function):
        @_functools.wraps(function)
        def stylist_wrapper(*args, **kwargs):
            print('Access to {0} has been stylistically replaced.'.format(function.__name__))
            print(old)
            print(new)
            return function(*args, **kwargs)
        return stylist_wrapper
    return stylist_decorator


# Example code.
# @stylist("GOval.getWidth()", "GOval.width", "In Python, you can just access this attribute directly.")
# def getWidth():
# print('I am a getWidth function.')
