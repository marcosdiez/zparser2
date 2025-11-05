#!/usr/bin/env python3
# flask --app hello run --host 0.0.0.0 --reload
# uwsgi --py-auto-reload 1 -s /tmp/uwsgi.socket --master -p 4 -w hello:app

"""description of the __main__ module"""

from flask import Flask, stream_with_context, request
from zparser2 import z, zparser2_init, __version__ as zparser2_version
from zparser2.web import zparser2_web_init

print(zparser2_version)

import local_module

# # # from werkzeug.middleware.proxy_fix import ProxyFix
# # # app.wsgi_app = ProxyFix(
# # #     app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
# # # )

@z.task
def task_on_the_main_file(
    somestring: str,
    some_int: int,
    some_float: float,
    some_boolean: bool,
    some_list=["aa", "bb", "cc"],
    favorite_number=42,
    my_float=4.5,
    workdir=None,
    a_true_boolean=True,
    a_false_boolean=False,
    workdir2: str = None,
    given_string="blah-bleh-blih",
    *vararg,
):
    "description of the task"
    z.print("this is the function task_on_the_main_file")
    z.print(f"somestring={somestring}")
    z.print(f"some_int={some_int}")
    z.print(f"some_float={some_float}")
    z.print(f"some_boolean={some_boolean}")
    z.print(f"some_list={some_list}")
    z.print(f"favorite_number={favorite_number}")
    z.print(f"my_float={my_float}")
    z.print(f"workdir={workdir}")
    z.print(f"a_true_boolean={a_true_boolean}")
    z.print(f"a_false_boolean={a_false_boolean}")
    z.print(f"workdir2={workdir2}")
    z.print(f"given_string={given_string}")
    z.print(f"vararg={vararg}")

@z.task
def sample(blah: str):
    return blah


@z.task
def another_task():
    return "This is just another task"


app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    if request.path == "/favicon.ico":
        return "File not found", 404

    return stream_with_context(
        zparser2_web_init(
            request.path,
            [
                "plugins",
            ],
            __name__
        )
    )


if __name__ == "__main__":
    import sys
    print(sys.argv)
    zparser2_init(["plugins"])
else:
    print(f"I am running on flask [{__name__}]")




