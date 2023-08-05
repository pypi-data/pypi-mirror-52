# -*- coding: utf-8 -*-
# Pretty ~ Useful ~ Python
from contextlib import contextmanager
from datetime import datetime
from inspect import stack
from os import environ
from os import makedirs
from os import path
from shutil import rmtree
from tempfile import mkdtemp
from time import time
from typing import Any
from typing import Optional

from pupy._alias import pp
from pupy.sh import cd
from pupy.sh import link_dirs
from pupy.sh import link_files
from pupy.sh import unlink_dirs
from pupy.sh import unlink_files


def timestamp(ts: Optional[float] = None) -> str:
    """Time stamp string w/ format yyyymmdd-HHMMSS

    :return: timestamp string

    .. doctest:: python

        >>> from datetime import datetime
        >>> stamps = ['20190225-161151', '20190225-081151']
        >>> timestamp(1551111111.111111) in stamps
        True
        >>> datetime.now().strftime("%Y%m%d-%H%M%S") == timestamp()
        True
        >>> timestamp(datetime.now()) == timestamp()
        True

    """
    if ts is None:
        return datetime.now().strftime("%Y%m%d-%H%M%S")
    elif isinstance(ts, float):
        return datetime.fromtimestamp(ts).strftime("%Y%m%d-%H%M%S")
    elif isinstance(ts, datetime):
        return ts.strftime("%Y%m%d-%H%M%S")


def environ_dict():
    return {k: environ[k] for k in environ}


@contextmanager
def linked_tmp_dir(
    suffix=None, prefix=None, dir=None, mkdirs=[], lndirs=[], lnfiles=[]
):
    temp_dir = mkdtemp(suffix, prefix, dir)
    lnfiles = [
        (path.join(temp_dir, _rel_link), target) for _rel_link, target in lnfiles
    ]
    lndirs = [(path.join(temp_dir, _rel_link), target) for _rel_link, target in lndirs]
    # print(mkdirs)
    _dirs2make = [
        path.join(temp_dir, e)
        for e in (
            dirpath if isinstance(dirpath, str) else path.join(*dirpath)
            for dirpath in mkdirs
        )
    ]
    _dirs2make.extend((path.split(link)[0] for link, target in lnfiles))
    _dirs2make.extend((path.split(link)[0] for link, target in lndirs))
    for dirpath_route in _dirs2make:
        # print("mkingdir", dirpath_route)
        makedirs(path.join(temp_dir, dirpath_route), exist_ok=True)

    link_files(lnfiles)
    link_dirs(lndirs)
    # from pupy.foreign import files_gen, dirs_gen
    # from pprint import pprint
    # pprint(list(files_gen(temp_dir)))
    # pprint(list(dirs_gen(temp_dir)))
    # try:
    #     lndirs = (
    #         (path.join(temp_dir, _rel_link), target) for _rel_link, target in lndirs
    #     )
    # except TypeError as e:
    #     pass
    try:
        yield temp_dir
    finally:
        try:
            unlink_files(lnfiles)
        except Exception as e:
            pass
        try:
            unlink_dirs(lndirs)
        except Exception as e:
            pass
        try:
            rmtree(temp_dir)
        except PermissionError:
            # sleep(3)
            # print(pwd())
            # print(temp_dir)
            cd("..")
            # print(pwd())
            rmtree(temp_dir)


def prinfo(obj: Any) -> None:
    try:
        pp({"object": obj, "type": obj})
    except:
        print("object:\n{}".format(obj))
        print("type:\n{}".format(type(obj)))


def pyfilepath(split=False):
    _filepath = path.abspath(stack()[1][1])
    if split:
        return path.split(_filepath)
    return _filepath


def time_funk(funk, *args, **kwargs):
    ti = time()
    _ret = funk(*args, **kwargs)
    tf = time()
    return _ret, tf - ti


def cmp_funks(f1, f2, runs=1, *args, **kwargs):
    f1_time = 0
    f2_time = 0
    for i in range(runs):
        r1, f1t = time_funk(f1, *args, **kwargs)
        f1_time += f1t
        r2, f2t = time_funk(f2, *args, **kwargs)
        f2_time += f2t
    f1_time = f1_time / runs
    f2_time = f2_time / runs
    return {
        "f1": str(f1.__name__),
        "f2": str(f2.__name__),
        "f1-time": f1_time,
        "f2-time": f2_time,
        "f1/f2": f1_time / f2_time,
    }


def time_funk(funk, *args, **kwargs):
    ti = time()
    _ret = funk(*args, **kwargs)
    tf = time()
    return _ret, tf - ti


def cmp_funks(f1, f2, runs, *args, **kwargs):
    f1_time = 0
    f2_time = 0
    for i in range(runs):
        r1, f1t = time_funk(f1, *args, **kwargs)
        f1_time += f1t
        r2, f2t = time_funk(f2, *args, **kwargs)
        f2_time += f2t
    f1_time = f1_time / runs
    f2_time = f2_time / runs
    return {
        "f1": str(f1.__name__),
        "f2": str(f2.__name__),
        "f1-time": f1_time,
        "f2-time": f2_time,
        "f1/f2": f1_time / f2_time,
        "runs": runs,
    }
