#!/usr/bin/env python3
"""description of the __main__ module"""
import zparser2
from zparser2 import z
print(zparser2.__version__)

import local_module


@z.task
def task_on_the_main_file(somestring: str, some_int: int, workdir=None, root_url=None):
    "description of the task"
    print("this is task_on_the_main_file")
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")


if __name__ == "__main__":
    zparser2.init(["plugins",])
