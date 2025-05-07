from docutils import nodes
from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import ViewList
import functools
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.compat import Directive

def scan_zparser(parser, plugin_name):
    for p in [p for p in parser.plugins.values() if not plugin_name or p.name == plugin_name ]:
        for task in p.tasks.values():
            yield p, task

def import_object(import_name):
    module_name, expr = import_name.split(':', 1)
    mod = __import__(module_name)
    reduce_ = getattr(functools, 'reduce', None) or reduce
    mod = reduce_(getattr, module_name.split('.')[1:], mod)
    globals_ = builtins
    if not isinstance(globals_, dict):
        globals_ = globals_.__dict__
    return eval(expr, globals_, mod.__dict__)

class AutoZParserDirective(Directive):

    has_content = False
    required_arguments = 1
    option_spec = {'prog': unchanged, 'plugin': unchanged}

    def make_rst(self):
        import_name, = self.arguments
        parser = import_object(import_name or '__undefined__')
        plugin = self.options.get('plugin', None)
        prog = 'wcli' #TODO don't hardcode that
        for plugin in parser.plugins.values():
            title = '{0} {1}'.format(prog, plugin.name).rstrip()
            yield '.. program:: ' + title
            yield title
            yield ('?') * len(title)
            yield plugin.help
            for task in plugin.tasks.values():
                title = '{0} {1} {2}'.format(prog, plugin.name, task.name).rstrip()
                yield ''
                yield '.. program:: ' + title
                yield ''
                yield title
                yield ('!' if task else '?') * len(title)
                yield ''
                yield task.help
                yield ''
                for arg in task.args:
                    yield '.. option:: {0} - {1}'.format(arg.name, arg.short_help)
                for arg in task.optional_args:
                    arg_name = "--{}".format(arg.name)
                    if arg.short:
                        arg_name = "{}/-{}".format(arg_name, arg.short)
                    yield (".. option:: {} (Default: {}) - {}".format(arg_name, arg.default, arg.short_help))

    def run(self):
        node = nodes.section()
        node.document = self.state.document
        result = ViewList()
        for line in self.make_rst():
            result.append(line, '<autozparser>')
        nested_parse_with_titles(self.state, result, node)
        return node.children

def setup(app):
    app.add_directive('autozparser', AutoZParserDirective)
