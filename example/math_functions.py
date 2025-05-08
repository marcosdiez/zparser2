"""here we do math"""
from zparser2 import z

@z.task
def duplicate_number(x: float):
    """returns twice the value of x"""
    return 2*x

@z.task
def triple_number(x: float):
    """returns 3 times the value of x"""
    return 3*x

