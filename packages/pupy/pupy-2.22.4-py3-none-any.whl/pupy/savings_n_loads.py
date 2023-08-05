# -*- coding: utf-8 -*-
# Pretty ~ Useful ~ Python
"""
===============
Savings & Loads
===============

Common funks for ur everyday savings and loads. 

If you are a friend of Jasm/Json/Jason-Greenberg like myself, 
'pip install ujson' for a better time.

If you need it... you can always...
pip install (msgpack, toml, ruamel.yaml) for the whole shebang.

"""

from codecs import getwriter
from io import open
from itertools import count
from os import path
from os import utime
from typing import Union

from pupy._jasm import json
from pupy._typing import JASM
from pupy.decorations import mkdirs

try:
    from toml import dumps as toml_dumps
    from toml import load as toml_load
    from toml import loads as toml_loads
except ModuleNotFoundError:
    pass

try:
    from msgpack import pack
    from msgpack import unpack
except ModuleNotFoundError:
    pass

try:
    from ruamel.yaml import YAML

    _yaml_saver = YAML()
    _yaml_loader = YAML(typ="safe")
except ModuleNotFoundError:
    pass


def safepath(path_str: str) -> str:
    """Checks if a file/dir path is save/unused; returns an unused path.

    :param path_str: file or dir path
    :return: A file/dir path that does not exist and contains the given path

    """
    if path.exists(path_str):
        f_bn, f_ext = path.splitext(path_str)
        for n in count(1):
            safe_save_path = f_bn + "_({}).".format(str(n)) + f_ext
            if not path.exists(safe_save_path):
                return safe_save_path
    return path_str


def lbytes(filepath: str) -> Union[bytes, bytearray]:
    """Read bytes from file path

    :param filepath: filepath as as string to read bites from
    :return: some bytes...

    """
    with open(filepath, "rb") as file:
        return file.read()


def sbytes(filepath: str, bytes: Union[bytes, bytearray]) -> None:
    """Write bytes to a filepath

    :param filepath: filepath as as string to read bites from
    :param bytes:
    :return: some bytes...

    """
    with open(filepath, "wb") as file:
        return file.write(bytes)


@mkdirs
def sstring(filepath: str, string: str) -> None:
    """Writes a string to filepath


    :param filepath: Filepath save location
    :param string: File as a string to be saved
    :return: None? what do you want? confirmation?

    .. note:: Decorated w/ @mkdirs
        Function is decorated with @mkdirs decorator; @mkdirs creates parent
        directories for the given filepath if they do not already exist.

    """
    with open(filepath, "wb") as file:
        file.write(string.encode("utf-8"))


def savings(filepath: str, string: str) -> None:
    """Alias for sstring"""
    return sstring(filepath, string)


def sstr(filepath: str, string: str) -> None:
    """Alias for sstring"""
    return sstring(filepath, string)


def lstring(filepath: str) -> str:
    """(lstring) Read and return the file-contents as a string given a filepath

    :param filepath: Path to a file to read
    :return: Content of the file read as a string

    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding="latin2") as f:
            return f.read()


def lstr(filepath: str) -> str:
    """Alias for lstring"""
    return lstring(filepath)


@mkdirs
def sjson(filepath: str, data: JASM, minify: bool = False) -> None:
    """Save json-serial-ize-able data to a specific filepath.

    :param filepath: destination filepath
    :param data: json cereal-izable dictionary/list/thing
    :param minify: Bool flag -- minify the json file
    :return: None

    """
    if isinstance(data, dict) and any(isinstance(val, bytes) for val in data.values()):
        data = {k: str(v, encoding="utf-8") for k, v in data.items()}
    if minify:
        json_string = json.dumps(data, ensure_ascii=True)
    else:
        json_string = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=True)
    sstring(filepath, json_string)


def save_jasm(filepath: str, data: JASM, minify: bool = False) -> None:
    """Alias for sjson (which stands for 'save-json')"""
    return sjson(filepath, data, minify)


def sjasm(filepath: str, data: JASM, minify: bool = False) -> None:
    """Alias for sjson (which stands for 'save-json')"""
    return sjson(filepath, data, minify)


def ljson(filepath: str) -> JASM:
    """Load a json file given a filepath and return the file-data

    :param filepath: path to the jasm file you want to load
    :return: Loaded file contents
    """
    try:
        with open(filepath) as infile:
            return json.load(infile)
    except UnicodeDecodeError as e:
        return json.loads(lstring(filepath))


def load_jasm(filepath: str) -> JASM:
    """Alias for ljson (which stands for 'load-json')"""
    return ljson(filepath)


def ljasm(filepath: str) -> JASM:
    """Alias for ljson (which stands for 'load-json')"""
    return ljson(filepath)


@mkdirs
def touch(filepath: str) -> None:
    """Touches a file just like touch on the command line

    :param filepath: filepath to 'touch' in a unix-y sense
    :return: None
    """
    with open(filepath, "a"):
        utime(filepath, None)


def shebang(filepath: str) -> Union[None, str]:
    """returns the shebang path given a filepath or None if it does not exist.

    :param filepath: path to a file w/ a shebange line
    :return: shebang line or None

    .. doctest::python

        >>> from inspect import getabsfile
        >>> script = 'ashellscript.sh'
        >>> with open(script, 'w') as f:
        ...     f.write('#!/bin/bash\\necho "howdy"\\n')
        25
        >>> shebang(script)
        '#!/bin/bash'
        >>> from os import remove
        >>> remove(script)

    """
    with open(filepath, "r") as f:
        first = f.readline().strip("\n")
        return first if "#!" in first[:2] else None


def stoml(filepath: str, data: JASM) -> None:
    try:
        filepath = filepath if "." in filepath else "{}.toml".format(filepath)
        sstring(filepath, toml_dumps(data))
        return filepath
    except NameError:
        raise EnvironmentError("'pip install toml' if you wanna use this!")


def ltoml(filepath: str) -> JASM:
    try:
        with open(filepath) as f:
            return toml_load(f)
    except NameError:
        raise EnvironmentError("'pip install toml' if you wanna use this!")
    except UnicodeDecodeError as e:
        return toml_loads(lstring(filepath))


def spak(filepath: str, data: JASM) -> None:
    try:
        filepath = filepath if "." in filepath else "{}.pak".format(filepath)
        with open(filepath, "wb") as outfile:
            pack(data, outfile)
        return filepath
    except NameError:
        raise EnvironmentError("'pip install msgpack' if you wanna use this!")


def lpak(filepath: str, raw: bool = False) -> JASM:
    try:
        with open(filepath, "rb") as data_file:
            return unpack(data_file, raw=raw)
    except NameError:
        raise EnvironmentError("'pip install msgpack' if you wanna use this!")


def syaml(filepath: str, data: JASM) -> None:
    try:
        filepath = filepath if "." in filepath else "{}.yml".format(filepath)
        with open(filepath, "w") as data_file:
            _yaml_saver.dump(data, data_file)
        return filepath
    except NameError:
        raise EnvironmentError("'pip install ruamel.yaml' if you wanna use this!")


def lyaml(filepath: str) -> JASM:
    try:
        with open(filepath) as data_file:
            return _yaml_loader.load(data_file)
    except NameError:
        raise EnvironmentError("'pip install ruamel.yaml' if you wanna use this!")
