import curses
import re
from typing import Dict

""" FramedWindow, part of cursed_framework.
Display a simple window on the screen. Provides functions to print, input a string, and input a character.
Output coloring limited to 6 color pairs at the moment.
colored_input - emulate an html input box kinda, for login or other input fields

TODO: Clean up quite a bit like there's some srs work to be done there

"""



void = None


class Formatters:
    formats = {
        "underline": curses.A_UNDERLINE,
        "bold": curses.A_BOLD,
        "dim": curses.A_DIM
    }

    def __getitem__(self, item):
        if item in self.formats.keys():
            return self.formats[item]


class FramedWindow(object):
    """
    FramedWindow:
    Class to allow creation of a simple, single-window text-based interface.
    Includes numerous methods to work with curses and ensure function.

    Constructor kwargs: h: window height, in rows;
                        w: width, in chars
                        x: offset from left. Recommend at least 4: 0, 1 are ' ' and '|', so get at least 2 spaces inside
                        the box is the best method; anything less than 2 overwrites the border.
                        y: offset from the top. 1 is default, 0 works too.

                        immediate: bool - if set to False, does not initialize curses, useful for inspection and testing

    """



    dimensions = {
        "h": 25,
        "w": 80,
        "x": 0,
        "y": 1
    }

    def __new__(cls, *args, **kwargs):
        """ Create as a singleton. """
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        """ Start curses, set window into screen, allow scroll """
        kwargs: Dict[str, int]
        if kwargs:
            for key, value in kwargs.items():
                if key in self.dimensions.keys():
                    self.dimensions[key] = value
        # load stuff

        if (("immediate" not in kwargs.keys()) or
                ("immediate" in kwargs.keys() and kwargs["immediate"] == True)):
            self.screen, self.window, self.formatter = self.start_buffer()
            ## flush the output buffer, ie show the output
            self.cprint("\n")

    def start_buffer(self):
        """ Start output buffering in fancy color render mode, construct the window.
        Note the output buffer is not flushed here.
        """
        screen = curses.initscr()
        curses.start_color()
        screen.scrollok(True)
        win = curses.newwin(
            self.dimensions["h"],
            self.dimensions["w"],
            self.dimensions["y"],
            self.dimensions["x"]
        )
        win.scrollok(True)
        win.idlok(True)
        # y + 2 cus we wnat to be inside the window and inside the border
        # and then to get the bottom - 2 (inside border, inside window)
        win.setscrreg(self.dimensions["y"] + 2, self.dimensions["h"] - self.dimensions["y"] - 2)
        fmt = Formatters()
        return screen, win, fmt

    def decompile(self):
        """
        Destroy the window entirely, and call the curses deconstructor. If not using this, you may lose
        the echo response when typing in the terminal afterwards (fix with Ctrl+J).
        """
        self.window.clear()
        curses.endwin()
        print("Clean exit from curses.")

    def recompile_window(self):
        """ Redraw the window entirely, and put the cursor back at the spot where it was when it was first drawn."""
        self.window.erase()
        self.reload()
        ## self.window.chgat(self.dimensions["y"] + 4, self.dimensions["x"] + 4)
        self.window.setscrreg(self.dimensions["y"] + 2, self.dimensions["h"] - self.dimensions["y"] - 2)
        self.cprint("\n")

    def reload(self):
        """ Flush the output buffer writing it to screen. Must call border before and after to keep the border. """
        ## do border twice in order to keep the lines.
        self.window.border(0)
        self.window.refresh()
        self.window.border(0)

    def _okprint(self, xo: str, data: str) -> void:
        """Green-On-Black"""
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.window.addstr(xo + data, curses.color_pair(1))

    def _warnprint(self, xo: str, data: str) -> void:
        """Yellow-On-Black"""
        curses.init_pair(2, curses.COLOR_yellow, curses.COLOR_BLACK)
        self.window.addstr(xo + data, curses.color_pair(2))

    def _badprint(self, xo: str, data: str) -> void:
        """red on yellow"""
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_YELLOW)
        self.window.addstr(xo + data, curses.color_pair(3))

    def _goodprint(self, xo: str, data: str) -> void:
        """ blue on white """
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
        self.window.addstr(xo + data, curses.color_pair(5))

    def _onbar(self, xo: str, data: str) -> void:
        """black with white field background"""
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.window.addstr(xo + data, curses.color_pair(6))

    def place_bar(self,
                  xstart: int,
                  length: int,
                  linenumber=None,
                  prevpos=True) -> void:
        """
        Print a rectangle with no foreground chars and a blank white background.
        Useful for something like the background for a faux- username/password input field.
        """
        # get pos where we started, to return to after placing
        starting_position = curses.getsyx()
        spacer = " " * length
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
        self.window.addstr(curses.getsyx()[0] - 1, xstart, spacer, curses.color_pair(4))
        # return to starting positon, then immediately flush the buffer to replace the cursor at start and print
        if prevpos is True:
            self.window.addstr(starting_position[0] - 1, xstart, "")
        self.reload()

    def cprint(self,
               data: str,
               end: str = "\n",
               offset: int = 4,
               style=None,
               delim=" ",
               ) -> void:
        """ Print a string to the screen.
        end: default is \n,  passing end="" here is the same as print(end="", flush=True)
        offset: offset from the 0 point on the X axis
        style: [ colored printing - OK: green, WARN: yellow, RED: red+yellow, GOOD: blue+white, onbar: black+white ]
        xo,delim: x offset * delim; default is '    '
        """
        if offset >= 0:
            xo = delim * offset
        else:
            curses.setsyx(self.find_curs()[0], self.find_curs()[1] + offset)
            xo = ""
        if style:
            if style == "ok":
                self._okprint(xo, data)
            elif style == "fail":
                self._badprint(xo, data)
            elif style == "warn":
                self._warnprint(xo, data)
            elif style == "good":
                self._goodprint(xo, data)
            elif style == "onbar":
                self._onbar(xo, data)
        else:
            self.window.addstr(xo + data)
        self.window.addstr(end)
        self.reload()

    def getstr(self,
               prompt: str = None,
               offset: int = 4
               ):
        """ Get a string from the user until \n. Like input()"""
        if prompt is None:
            self.window.addstr(curses.getsyx()[0] - 1, curses.getsyx()[1], "")
            self.reload()
        else:
            self.cprint("{}".format(prompt), end="", offset=offset)
        ## sleep 400ms to prevent double-pressed carriage returns from skipping the next prompt
        curses.napms(400)
        x = self.window.getstr()
        return x.decode()

    def getfield(self,
                 xpos,
                 lineno=None) -> str:
        """
        :param xpos: Position to place the cursor, as offset from 0 on X-Axis
        :param lineno: Position in the Y axis to place the line. If :lineno: not provided,
        getst the field starting at the current x, y position of the cursor.
        :return: The user's input into this field, as a string.
        """
        if not lineno:
            lineno = curses.getsyx()[0] - 1
        s = ""
        curses.noecho()
        while True:

            k = self.window.getch()
            s += chr(k)
            if k == 13 or k == 10:
                break

            if k == 8 or k == 127:
                self.cprint("  ", end="", offset=-2, style="onbar")
            else:
                s += k
                self.cprint(k, end="", offset=0, style="onbar")
            self.window.refresh()

        self.cprint("")
        curses.echo()
        return

    def getch(self,
              prompt: str = None,
              offset: int = 0
              ):
        """ Recieve a single character of input and immediately return, like getch """
        ## sleep 400ms to prevent double-pressed carriage returns from skipping the next prompt
        curses.napms(400)
        if prompt is not None:
            self.cprint(prompt, end="")
        x = self.window.getkey()
        return x

    def find_curs(self):
        """ Get the present Y, X position of the cursor. """
        y, x = curses.getsyx()
        return y, x

    def get_window_size(self):
        """ Return the current window size as y,x tuple. """
        return (self.dimensions["h"], self.dimensions["w"])

    def colored_prompt(self, masked=False):
        self.suppress_echo()
        ystart, xstart = self.find_curs()
        s = ""
        while True:

            k = self.window.getch()
            s += chr(k)
            if k == 13 or k == 10:
                break
            if k == 8 or k == 127:
                self.window.addstr("\b \b", curses.color_pair(5))
                s = s[:-2]
                self.reload()
                continue
            else:
                self.cprint(chr(k) if not masked else "*", offset=0, end="", style="good")
                self.window.refresh()
        self.enable_echo()
        self.cprint("\n")
        return s.strip("\n")

    def enable_color(self):
        curses.start_color()

    def suppress_echo(self):
        curses.noecho()

    def enable_echo(self):
        curses.echo()

    def validate_address(self, address: str, allow_blank=False) -> bool:
        """
        Determine if this is a valid IPv4 address or mask. Non-CIDR only
        :param address: non-cidr string
        :return: True if good, False if bad
        """
        if allow_blank is True and len(address.strip()) == 0:
            return True
        splitted = address.split(".")
        if len(splitted) != 4:
            self.cprint("Bad address: {} - improper length.".format(address))
            return False
        else:
            for i in splitted:
                try:
                    x = int(re.sub("[^0-9]", "", i))
                    if x > 255 or int(x) < 0:
                        self.cprint("Bad address:  bad octet -> {} <- ".format(i))
                        return False
                except ValueError as e:
                    self.cprint(
                        "Bad address: Invalid/non-convertible IPv4 octet -> {} <- (type: {}) in {}".format(i, type(i),
                                                                                                           address))
                    return False
                except TypeError as e:
                    self.cprint("Error in IP address syntax: {} - bad address: {}".format(e, address))
                    return False
        return True

class _Color:
    colors = {
        "blue": curses.COLOR_BLUE,
        "black": curses.COLOR_BLACK,
        "green": curses.COLOR_GREEN,
        "red": curses.COLOR_RED,
        "yellow": curses.COLOR_YELLOW
    }

    def get_color(self, c):
        if c in self.colors:
            return self.colors[c]


class SnapIn(object):
    screen_object = None
    window_object = None
#
#
# class LoginWindow(SnapIn):
#
#     """
#     +-----------------------------
#     |   Login: __bilbo_______________
#     |
#     |   Password: __bagend69____________
#     |
#     |
#     +------------------------------
# """
#
#     def __init__(self):
#         if self.window_object is not None and self.screen_object is not None:
#             pass
#         else:
#             self.screen = curses.initscr()
#             curses.start_color()
#             self.cp = curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
#             self.screen.scrollok(True)
#             self.win = curses.newwin( 10, 60, 1, 2)
#             self.colors = _Color()
#             self.construct_frames()
#
#     def colorprompt(self, ypos, xoffset):
#         x = ""
#         while True:
#
#             curses.noecho()
#             a =  self.win.getkey()
#             curses.echo()
#             x += a
#             self.win.addstr(ypos, xoffset, a , curses.color_pair(1))
#
#             xoffset+=1
#             if "\n" in x:
#                 break
#         self.win.addstr(ypos+2, 4, "")
#         self.reload()
#         return x
#
#     def reload(self):
#         self.win.border(0)
#         self.win.refresh()
#         self.win.border(0)
#
#     def create_color_pair(self, fg, bg="black"):
#         pair = curses.init_pair(self.colors.get_color(fg), self.colors.get_color(bg))
#         return pair
#
#     def construct_frames(self):
#         ## LOGIN - LINE 4
#         ## PASSWORD - LINE 5
#
#         self.win.addstr( 4, 4, "Login: ")
#         self.win.addstr( 5, 4, "Password: ")
#         self.reload()
#         self.win.addstr(4, 20, "")
#         x = self.input_user()
#         y = self.input_password()
#         time.sleep(3)
#         return x, y
#
#     def input_user(self):
#         self.reload()
#         #login = self.win.getstr(4, 20, curses.color_pair(1))
#         login = self.colorprompt(4, 20)
#         self.win.addstr(4, 20, "")
#         return login
#
#     def input_password(self):
#         p = ""
#         index = 20
#         while True:
#             key = self.win.getkey()
#             p += key
#             self.win.addstr(5, index + len(p), "*", curses.color_pair(1))
#             if "\n" in p:
#                 break
#         return p
#
#
def force_unload():
    curses.endwin()


#
#
import atexit

atexit.register(force_unload)
