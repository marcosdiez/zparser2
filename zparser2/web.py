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
        self.print("<!DOCTYPE html><html><style>a { text-decoration: none; }</style><pre>")

    def end(self):
        self.print("</pre></html>")
        self.running = False

    def display(self):
        yield self.q.get()

    def print(self, msg: str):
        # print(f"WebPrinter({msg})")
        # self.q.put(f"[{msg}]")
        self.q.put(msg)

    def make_url(self, name: str):
        return f"<a href='{name}/'>{name}</a>"

    def make_prog_url(self, name):
        return f"<a href='../'>{name}</a>"

    def make_prog_url2(self, name):
        return f"<a href='../../'>{name}</a>"

    def make_plugin_url(self, name):
        return f"<a href='../'>{name}</a>"


    def args_section_begin(self):
        self.print("<form name='one'>")

    def args_section_end(self):
        self.print("""<script>
        function buildParametersFromForm(){
            var output = ""
            for ( const elem of document.one.elements ) {
                if ( elem.name == "submit_button" ){
                    continue;
                }
                if ( elem.type == "checkbox" ) {
                    output += elem.checked + "/";
                } else {
                    output += elem.value + "/";
                }
            }
            return output;
        }

        function submitForm(){
            const url_sufix = buildParametersFromForm()
            var new_url = location.href;
            if ( new_url[ new_url.length -1] != "/" ) {
                new_url += "/";
            }
            new_url += url_sufix;
            // alert(new_url);
            location.href = new_url;
            return false;
        }
        </script><input type="button" onclick="submitForm()" name='submit_button' value="Run" />
        </form>
        """)

    def args_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th><th>Description</th><th>Value</th></tr>")

    def args_end(self):
        self.print("</table>")

    def optional_args_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th><th>Default Value</th><th>Description</th><th>Value</th></tr>")

    def optional_args_end(self):
        self.print("</table>")

    def varargs_begin(self):
        self.print("<table border=1>")
        self.print(f"<tr><th>Argument Name</th><th>Type</th><th>Description</th><th>Value</th></tr>")

    def varargs_end(self):
        self.print("</table>")

    def print_argument(self, arg):
        arg_type_text = f"{arg.type}".replace("<", "&lt;").replace(">", "&gt;")

        default_value_text = ""
        if arg.has_default and arg.default is not None:
            if isinstance(arg.default, list):
                default_value_text = ""
                for i in range(0, len(arg.default)):
                    default_value_text += f"{arg.default[i]}"
                    if i != len(arg.default) -1:
                        default_value_text += ","
                default_value_text = f' value="{default_value_text}" '
            else:
                default_value_text = f' value="{arg.default}" '

        if arg.type is int:
            form_value =f'<input type="number" step="1" name="{arg.name}" {default_value_text} />'
        elif arg.type is float:
            form_value =f'<input type="number"          name="{arg.name}" {default_value_text} />'
        elif arg.type is bool:
            checked = ""
            if arg.has_default and arg.default:
                checked = " checked "
            form_value =f'<input type="checkbox"        name="{arg.name}" {checked} />'
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


def zparser2_run(request_path: str, plugin_list: list):
    argv = process_path(request_path)
    argv = ["zparser_web"] + argv

    global z
    try:
        z.parse(argv).run()
    except ZExitException as exit_exception:
        pass
    z.printer.running = False



def zparser2_web_init(request_path: str, plugin_list: list = []):
    z.printer.__class__ = WebPrinter  # yes, we monkeypatch !
    z.printer.init()
    z.set_plugin_module(plugin_list)

    threading.Thread(target=zparser2_run, args=[request_path, plugin_list]).start()

    while z.printer.running or not z.printer.q.empty():
        for msg in z.printer.display():
            yield f"{msg}\n"
