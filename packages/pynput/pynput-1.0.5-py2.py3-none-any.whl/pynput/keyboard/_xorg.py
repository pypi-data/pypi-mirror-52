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
import threading

import Xlib.display
import Xlib.ext
import Xlib.ext.xtest
import Xlib.X
import Xlib.XK
import Xlib.protocol

from pynput._util import NotifierMixin
from pynput._util.xorg import *
from . import _base


class KeyCode(_base.KeyCode):
    @classmethod
    def _from_symbol(self, symbol, **kwargs):
        """Creates a key from a symbol.

        :param str symbol: The symbol name.

        :return: a key code
        """
        # First try simple translation
        keysym = Xlib.XK.string_to_keysym(symbol)
        if keysym:
            return self.from_vk(keysym, **kwargs)

        # If that fails, try checking a module attribute of Xlib.keysymdef.xkb
        if not keysym:
            try:
                return self.from_vk(
                    getattr(Xlib.keysymdef.xkb, 'XK_' + symbol, 0),
                    **kwargs)
            except:
                return self.from_vk(
                    SYMBOLS.get(symbol, (0,))[0],
                    **kwargs)


class Key(enum.Enum):
    # Default keys
    alt = KeyCode._from_symbol('Alt_L')
    alt_l = KeyCode._from_symbol('Alt_L')
    alt_r = KeyCode._from_symbol('Alt_R')
    alt_gr = KeyCode._from_symbol('Mode_switch')
    backspace = KeyCode._from_symbol('BackSpace')
    caps_lock = KeyCode._from_symbol('Caps_Lock')
    cmd = KeyCode._from_symbol('Super_L')
    cmd_l = KeyCode._from_symbol('Super_L')
    cmd_r = KeyCode._from_symbol('Super_R')
    ctrl = KeyCode._from_symbol('Control_L')
    ctrl_l = KeyCode._from_symbol('Control_L')
    ctrl_r = KeyCode._from_symbol('Control_R')
    delete = KeyCode._from_symbol('Delete')
    down = KeyCode._from_symbol('Down')
    end = KeyCode._from_symbol('End')
    enter = KeyCode._from_symbol('Return')
    esc = KeyCode._from_symbol('Escape')
    f1 = KeyCode._from_symbol('F1')
    f2 = KeyCode._from_symbol('F2')
    f3 = KeyCode._from_symbol('F3')
    f4 = KeyCode._from_symbol('F4')
    f5 = KeyCode._from_symbol('F5')
    f6 = KeyCode._from_symbol('F6')
    f7 = KeyCode._from_symbol('F7')
    f8 = KeyCode._from_symbol('F8')
    f9 = KeyCode._from_symbol('F9')
    f10 = KeyCode._from_symbol('F10')
    f11 = KeyCode._from_symbol('F11')
    f12 = KeyCode._from_symbol('F12')
    f13 = KeyCode._from_symbol('F13')
    f14 = KeyCode._from_symbol('F14')
    f15 = KeyCode._from_symbol('F15')
    f16 = KeyCode._from_symbol('F16')
    f17 = KeyCode._from_symbol('F17')
    f18 = KeyCode._from_symbol('F18')
    f19 = KeyCode._from_symbol('F19')
    f20 = KeyCode._from_symbol('F20')
    home = KeyCode._from_symbol('Home')
    left = KeyCode._from_symbol('Left')
    page_down = KeyCode._from_symbol('Page_Down')
    page_up = KeyCode._from_symbol('Page_Up')
    right = KeyCode._from_symbol('Right')
    shift = KeyCode._from_symbol('Shift_L')
    shift_l = KeyCode._from_symbol('Shift_L')
    shift_r = KeyCode._from_symbol('Shift_R')
    space = KeyCode._from_symbol('space', char=' ')
    tab = KeyCode._from_symbol('Tab')
    up = KeyCode._from_symbol('Up')

    insert = KeyCode._from_symbol('Insert')
    menu = KeyCode._from_symbol('Menu')
    num_lock = KeyCode._from_symbol('Num_Lock')
    pause = KeyCode._from_symbol('Pause')
    print_screen = KeyCode._from_symbol('Print')
    scroll_lock = KeyCode._from_symbol('Scroll_Lock')


class Controller(NotifierMixin, _base.Controller):
    _KeyCode = KeyCode
    _Key = Key

    #: The shift mask for :attr:`Key.ctrl`
    CTRL_MASK = Xlib.X.ControlMask

    #: The shift mask for :attr:`Key.shift`
    SHIFT_MASK = Xlib.X.ShiftMask

    def __init__(self):
        super(Controller, self).__init__()
        self._display = Xlib.display.Display()
        self._keyboard_mapping = None
        self._borrows = {}
        self._borrow_lock = threading.RLock()

        self.ALT_MASK = alt_mask(self._display)
        self.ALT_GR_MASK = alt_gr_mask(self._display)

    def __del__(self):
        if self._display:
            self._display.close()

    @property
    def keyboard_mapping(self):
        """A mapping from *keysyms* to *key codes*.

        Each value is the tuple ``(key_code, shift_state)``. By sending an
        event with the specified *key code* and shift state, the specified
        *keysym* will be touched.
        """
        if not self._keyboard_mapping:
            self._update_keyboard_mapping()
        return self._keyboard_mapping

    def _handle(self, key, is_press):
        """Resolves a key identifier and sends a keyboard event.

        :param event: The *X* keyboard event.

        :param int keysym: The keysym to handle.
        """
        event = Xlib.display.event.KeyPress if is_press \
            else Xlib.display.event.KeyRelease
        keysym = self._keysym(key)

        # Make sure to verify that the key was resolved
        if keysym is None:
            raise self.InvalidKeyException(key)

        try:
            keycode, shift_state = self.keyboard_mapping[keysym]
            self._send_key(event, keycode, shift_state)

        except KeyError:
            with self._borrow_lock:
                keycode, index, count = self._borrows[keysym]
                self._send_key(
                    event, keycode, index_to_shift(self._display, index))
                count += 1 if is_press else -1
                self._borrows[keysym] = (keycode, index, count)

        # Notify any running listeners
        self._emit('_on_fake_event', key, is_press)

    def _keysym(self, key):
        """Converts a key to a *keysym*.

        :param KeyCode key: The key code to convert.
        """
        return self._resolve_dead(key) if key.is_dead else None \
            or self._resolve_special(key) \
            or self._resolve_normal(key) \
            or self._resolve_borrowed(key) \
            or self._resolve_borrowing(key)

    def _send_key(self, event, keycode, shift_state):
        """Sends a single keyboard event.

        :param event: The *X* keyboard event.

        :param int keycode: The keycode.

        :param int shift_state: The shift state. The actual value used is
            :attr:`shift_state` or'd with this value.
        """
        with display_manager(self._display) as d, self.modifiers as modifiers:
            window = d.get_input_focus().focus
            window.send_event(event(
                detail=keycode,
                state=shift_state | self._shift_mask(modifiers),
                time=0,
                root=d.screen().root,
                window=window,
                same_screen=0,
                child=Xlib.X.NONE,
                root_x=0, root_y=0, event_x=0, event_y=0))

    def _resolve_dead(self, key):
        """Tries to resolve a dead key.

        :param str identifier: The identifier to resolve.
        """
        try:
            keysym, _ = SYMBOLS[CHARS[key.combining]]
        except:
            return None

        if keysym not in self.keyboard_mapping:
            return None

        return keysym

    def _resolve_special(self, key):
        """Tries to resolve a special key.

        A special key has the :attr:`~KeyCode.vk` attribute set.

        :param KeyCode key: The key to resolve.
        """
        if not key.vk:
            return None

        return key.vk

    def _resolve_normal(self, key):
        """Tries to resolve a normal key.

        A normal key exists on the keyboard, and is typed by pressing
        and releasing a simple key, possibly in combination with a modifier.

        :param KeyCode key: The key to resolve.
        """
        keysym = self._key_to_keysym(key)
        if keysym is None:
            return None

        if keysym not in self.keyboard_mapping:
            return None

        return keysym

    def _resolve_borrowed(self, key):
        """Tries to resolve a key by looking up the already borrowed *keysyms*.

        A borrowed *keysym* does not exist on the keyboard, but has been
        temporarily added to the layout.

        :param KeyCode key: The key to resolve.
        """
        keysym = self._key_to_keysym(key)
        if keysym is None:
            return None

        with self._borrow_lock:
            if keysym not in self._borrows:
                return None

        return keysym

    def _resolve_borrowing(self, key):
        """Tries to resolve a key by modifying the layout temporarily.

        A borrowed *keysym* does not exist on the keyboard, but is temporarily
        added to the layout.

        :param KeyCode key: The key to resolve.
        """
        keysym = self._key_to_keysym(key)
        if keysym is None:
            return None

        keyboard_mapping = self._display.get_keyboard_mapping(8, 255 - 8)

        def i2kc(index):
            return index + 8

        def kc2i(keycode):
            return keycode - 8

        #: Finds a keycode and index by looking at already used keycodes
        def reuse():
            for keysym, (keycode, _, _) in self._borrows.items():
                keycodes = keyboard_mapping[kc2i(keycode)]

                # Only the first four items are addressable by X
                for index in range(4):
                    if not keycodes[index]:
                        return keycode, index

        #: Finds a keycode and index by using a new keycode
        def borrow():
            for i, keycodes in enumerate(keyboard_mapping):
                if not any(keycodes):
                    return i2kc(i), 0

        #: Finds a keycode and index by reusing an old, unused one
        def overwrite():
            for keysym, (keycode, index, count) in self._borrows.items():
                if count < 1:
                    del self._borrows[keysym]
                    return keycode, index

        #: Registers a keycode for a specific key and modifier state
        def register(keycode, index):
            i = kc2i(keycode)
            keyboard_mapping[i][index] = keysym
            d.change_keyboard_mapping(
                keycode,
                keyboard_mapping[i:i + 1])
            self._borrows[keysym] = (keycode, index, 0)

        try:
            with display_manager(self._display) as d, self._borrow_lock:
                # First try an already used keycode, then try a new one, and
                # fall back on reusing one that is not currently pressed
                register(*(
                    reuse() or
                    borrow() or
                    overwrite()))
            return keysym

        except TypeError:
            return None

    def _key_to_keysym(self, key):
        """Converts a character key code to a *keysym*.

        :param KeyCode key: The key code.

        :return: a keysym if found
        :rtype: int or None
        """
        symbol = CHARS.get(key.char, None)
        if symbol is None:
            return None

        try:
            return symbol_to_keysym(symbol)
        except:
            try:
                return SYMBOLS[symbol][0]
            except:
                return None

    def _shift_mask(self, modifiers):
        """The *X* modifier mask to apply for a set of modifiers.

        :param set modifiers: A set of active modifiers for which to get the
            shift mask.
        """
        return (
            (self.ALT_MASK
                if Key.alt in modifiers else 0) |

            (self.ALT_GR_MASK
                if Key.alt_gr in modifiers else 0) |

            (self.CTRL_MASK
                if Key.ctrl in modifiers else 0) |

            (self.SHIFT_MASK
                if Key.shift in modifiers else 0))

    def _update_keyboard_mapping(self):
        """Updates the keyboard mapping.
        """
        with display_manager(self._display) as d:
            self._keyboard_mapping = keyboard_mapping(d)


@Controller._receiver
class Listener(ListenerMixin, _base.Listener):
    _EVENTS = (
        Xlib.X.KeyPress,
        Xlib.X.KeyRelease)

    #: A mapping from keysym to special key
    _SPECIAL_KEYS = {
        key.value.vk: key
        for key in Key}

    def _keycode_to_keysym(self, display, keycode, index):
        """Converts a keycode and shift state index to a keysym.

        This method uses a simplified version of the *X* convention to locate
        the correct keysym in the display table: since this method is only used
        to locate special keys, alphanumeric keys are not treated specially.

        :param display: The current *X* display.

        :param keycode: The keycode.

        :param index: The shift state index.

        :return: a keysym
        """
        keysym = display.keycode_to_keysym(keycode, index)
        if keysym:
            return keysym
        elif index & 0x2:
            return self._keycode_to_keysym(display, keycode, index & ~0x2)
        elif index & 0x1:
             return self._keycode_to_keysym(display, keycode, index & ~0x1)
        else:
            return 0

    def _event_to_key(self, display, event):
        """Converts an *X* event to a :class:`KeyCode`.

        :param display: The current *X* display.

        :param event: The event to convert.

        :return: a :class:`pynput.keyboard.KeyCode`

        :raises IndexError: if the key code is invalid
        """
        keycode = event.detail
        index = shift_to_index(display, event.state)

        # First try special keys...
        keysym = self._keycode_to_keysym(display, keycode, index)
        if keysym in self._SPECIAL_KEYS:
            return self._SPECIAL_KEYS[keysym]

        # ...then try characters...
        name = KEYSYMS[keysym]
        if name in SYMBOLS:
            char = SYMBOLS[name][1]
            if char in DEAD_KEYS:
                return KeyCode.from_dead(DEAD_KEYS[char])
            else:
                return KeyCode.from_char(char)

        # ...and fall back on a virtual key code
        return KeyCode.from_vk(keysym)

    def _run(self):
        with self._receive():
            super(Listener, self)._run()

    def _initialize(self, display):
        # Get the keyboard mapping to be able to translate events details to
        # key codes
        min_keycode = display.display.info.min_keycode
        keycode_count = display.display.info.max_keycode - min_keycode + 1
        self._keyboard_mapping = display.get_keyboard_mapping(
            min_keycode, keycode_count)

    def _handle(self, display, event):
        # Convert the event to a KeyCode; this may fail, and in that case we
        # pass None
        try:
            key = self._event_to_key(display, event)
        except IndexError:
            key = None
        except:
            # TODO: Error reporting
            return

        if event.type == Xlib.X.KeyPress:
            self.on_press(key)

        elif event.type == Xlib.X.KeyRelease:
            self.on_release(key)

    def _on_fake_event(self, key, is_press):
        """The handler for fake press events sent by the controllers.

        :param KeyCode key: The key pressed.

        :param bool is_press: Whether this is a press event.
        """
        (self.on_press if is_press else self.on_release)(
            self._SPECIAL_KEYS.get(key.vk, key))
