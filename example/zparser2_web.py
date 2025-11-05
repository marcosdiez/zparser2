#!/usr/bin/env python3
"""description of the __main__ module"""

# flask --app hello run --host 0.0.0.0 --reload

from flask import Flask, stream_with_context, request
from zparser2.web import zparser2_web_init
from zparser2 import z, zparser2_init, __version__ as zparser2_version
import math_functions
import string_functions


@z.task
def say_hello(name: str):
    """this is a function on the main file"""
    z.print(f"Hello {name}, welcome to zparser2 {zparser2_version} !")

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    if request.path == "/favicon.ico":
        return "File not found", 404

    return stream_with_context(
        zparser2_web_init(request.path, [], __name__)
    )


if __name__ == "__main__":
    zparser2_init()
else:
    print(f"This is zparser2 {zparser2_version} am running on flask [{__name__}]")

