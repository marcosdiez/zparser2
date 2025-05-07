"""
BLA BLAH BLAH

bleh blih bloh bluh
"""

import sys
import os
expected_python_path = os.path.abspath(os.path.dirname((os.path.abspath(__file__))) + os.sep + ".." + os.sep + "..")
sys.path.append(expected_python_path)
from zparser.zparser import z

@z.task
def aaaa(tenant_name, workdir=None, root_url=None):
    "description of the function"
    pass
