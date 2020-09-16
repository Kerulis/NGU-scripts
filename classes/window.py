"""Window class contains the coordinate for the top left of the game window."""
import ctypes
import platform
from typing import Tuple

import win32gui
from deprecated import deprecated


class Window:
    """This class contains game window coordinates."""

    id = 0
    # difference between web and steam version
    x = 0
    y = 0

    # mouse offsets
    cx = x
    cy = y

    @deprecated(reason="Window() -Window instantiation- is deprecated, use Window.init() instead")
    def __init__(self, debug=False):
        Window.init(debug)

    @staticmethod
    def init(debug: bool = False):
        """Finds the game window and returns its coords."""
        if platform.release() == "10":
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        else:
            ctypes.windll.user32.SetProcessDPIAware()

        def window_enumeration_handler(hwnd, top_windows):
            """Add window title and ID to array."""
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        top_windows = []
        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        windows = [window[0] for window in top_windows if window[1] == 'NGU Idle']
        if len(windows) == 0:
            raise RuntimeError("Game window not found.")
        Window.id = windows[0]

    @staticmethod
    def set_pos(x: int, y: int) -> None:
        """Set top left coordinates."""
        Window.x = x
        Window.y = y

    @staticmethod
    def get_rect() -> Tuple[int, int, int, int]:
        """Returns the coordinates of the window"""
        return win32gui.GetWindowRect(Window.id)

    @staticmethod
    def get_rect_size() -> Tuple[int, int]:
        """Returns the resolution of the whole rect"""
        rect = win32gui.GetWindowRect(Window.id)
        return rect[2] - rect[0], rect[3] - rect[1]

    @staticmethod
    def get_rect_size_client() -> Tuple[int, int]:
        """Returns the resolution of the game window"""
        rect = win32gui.GetClientRect(Window.id)
        return rect[2] - rect[0], rect[3] - rect[1]

    @staticmethod
    def get_rect_borders() -> Tuple[int, int]:
        """Returns the border offsets (top, side)"""
        rect1 = Window.get_rect_size()
        rect2 = Window.get_rect_size_client()
        return int((rect1[0] - rect2[0]) / 2), rect1[1] - rect2[1] - int((rect1[0] - rect2[0]) / 2)

    @staticmethod
    def coord_manager(x: int, y: int) -> Tuple[int, int]:
        """"Scales coordinates based on resolution and adds borders"""
        resolution = Window.get_rect_size_client()
        base_resolution = (960, 600)
        x = int(x / base_resolution[0] * resolution[0])
        y = int(y / base_resolution[1] * resolution[1])

        borders = Window.get_rect_borders()
        x += borders[0]
        y += borders[1]

        return x, y

    @staticmethod
    def coord_manager_area(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
        coords1 = Window.coord_manager(x1, y1)
        coords2 = Window.coord_manager(x2, y2)
        return coords1[0], coords1[1], coords2[0], coords2[1]

    @staticmethod
    def shake() -> None:
        """Shake that Window"""
        for x in range(1000):
            win32gui.MoveWindow(Window.id, x, 0, 1000, 800, False)
        for y in range(1000):
            win32gui.MoveWindow(Window.id, 1000, y, 1000, 800, False)
        for x in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, x, 1000, 1000, 800, False)
        for y in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, 0, y, 1000, 800, False)
