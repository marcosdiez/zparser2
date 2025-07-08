#!/usr/bin/env python3
"""description of the __main__ module"""
from zparser2 import z, zparser2_init
import math_functions
import string_functions


@z.task
def say_hello(name: str):
    """this is a function on the main file"""
    print(f"Hello {name}, welcome to zparser 2!")

if __name__ == "__main__":
    zparser2_init()
