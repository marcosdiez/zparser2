#!/usr/bin/env python3
# flask --app hello run --host 0.0.0.0 --reload
# uwsgi --py-auto-reload 1 -s /tmp/uwsgi.socket --master -p 4 -w hello:app

"""description of the __main__ module"""

from flask import Flask, stream_with_context, request
from zparser2 import z, zparser2_init, __version__ as zparser2_version
from zparser2.web import zparser2_web_init

print(zparser2_version)

import local_module


@z.task
def task_on_the_main_file(
    somestring: str,
    some_int: int,
    some_float: float,
    some_boolean: bool,
    some_list = ["aa", "bb", "cc"],
    favorite_number=42,
    my_float=4.5,
    workdir = None,
    a_true_boolean = True,
    a_false_boolean = False,
    workdir2 : str = None,
    root_url="http://blah",
    *vararg,
):
    "description of the task"
    print("this is task_on_the_main_file")
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"some_float={some_float}")
    print(f"some_list={some_list}")
    print(f"favorite_number={favorite_number}")
    print(f"my_float={my_float}")
    print(f"workdir={workdir}")
    print(f"workdir2={workdir2}")
    print(f"root_url={root_url}")
    print(f"vararg={vararg}")


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
        )
    )


if __name__ == "__main__":
    zparser2_init(
        [
            "plugins",
        ]
    )
else:
    print(f"I am running on flask [{__name__}]")


# import sample


# # # from werkzeug.middleware.proxy_fix import ProxyFix
# # # app.wsgi_app = ProxyFix(
# # #     app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
# # # )


# # @z.task
# # def sample(blah):
# #     return blah


# # @z.task
# # def another_task():
# #     return "This is just another task"
