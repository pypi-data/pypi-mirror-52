# -*- coding: utf-8 -*-
# Pretty ~ Useful ~ Python
from binascii import hexlify
from math import ceil
from os import path
from os import stat
from os import urandom
from re import compile as _compile
from re import sub
from shutil import get_terminal_size
from string import printable
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional

from pupy._typing import Flint


def nbytes(num: Flint) -> str:
    """
    this function will convert bytes to MB.... GB... etc

    .. doctest:: python

        >>> nbytes(100)
        '100.0 bytes'
        >>> nbytes(1000)
        '1000.0 bytes'
        >>> nbytes(10000)
        '9.8 KB'
        >>> nbytes(100000)
        '97.7 KB'
        >>> nbytes(1000000)
        '976.6 KB'
        >>> nbytes(10000000)
        '9.5 MB'
        >>> nbytes(100000000)
        '95.4 MB'
        >>> nbytes(1000000000)
        '953.7 MB'
        >>> nbytes(10000000000)
        '9.3 GB'
        >>> nbytes(100000000000)
        '93.1 GB'
        >>> nbytes(1000000000000)
        '931.3 GB'
        >>> nbytes(10000000000000)
        '9.1 TB'
        >>> nbytes(100000000000000)
        '90.9 TB'

    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def filesize(filepath: str) -> str:
    """this function will return the file size

    :param filepath:
    :return:
    """
    if path.isfile(filepath):
        file_info = stat(filepath)
        return nbytes(file_info.st_size)


def nseconds(t1: float, t2: Optional[float] = None) -> str:
    """Formats time string

    Formats t1 if t2 is None as a string; Calculates the time and formats
    the time t2-t1 if t2 is not None.

    :param t1: time 1/initial in seconds
    :type t1: double
    :param t2: time 2 (Default value = None)
    :type t2: None or double
    :returns: formated string of the t1 - t2 or t1
    :rtype: str

    """
    if t2 is not None:
        return nseconds((t2 - t1))
    elif t1 == 0.0:
        return "0 sec"
    elif 0.000001 > t1 >= 0.000000001:
        return "%.3f ns" % ((10 ** 9) * t1)
    elif 0.001 > t1 >= 0.000001:
        return "%.3f μs" % ((10 ** 6) * t1)
    elif 1 > t1 >= 0.001:
        return "%.3f ms" % ((10 ** 3) * t1)
    return "%.3f sec" % t1


def term_table(
    strings: List[str], row_wise: bool = False, filler: str = "~"
) -> Iterator[Any]:
    """

    :param strings:
    :param row_wise:
    :param filler:
    :return:
    """
    max_str_len = max(len(str) for str in strings) + 5
    terminal_cols = get_terminal_size((80, 20)).columns
    n_cols = terminal_cols // max_str_len
    n_rows = int(ceil(len(strings) / n_cols))
    spaces = " " * ((terminal_cols - (max_str_len * n_cols)) // n_cols)
    size_string = "{:<" + str(max_str_len) + "}" + spaces
    fmtstring = size_string * (n_cols - 1) + "{:<}"
    strings.extend(filler for _ in range(n_rows * n_cols - len(strings)))
    if row_wise:
        line_iter = zip(*(strings[i::n_cols] for i in range(n_cols)))
    else:
        line_iter = (strings[i::n_rows] for i in range(n_rows))
    return (fmtstring.format(*row) for row in line_iter)


def bytes2str(bites: bytes, encoding: str = "utf-8") -> str:
    """Convert bytes to a string

    :param bites: bytes
    :type bites: bytes
    :param encoding: encoding of the string (default is utf-8)
    :type encoding: str
    :return: converted bytes
    :rtype: str


    .. doctest:: python

        >>> a = b'abcdefg'
        >>> type(a)
        <class 'bytes'>
        >>> bytes2str(a)
        'abcdefg'
        >>> type(bytes2str(a))
        <class 'str'>

    """
    return bites.decode(encoding)


def binary_string(number: int) -> str:
    """Number to binary string

    :param number: some number (an integer) to turn into a binary string
    :return: Some string which is the binary string
    :rtype: str

    .. doctest:: python

        >>> binary_string(200)
        '11001000'
        >>> binary_string(10)
        '1010'

    """
    return bin(number)[2:]


def strip_comments(string: str) -> str:
    filelines = string.splitlines(keepends=False)
    r = _compile(r'(?:"(?:[^"\\]|\\.)*"|[^"#])*(#|$)')
    return "\n".join((line[: r.match(line).start(1)] for line in filelines))


def strip_ascii(s: str) -> str:
    """Remove all ascii characters from a string

    :param s: string with non-ascii characters
    :type s: string
    :return: string of only the non-ascii characters

    .. doctest::

        >>> string_w_non_ascii_chars = 'Three fourths: ¾'
        >>> strip_ascii(string_w_non_ascii_chars)
        '¾'

    """
    return "".join(sc for sc in (str(c) for c in s) if sc not in printable)


def no_b(string: str) -> str:
    """Removes the b'' from binary strings and sub-strings that contain b''

    :param string: A string surrounded by b'' or a sub-string with b''
    :return: A string without binary b'' quotes surround it

    .. doctest::

        >>> no_b("b'a_string'")
        'a_string'

    """
    return sub("b'([^']*)'", r"\1", string)


def no_u(string: str) -> str:
    """Removes the u'' from unicode strings and sub-strings that contain u''

    :param string: A string surrounded by u'' or a sub-string with u''
    :return: A string without unicode u'' quotes surround it

    .. doctest:: python

        >>> a = "u'a_string'"
        >>> no_u(a)
        'a_string'


    """
    return sub("u'([^']*)'", r"\1", string)


def rhex_str(length: int = 4) -> str:
    """Returns a random hex string

    :param length: length of random bytes to turn into hex (defaults to 4)
    :type length: int
    :return: random hexadecimal string
    :rtype: str

    .. doctest:: python

        >>> a = rhex_str()
        >>> isinstance(a, str)
        True
        >>> len(a) == 8
        True

    """
    return bytes2str(hexlify(urandom(length)))
