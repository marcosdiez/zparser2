"""
BLA BLAH BLAH

bleh blih bloh bluh
"""

import sys
import os
from zparser2 import z


@z.task
def aaaa(somestring: str, some_int: int, workdir=None, root_url=None):
    "description of the function"
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")
