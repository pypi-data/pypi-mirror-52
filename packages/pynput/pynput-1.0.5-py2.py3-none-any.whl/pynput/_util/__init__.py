# coding=utf-8
# pynput
# Copyright (C) 2015-2016 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import contextlib
import functools
import threading


class AbstractListener(threading.Thread):
    """A class implementing the basic behaviour for event listeners.

    Instances of this class can be used as context managers. This is equivalent
    to the following code::

        listener.start()
        listener.wait()
        try:
            with_statements()
        finally:
            listener.stop()

    :param kwargs: A mapping from callback attribute to callback handler. All
        handlers will be wrapped in a function reading the return value of the
        callback, and if it ``is False``, raising :class:`StopException`.

        Any callback that is falsy will be ignored.
    """
    class StopException(Exception):
        """If an event listener callback raises this exception, the current
        listener is stopped.

        Its first argument must be set to the :class:`AbstractListener` to
        stop.
        """
        pass

    def __init__(self, **kwargs):
        super(AbstractListener, self).__init__()

        def wrapper(f):
            def inner(*args):
                if f(*args) is False:
                    raise self.StopException(self)
            return inner

        self._running = False
        self._thread = threading.current_thread()
        self._condition = threading.Condition()
        self._ready = False

        self.daemon = True

        for name, callback in kwargs.items():
            setattr(self, name, wrapper(callback or (lambda *a: None)))

    @property
    def running(self):
        """Whether the listener is currently running.
        """
        return self._running

    def stop(self):
        """Stops listening for mouse events.

        When this method returns, no more events will be delivered.
        """
        if self._running:
            self._running = False
            self._stop()

    def __enter__(self):
        self.start()
        self.wait()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def wait(self):
        """Waits for this listener to become ready.
        """
        self._condition.acquire()
        while not self._ready:
            self._condition.wait()
        self._condition.release()

    def run(self):
        """The thread runner method.
        """
        self._running = True
        self._thread = threading.current_thread()
        self._run()

    @classmethod
    def _emitter(self, f):
        """A decorator to mark a method as the one emitting the callbacks.

        This decorator will wrap the method and catch :class:`StopException`.
        If this exception is caught, the listener will be stopped.
        """
        @functools.wraps(f)
        def inner(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except self.StopException as e:
                e.args[0].stop()

        return inner

    def _mark_ready(self):
        """Marks this listener as ready to receive events.

        This method must be called from :meth:`_run`. :meth:`wait` will block
        until this method is called.
        """
        self._condition.acquire()
        self._ready = True
        self._condition.notify()
        self._condition.release()

    def _run(self):
        """The implementation of the :meth:`run` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _stop(self):
        """The implementation of the :meth:`stop` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()


class NotifierMixin(object):
    """A mixin for notifiers of fake events.

    This mixin can be used for controllers on platforms where sending fake
    events does not cause a listener to receive a notification.
    """
    def _emit(self, action, *args):
        """Sends a notification to all registered listeners.

        This method will ensure that listeners that raise
        :class:`StopException` are stopped.

        :param str action: The name of the notification.

        :param args: The arguments to pass.
        """
        stopped = []
        for listener in self._listeners():
            try:
                getattr(listener, action)(*args)
            except listener.StopException:
                stopped.append(listener)
        for listener in stopped:
            listener.stop()

    @classmethod
    def _receiver(cls, listener_class):
        """A decorator to make a class able to receive fake events from a
        controller.

        This decorator will add the method ``_receive`` to the decorated class.

        This method is a context manager which ensures that all calls to
        :meth:`_emit` will invoke the named method in the listener instance
        while the block is active.
        """
        @contextlib.contextmanager
        def receive(self):
            """Executes a code block with this listener instance registered as
            a receiver of fake input events.
            """
            self._controller_class._add_listener(self)
            try:
                yield
            finally:
                self._controller_class._remove_listener(self)

        listener_class._receive = receive
        listener_class._controller_class = cls

        # Make sure this class has the necessary attributes
        if not hasattr(cls, '_listener_cache'):
            cls._listener_cache = set()
            cls._listener_lock = threading.Lock()

        return listener_class

    @classmethod
    def _listeners(cls):
        """Iterates over the set of running listeners.

        This method will quit without acquiring the lock if the set is empty,
        so there is potential for race conditions. This is an optimisation,
        since :class:`Controller` will need to call this method for every
        control event.
        """
        if not cls._listener_cache:
            return
        with cls._listener_lock:
            for listener in cls._listener_cache:
                yield listener

    @classmethod
    def _add_listener(cls, listener):
        """Adds a listener to the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.add(listener)

    @classmethod
    def _remove_listener(cls, listener):
        """Removes this listener from the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.remove(listener)
