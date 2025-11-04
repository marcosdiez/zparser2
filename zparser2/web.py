import threading
import queue

from . import z, Printer, ZExitException


class WebPrinter(Printer):
    END_BOLD = "</b>"
    END_RED = "</font>"
    BOLD = "<b>"
    RED = "<font color='red'>"

    def init(self):
        self.running = True
        self.q = queue.SimpleQueue()
        self.print("<pre>\n")

    def display(self):
        yield self.q.get()

    def print(self, msg: str):
        # print(f"WebPrinter({msg})")
        self.q.put(msg)

    def make_url(self, name: str):
        return f"<a href='{name}/'>{name}</a>"


def process_path(request_path: str):
    result = []
    for elem in request_path.split("/"):
        if elem != "":
            result.append(elem)
    return result


def zparser2_run(request_path: str):
    # argv = request_path.split("/")[1:]
    argv = process_path(request_path)
    argv = ["zparser_web"] + argv
    # print(argv)
    try:
        z.parse(argv).run()
    except ZExitException as e:
        print(f"ZExitException(e={e})")
    z.printer.running = False


def zparser2_web_init(request_path: str, plugin_list: list = []):
    z.printer.__class__ = WebPrinter  # yes, we monkeypatch !
    z.printer.init()
    z.set_plugin_module(plugin_list)

    t = threading.Thread(target=zparser2_run, args=[request_path])

    t.start()

    while z.printer.running or not z.printer.q.empty():
        for msg in z.printer.display():
            yield f"{msg}\n"
