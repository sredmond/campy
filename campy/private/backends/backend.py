"""Load a campy graphical backend.

The default graphical backend is Tk, but others are available in varying
degrees of support.

The available backends are:

- Tk (default): Cross-platform graphics and widget library.
- JBE: Text-based communication to a Java backend: `acm.jar`. Requires Java.

This structure was modelled off of matplotlib's - for more information, see:

https://matplotlib.org/faq/usage_faq.html#what-is-a-backend

There are two ways to configure your backend. If there's a conflict, the last
one in the list will be used.

1. Setting the `CAMPY_BACKEND` environmental variable, either for your current
shell or for a single script::

    $ export CAMPY_BACKEND="Tk"
    $ python test.py

    $ CAMPY_BACKEND="tk" python test.py

2. If your script depends on a specific backend you can call `use()`::

    $ import campy
    $ campy.use('tk')

The `use()` function must be invoked before importing any other campy modules.
Calling `use` after another `campy` module has been imported will have no
effect. If you are building library code, you should avoid explicitly calling
`use()` unless absolutely necessary because your users will have to change the
code if they want to use a different backend.

Note: Backend name specifications are not case-sensitive, e.g. 'Tk' and 'tk'
are equivalent.
"""
# TODO(sredmond): Add support for `use`.
# TODO(sredmond): Add support for a .campyrc file.
from campy.private.backends.jbe.backend_jbe import JavaBackend
from campy.private.backends.tk.backend_tk import TkBackend

import logging
import os

# Module-level logger.
logger = logging.getLogger(__name__)

# The default backend to use when an environmental variable doesn't override.
DEFAULT_BACKEND = 'Tk'

backend_name = os.environ.get('CAMPY_BACKEND', DEFAULT_BACKEND).lower()
logger.debug('Attempting to create backend {!r}'.format(backend_name))

# Load a backend.
# TODO(sredmond): This is effectively a singleton because Python only imports
# modules once, unless forced to otherwise, such as with Jupyter's %autoreload
# magic. To defend against forced module reimport, this should be encapsulated.
if backend_name == 'tk':  # Load the Tk backend
    backend = TkBackend()
elif backend_name == 'jbe':  # Load the JBE backend.
    backend = JavaBackend()
else:
    raise ImportError('Unrecognized backend: {!r}'.format(backend_name))
