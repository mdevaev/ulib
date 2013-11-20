import os
import sys
import struct


##### Public methods #####
def colored(codes_list, text, force_colors_flag = False, raw_flag = False, output = sys.stdout) :
    # XXX: See man 4 console_codes. UNIX-only.

    if (output.isatty() or force_colors_flag) and os.name == "posix" :
        if not isinstance(codes_list, (list, tuple)) :
            codes = str(codes_list)
        else :
            codes = ";".join(map(str, codes_list))
        # XXX: \033 == \x1b
        colored_tuple = ("\x1b[%sm" % (codes), text, "\x1b[0m")
    else :
        colored_tuple = ("", text, "")
    return ( colored_tuple if raw_flag else "".join(colored_tuple) )


###
def terminalSize(min_columns = 80, min_lines = 24, default_columns = 80, default_lines = 24, output = sys.stdout) :
    # XXX: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python

    (columns, lines) = __environTerminalSize(output)
    if columns > 0 and lines > 0 :
        return (columns, lines)

    method = {
        "posix" : __posixTerminalSize,
        "nt"    : __ntTerminalSize,
    }.get(os.name)
    if method is None :
        return (default_columns, default_lines)

    (columns, lines) = method(output)
    if columns <= 0 or lines <= 0 :
        return (default_columns, default_lines)

    return (max(columns, min_columns), max(lines, min_lines))


##### Private methods #####
def __environTerminalSize(output) :
    try :
        return (int(os.environ["COLUMNS"]), int(os.environ["LINES"]))
    except (KeyError, ValueError) :
        return (0, 0)

def __posixTerminalSize(output) :
    import fcntl
    import termios

    gwinsz = struct.pack("HHHH", 0, 0, 0, 0)
    try :
        gwinsz = fcntl.ioctl(output.fileno(), termios.TIOCGWINSZ, gwinsz)
    except Exception :
        pass
    (lines, columns) = struct.unpack("HHHH", gwinsz)[:2]
    return (columns, lines)

def __ntTerminalSize(output) :
    import ctypes

    if output == sys.stdin :
        handle = -10
    elif output == sys.stdout :
        handle = -11
    elif output == sys.stderr :
        handle = -12
    else :
        raise RuntimeError("Unsupported output: %s" % (output))

    try :
        handle = ctypes.windll.kernel32.GetStdHandle(handle)
        csbi = ctypes.create_string_buffer(22)
        res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        if res :
            (left, top, right, bottom) = struct.unpack("hhhhHhhhhhh", csbi.raw)[5:9]
            columns = right - left + 1
            lines = bottom - top + 1
            return (columns, lines)
        return (0, 0)
    except Exception :
        return (0, 0)

