"""XPTa XPTb XPTc"""

from zparser2 import z

alias = ["p3"]


@z.task
def oonononono(somestring: str, some_int: int, workdir=None, root_url=None):
    "uga buga buga uga uga"
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")
