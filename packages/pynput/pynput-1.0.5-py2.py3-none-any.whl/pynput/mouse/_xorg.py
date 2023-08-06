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
import Xlib.display
import Xlib.ext
import Xlib.ext.xtest
import Xlib.X
import Xlib.protocol

from pynput._util.xorg import *
from . import _base


class Button(enum.Enum):
    """The various buttons.
    """
    left = 1
    middle = 2
    right = 3
    scroll_up = 4
    scroll_down = 5
    scroll_left = 6
    scroll_right = 7


class Controller(_base.Controller):
    def __init__(self):
        self._display = Xlib.display.Display()

    def __del__(self):
        if hasattr(self, '_display'):
            self._display.close()

    def _position_get(self):
        with display_manager(self._display) as d:
            data = d.screen().root.query_pointer()._data
            return (data["root_x"], data["root_y"])

    def _position_set(self, pos):
        x, y = pos
        with display_manager(self._display) as d:
            Xlib.ext.xtest.fake_input(d, Xlib.X.MotionNotify, x=x, y=y)

    def _scroll(self, dx, dy):
        if dy:
            self.click(
                button=Button.scroll_up if dy > 0 else Button.scroll_down,
                count=abs(dy))

        if dx:
            self.click(
                button=Button.scroll_right if dx > 0 else Button.scroll_left,
                count=abs(dx))

    def _press(self, button):
        with display_manager(self._display) as d:
            Xlib.ext.xtest.fake_input(d, Xlib.X.ButtonPress, button.value)

    def _release(self, button):
        with display_manager(self._display) as d:
            Xlib.ext.xtest.fake_input(d, Xlib.X.ButtonRelease, button.value)


class Listener(ListenerMixin, _base.Listener):
    #: A mapping from button values to scroll directions
    _SCROLL_BUTTONS = {
        Button.scroll_up.value: (0, 1),
        Button.scroll_down.value: (0, -1),
        Button.scroll_right.value: (1, 0),
        Button.scroll_left.value: (-1, 0)}

    _EVENTS = (
        Xlib.X.ButtonPressMask,
        Xlib.X.ButtonReleaseMask)

    def _handle(self, display, event):
        x = event.root_x
        y = event.root_y

        if event.type == Xlib.X.ButtonPress:
            # Scroll events are sent as button presses with the scroll
            # button codes
            scroll = self._SCROLL_BUTTONS.get(event.detail, None)
            if scroll:
                self.on_scroll(x, y, *scroll)
            else:
                self.on_click(x, y, Button(event.detail), True)

        elif event.type == Xlib.X.ButtonRelease:
            # Send an event only if this was not a scroll event
            if event.detail not in self._SCROLL_BUTTONS:
                self.on_click(x, y, Button(event.detail), False)

        else:
            self.on_move(x, y)
