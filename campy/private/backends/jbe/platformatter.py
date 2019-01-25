import string as _string

import campy.util.strlib as _strlib

class Platformatter(_string.Formatter):
    """Subclasess a string Formatter to support the following additional specifiers.

        !q write_quoted_string()
        !b boolalpha()  truthy values become lower-case true, else false
        !u urlencode() -> implies write_quoted

    """
    def format(self, format_string, *args, **kwargs):
        # print('format')
        # print(format_string, args, kwargs)
        return super().format(format_string, *args, **kwargs)

    def vformat(self, format_string, args, kwargs):
        # print('vformat')
        # print(format_string, args, kwargs)
        out =  super().vformat(format_string, args, kwargs)
        # print(out)
        return out

    def parse(self, format_string):
        # print('parse')
        # print(format_string)
        out = super().parse(format_string)
        # print(out)
        return out

    def get_field(self, field_name, args, kwargs):
        # print('get_field')
        # print(field_name, args, kwargs)
        return super().get_field(field_name, args, kwargs)

    def get_value(self, key, args, kwargs):
        # print('get_value')
        # print(key, args, kwargs)
        return super().get_value(key, args, kwargs)

    def check_unused_args(self, used_args, args, kwargs):
        # print('check_unused_args')
        # print(used_args, args, kwargs)
        return super().check_unused_args(used_args, args, kwargs)

    def format_field(self, value, format_spec):
        # print('format_field')
        # print(value, format_spec)
        return super().format_field(value, format_spec)

    def convert_field(self, value, conversion):
        # print('convert_field')
        # print(value, conversion)
        if conversion == 'b':
            return 'true' if value else 'false'
        elif conversion == 'q':
            return _strlib.quote_string(value)
        elif conversion == 'u':
            return _strlib.quote_string(_strlib.url_encode(value))

        return super().convert_field(value, conversion)

def _test():
    out = pformat('{0!s} {1!r} {2!b}', 4, 1, 4)
    print(out)

# Create one instance, and export its `format` method as a module-level function.

_inst = Platformatter()
pformat = _inst.format

__all__ = ['Platformatter', 'pformat']

if __name__ == '__main__':
    _test()
