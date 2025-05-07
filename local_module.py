"""
description of the local module
"""

from zparser2 import z

alias = ["xibrapz"]


@z.task
def task_on_a_local(somestring: str, some_int: int, workdir=None, root_url=None):
    "description of the task"
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")
