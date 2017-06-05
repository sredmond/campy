# package acm.io;
from __future__ import print_function

class IOModel(object):
    def print(self, object):
        """String, boolean, char, double, float, int, long, object"""
        raise NotImplementedError

    def println(self, object):
        """String, boolean, char, double, float, int, long, Object"""
        raise NotImplementedError

    def show_error_message(self, msg):
        raise NotImplementedError

    def read_line(self, prompt=None):
        raise NotImplementedError

    def read_int(self, prompt=None, low=None, high=None):
        raise NotImplementedError

    def read_double(self, prompt=None, low=None, high=None):
        raise NotImplementedError

    def read_boolean(self, prompt=None, true_label="true", false_label="false"):
        raise NotImplementedError
