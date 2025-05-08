"""string processing"""
from zparser2 import z

@z.task
def add_square_brackets_to_string(x: str):
    """x -> [x]"""
    return f"[{x}]"

@z.task
def first_word(x: str):
    """returns the first word of a string"""
    return x.split(" ")[0]

@z.task
def last_word(x: str):
    """returns the first word of a string"""
    return x.split(" ")[-1]

@z.task
def another_task(somestring: str, some_int: int, workdir=None, root_url=None):
    """description of the task"""
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")
