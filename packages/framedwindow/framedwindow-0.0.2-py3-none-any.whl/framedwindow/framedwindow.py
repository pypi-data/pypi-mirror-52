import curses
import time


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
    """ Loader: series of methods to bootstrap curses guis. """

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

        if kwargs:
            for key, value in kwargs.items():
                if key in self.dimensions.keys():
                    self.dimensions[key] = value
        # load stuff

        if  (("immediate" not in kwargs.keys()) or
                ( "immediate" in kwargs.keys() and kwargs["immediate"] == True)):
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
        win.setscrreg(self.dimensions["y"]+2, self.dimensions["h"] - self.dimensions["y"] - 2)
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
        self.window.setscrreg(self.dimensions["y"]+2, self.dimensions["h"] - self.dimensions["y"] - 2)
        self.cprint("\n")

    def reload(self):
        """ Flush the output buffer writing it to screen. Must call border before and after to keep the border. """
        ## do border twice in order to keep the lines.
        self.window.border(0)
        self.window.refresh()
        self.window.border(0)


    def _okprint(self, xo, data):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.window.addstr(xo + data, curses.color_pair(1))

    def _warnprint(self, xo, data):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
        self.window.addstr(xo + data, curses.color_pair(2))

    def _badprint(self, xo, data):
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_YELLOW)
        self.window.addstr(xo + data, curses.color_pair(3))


    def _goodprint(self, xo, data):
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
        self.window.addstr(xo + data, curses.color_pair(5))

    def place_bar(self,
                  xstart:int,
                  length:int,
                  linenumber=None,
                  cr=False):
        """
        Print a rectangle with no foreground chars and a blank white background.
        Useful for something like the background for a faux- username/password input field.
        """
        #get pos where we started, to return to after placing
        starting_position = curses.getsyx()
        spacer = " " * length
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
        self.window.addstr(curses.getsyx()[0], xstart, spacer, curses.color_pair(4))
        if cr:
            self.window.addstr("\n")
        # return to starting positon, then immediately flush the buffer to replace the cursor at start and print
        self.window.addstr(starting_position[0], starting_position[1], "")
        self.reload()
        time.sleep(1)



    def cprint(self,
               data: str,
               end: str = "\n",
               offset: int = 4,
               status=None,

               ):
        """ Print a string to the screen. Emulate print() behavior """
        xo = " " * offset
        if status:
            if status == "ok":
                self._okprint(xo, data)
            elif status == "fail":
                self._badprint(xo, data)
            elif status == "warn":
                self._warnprint(xo, data)
            elif status == "good":
                self._goodprint(xo, data)
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
            self.cprint("", end="", offset=offset)
        else:
            self.cprint("{}".format(prompt), end="", offset=offset)
        ## sleep 400ms to prevent double-pressed carriage returns from skipping the next prompt
        curses.napms(400)
        x = self.window.getstr()
        return x.decode()

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

    def _find_curs(self):
        """ Get the present Y, X position of the cursor. """
        y, x = self.window.getyx()
        return y, x

    def get_window_size(self):
        """ Return the current window size as y,x tuple. """
        return (self.dimensions["h"], self.dimensions["w"])




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
# def force_unload():
#     pass
#
#
# import atexit
# atexit.register(force_unload)
