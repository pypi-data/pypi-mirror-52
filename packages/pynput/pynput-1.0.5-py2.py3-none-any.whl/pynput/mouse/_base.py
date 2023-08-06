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

import enum

from pynput._util import AbstractListener


class Button(enum.Enum):
    """The various buttons.

    The actual values for these items differ between platforms. Some
    platforms may have additional buttons, but these are guaranteed to be
    present everywhere.
    """
    #: The left button
    left = 1

    #: The middle button
    middle = 2

    #: The right button
    right = 3


class Controller(object):
    """A controller for sending virtual mouse events to the system.
    """
    @property
    def position(self):
        """The current position of the mouse pointer.

        This is the tuple ``(x, y)``, and setting it will move the pointer.
        """
        return self._position_get()

    @position.setter
    def position(self, pos):
        self._position_set(pos)

    def scroll(self, dx, dy):
        """Sends scroll events.

        :param int dx: The horizontal scroll. The units of scrolling is
            undefined.

        :param int dy: The vertical scroll. The units of scrolling is
            undefined.
        """
        self._scroll(dx, dy)

    def press(self, button):
        """Emits a button press event at the current position.

        :param Button button: The button to press.
        """
        self._press(button)

    def release(self, button):
        """Emits a button release event at the current position.

        :param Button button: The button to release.
        """
        self._release(button)

    def move(self, dx, dy):
        """Moves the mouse pointer a number of pixels from its current
        position.

        :param int x: The horizontal offset.

        :param int dy: The vertical offset.
        """
        self.position = tuple(sum(i) for i in zip(self.position, (dx, dy)))

    def click(self, button, count=1):
        """Emits a button click event at the current position.

        The default implementation sends a series of press and release events.

        :param Button button: The button to click.

        :param int count: The number of clicks to send.
        """
        with self as controller:
            for _ in range(count):
                controller.press(button)
                controller.release(button)

    def __enter__(self):
        """Begins a series of clicks.

        In the default :meth:`click` implementation, the return value of this
        method is used for the calls to :meth:`press` and :meth:`release`
        instead of ``self``.

        The default implementation is a no-op.
        """
        return self

    def __exit__(self, type, value, traceback):
        """Ends a series of clicks.
        """
        pass

    def _position_get(self):
        """The implementation of the getter for :attr:`position`.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _position_set(self, pos):
        """The implementation of the setter for :attr:`position`.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _scroll(self, dx, dy):
        """The implementation of the :meth:`scroll` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _press(self, button):
        """The implementation of the :meth:`press` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _release(self, button):
        """The implementation of the :meth:`release` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()


class Listener(AbstractListener):
    """A listener for mouse events.

    Instances of this class can be used as context managers. This is equivalent
    to the following code::

        listener.start()
        try:
            with_statements()
        finally:
            listener.stop()

    This class inherits from :class:`threading.Thread` and supports all its
    methods. It will set :attr:`daemon` to ``True`` when created.

    :param callable on_move: The callback to call when mouse move events occur.

        It will be called with the arguments ``(x, y)``, which is the new
        pointer position. If this callback raises :class:`StopException` or
        returns ``False``, the listener is stopped.

    :param callable on_click: The callback to call when a mouse button is
        clicked.

        It will be called with the arguments ``(x, y, button, pressed)``,
        where ``(x, y)`` is the new pointer position, ``button`` is one of the
        :class:`Button` values and ``pressed`` is whether the button was
        pressed.

        If this callback raises :class:`StopException` or returns ``False``,
        the listener is stopped.

    :param callable on_scroll: The callback to call when mouse scroll
        events occur.

        It will be called with the arguments ``(x, y, dx, dy)``, where
        ``(x, y)`` is the new pointer position, and ``(dx, dy)`` is the scroll
        vector.

        If this callback raises :class:`StopException` or returns ``False``,
        the listener is stopped.
    """
    def __init__(self, on_move=None, on_click=None, on_scroll=None):
        super(Listener, self).__init__(
            on_move=on_move, on_click=on_click, on_scroll=on_scroll)
