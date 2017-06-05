""" TBD why do subsequent raises of the same exception object add to the traceback attirbute
"""

class ErrorException(RuntimeError):
    """
    This class allows errors to be reported in a consistent way.
    Clients typically call
        <pre><code>
        &nbsp;    raise ErrorException(msg);
        </code></pre>
    """
    def __init__(self, msg):
        if instance(msg, Exception):
            msg = "{cls}: {msg}".format(cls=msg.__class__, msg=str(msg))
        super().__init__(self, msg)
