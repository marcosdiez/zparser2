#!/usr/bin/env python3
"""description of the __main__ module"""
from zparser2 import z, zparser2_init, __version__ as zparser2_version
print(zparser2_version)

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
    zparser2_init(["plugins",])
