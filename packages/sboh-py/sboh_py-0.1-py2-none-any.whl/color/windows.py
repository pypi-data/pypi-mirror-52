import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


class Back:
    BLUE = 0x10  # background color contains blue.
    GREEN = 0x20  # background color contains green.
    RED = 0x40  # background color contains red.
    INTENSITY = 0x80  # background color is intensified.


class Fore:
    BLACK = 0x00
    BLUE = 0x01  # text color contains blue.
    GREEN = 0x02  # text color contains green.
    RED = 0x04  # text color contains red.
    YELLOW = RED | GREEN
    INTENSITY = 0x08  # text color is intensified.


def set_color(color, handle=std_out_handle):
    isChanged = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return isChanged


def remove_color():
    sys.stdout.flush()


def print_error(msg: str = "Error"):
    set_color(Fore.RED)
    print(msg)


def print_warning(msg: str = "Warning"):
    set_color(Fore.YELLOW)
    print(msg)


def print_debug(msg: str = "Debug"):
    set_color(Fore.GREEN)
    print(msg)


def print_info(msg: str = "Info"):
    set_color(Fore.BLUE)
    print(msg)
