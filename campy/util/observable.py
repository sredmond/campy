#!/usr/bin/env python3 -tt
"""
File: observable.h
------------------
This file defines an abstract superclass named <code>Observable</code> that
allows objects to store lists of observers, which are other objects that are
notified when some part of the state of the observable object changes.
This is an example of the classic Observer/Observable design pattern.
"""
from abc import abstractmethod as _abstractmethod

class Observable():
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, *args, **kwargs)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

class Observer():
    @_abstractmethod
    def update(self, observed, *args, **kwargs):
        pass

__all__ = ['Observable', 'Observer']
