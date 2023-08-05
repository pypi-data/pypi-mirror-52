# -*- coding: utf-8 -*-
# Pretty ~ Useful ~ Python

from typing import Any
from typing import Iterator
from typing import List
from typing import Optional

from pupy._typing import Flint

def nbytes(num: Flint) -> str: ...
def filesize(filepath: str) -> str: ...
def nseconds(t1: float, t2: Optional[float] = ...) -> str: ...
def term_table(
    strings: List[str], row_wise: bool = ..., filler: str = ...
) -> Iterator[Any]: ...
def bytes2str(bites: bytes, encoding: str = ...) -> str: ...
def binary_string(number: int) -> str: ...
def strip_comments(string: str) -> str: ...
def strip_ascii(s: str) -> str: ...
def no_b(string: str) -> str: ...
def no_u(string: str) -> str: ...
def rhex_str(length: int = ...) -> str: ...
