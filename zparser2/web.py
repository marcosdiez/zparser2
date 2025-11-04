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

    def args_section_begin(self):
        self.print("<form>")

    def args_section_end(self):
        self.print("</form>")

    def args_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th></th><th>Description</th><th>Value</th>")

    def args_end(self):
        self.print("</table>")

    def optional_args_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th><th>Default Value</th><th>Description</th><th>Value</th>")

    def optional_args_end(self):
        self.print("</table>")

    def varargs_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th></th><th>Description</th><th>Value</th>")

    def varargs_end(self):
        self.print("</table>")

    def print_argument(self, arg):

        arg_type_text = f"{arg.type}".replace("<", "&lt;").replace(">", "&gt;")

        default_value_text = ""
        if arg.has_default and arg.default is not None:
            default_value_text = f' value="{arg.default}" '

        if arg.type is int:
            form_value =f'<input type="number" step="1" name="{arg.name}" {default_value_text} />'
        elif arg.type is float:
            form_value =f'<input type="number"          name="{arg.name}" {default_value_text} />'
        else:
            form_value =f'<input type="text"            name="{arg.name}" {default_value_text} />'

        if arg.has_default:
            self.print(f"<tr><th>{arg.name}</th><td>{arg_type_text}</td><td>{arg.default}</td><td>{arg.short_help}</td><td>{form_value}</td></tr>")
        else:
            self.print(f"<tr><th>{arg.name}</th><td>{arg_type_text}</td><td>{arg.short_help}</td><td>{form_value}</td></tr>")


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
