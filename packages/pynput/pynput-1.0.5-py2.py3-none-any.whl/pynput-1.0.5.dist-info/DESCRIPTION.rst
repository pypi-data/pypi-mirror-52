pynput
======

This library allows you to control and monitor input devices.

Currently, mouse and keyboard input and monitoring are supported.


Controlling the mouse
---------------------

Use ``pynput.mouse.Controller`` like this::

    from pynput.mouse import Button, Controller

    mouse = Controller()

    # Read pointer position
    print('The current pointer position is {0}'.format(
        mouse.position))

    # Set pointer position
    mouse.position = (10, 20)
    print('Now we have moved it to {0}'.format(
        mouse.position))

    # Move pointer relative to current position
    mouse.move(5, -5)

    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)

    # Double click; this is different from pressing and releasing
    # twice on Mac OSX
    mouse.click(Button.left, 2)

    # Scroll two steps down
    mouse.scroll(0, 2)


Monitoring the mouse
--------------------

Use ``pynput.mouse.Listener`` like this::

    from pynput.mouse import Listener

    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(dx, dy):
        print('Scrolled {0}'.format(
            (x, y)))

    # Collect events until released
    with Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

A mouse listener is a ``threading.Thread``, and all callbacks will be invoked
from the thread.

Call ``pynput.mouse.Listener.stop`` from anywhere, or raise
``pynput.mouse.Listener.StopException`` or return ``False`` from a callback to
stop the listener.

On *Windows*, virtual events sent by *other* processes may not be received.
This library takes precautions, however, to dispatch any virtual events
generated to all currently running listeners of the current process.


Controlling the keyboard
------------------------

Use ``pynput.keyboard.Controller`` like this::

    from pynput.keyboard import Key, Controller

    keyboard = Controller()

    # Press and release space
    keyboard.press(Key.space)
    keyboard.release(Key.space)

    # Type a lower case A; this will work even if no key on the
    # physical keyboard is labelled 'A'
    keyboard.press('a')
    keyboard.release('a')

    # Type two upper case As
    keyboard.press('A')
    keyboard.release('A')
    with keyboard.pressed(Key.shift):
        keyboard.press('a')
        keyboard.release('a')

    # Type 'Hello World' using the shortcut type method
    keyboard.type('Hello World')


Monitoring the keyboard
-----------------------

Use ``pynput.keyboard.Listener`` like this::

    from pynput.keyboard import Key, Listener

    def on_press(key):
        print('{0} pressed'.format(
            key))

    def on_release(key):
        print('{0} release'.format(
            key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

A keyboard listener is a ``threading.Thread``, and all callbacks will be
invoked from the thread.

Call ``pynput.keyboard.Listener.stop`` from anywhere, or raise
``pynput.keyboard.Listener.StopException`` or return ``False`` from a callback
to stop the listener.

Starting a keyboard listener may be subject to some restrictions on your
platform.

On *Mac OSX*, one of the following must be true:

 *  The process must run as root.

 *  Your application must be white listed under *Enable access for assistive
    devices*. Note that this might require that you package your application,
    since otherwise the entire *Python* installation must be white listed.

On *Windows*, virtual events sent by *other* processes may not be received.
This library takes precautions, however, to dispatch any virtual events
generated to all currently running listeners of the current process.


Release Notes
=============

v1.0.5 - Fixes for dragging on OSX
----------------------------------
*  Corrected dragging on *OSX*.
*  Added scroll speed constant for *OSX* to correct slow scroll speed.


v1.0.4 - Fixes for clicking and scrolling on Windows
----------------------------------------------------
*  Corrected name of mouse input field when sending click and scroll events.


v1.0.3 - Fixes for Python 3 on Windows
--------------------------------------
*  Corrected use of ``ctypes`` on Windows.


v1.0.2 - Fixes for thread identifiers
-------------------------------------
*  Use thread identifiers to identify threads, not Thread instances.


v1.0.1 - Fixes for Python 3
---------------------------
*  Corrected bugs which prevented the library from being used on *Python 3*.


v1.0 - Stable Release
---------------------
*  Changed license to *LGPL*.
*  Corrected minor bugs and inconsistencies.
*  Corrected and extended documentation.


v0.6 - Keyboard Monitor
-----------------------
*  Added support for monitoring the keyboard.
*  Corrected wheel packaging.
*  Corrected deadlock when stopping a listener in some cases on *X*.
*  Corrected key code constants on *Mac OSX*.
*  Do not intercept events on *Mac OSX*.


v0.5.1 - Do not die on dead keys
--------------------------------
*  Corrected handling of dead keys.
*  Corrected documentation.


v0.5 - Keyboard Modifiers
-------------------------
*  Added support for modifiers.


v0.4 - Keyboard Controller
--------------------------
*  Added keyboard controller.


v0.3 - Cleanup
------------------------------------------------------------
*  Moved ``pynput.mouse.Controller.Button`` to top-level.


v0.2 - Initial Release
----------------------
*  Support for controlling the mouse on *Linux*, *Mac OSX* and *Windows*.
*  Support for monitoring the mouse on *Linux*, *Mac OSX* and *Windows*.


