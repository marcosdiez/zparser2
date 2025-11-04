#!/usr/bin/env python3
import unittest
from zparser2 import z, Plugin, ArgumentOptional, Task, TaskAlreadyExistOnThisPluginException, __version__ as zversion, Printer


class TestZParser(unittest.TestCase):

    def _load_task(self, plugin, function, name=None, overwrite={}, short={}):
        z.plugins[plugin] = Plugin(plugin, Printer())
        z._register(plugin, function, name, overwrite, short)
        if name is None:
            name = function.__name__
        return z.plugins[plugin].tasks[name]

    def assertArgsValue(self, task, expected):
        self.assertEqual(task._args_value(), expected)

    def test_task_help(self):
        def my_func():
            """my help"""
            pass

        t = self._load_task("plug", my_func)

        # test help message
        self.assertEqual(t.help, "my help")


    def test_add_task_twice(self):
        def my_task():
            pass
        a_task = Task(my_task, "my_task", None, None, Printer())
        p = Plugin("a_plugin", Printer())
        p.add_task(a_task)

        with self.assertRaises(TaskAlreadyExistOnThisPluginException):
            p.add_task(a_task)


    def test_task_positional_arg(self):
        def my_func(arg1, arg2, arg3=None):
            """my help"""
            pass

        t = self._load_task("plug", my_func)

        self.assertEqual(len(t.all_args), 3)
        a1 = t.all_args[0]
        a2 = t.all_args[1]
        a3 = t.all_args[2]
        self.assertEqual(a1.name, "arg1")
        self.assertNotIsInstance(a1, ArgumentOptional)
        self.assertEqual(a2.name, "arg2")
        self.assertNotIsInstance(a2, ArgumentOptional)
        self.assertEqual(a3.name, "arg3")
        self.assertIsInstance(a3, ArgumentOptional)

    def test_parser_task(self):
        def my_func():
            pass

        t = self._load_task("plug", my_func)

        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertEqual(task, t)

    def test_parser_pos_arg(self):
        def my_func(arg1):
            pass

        self._load_task("plug", my_func)

        task = z.parse(["wcli.py", "plug", "my_func", "value1"])
        self.assertArgsValue(task, ["value1"])

    def test_parser_opt_arg(self):
        def my_func(arg1="value2"):
            pass

        self._load_task("plug", my_func)

        task = z.parse(["wcli.py", "plug", "my_func", "value1"])
        self.assertArgsValue(task, ["value1"])

        task = z.parse(["wcli.py", "plug", "my_func", "--arg1", "value1"])
        self.assertArgsValue(task, ["value1"])

        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertArgsValue(task, ["value2"])

    def test_parser_varargs(self):
        def my_func(*arg1):
            pass

        self._load_task("plug", my_func)

        task = z.parse(["wcli.py", "plug", "my_func", "value1", "value2"])
        self.assertArgsValue(task, ["value1", "value2"])

        # check if we can call parser twice and value are reinitialized
        task = z.parse(["wcli.py", "plug", "my_func", "value3", "value2"])
        self.assertArgsValue(task, ["value3", "value2"])

    def test_parser_mixed_args(self):
        def my_func(arg1, arg2=None, *arg3):
            pass

        self._load_task("plug", my_func)
        task = z.parse(
            ["wcli.py", "plug", "my_func", "value1", "value2", "value3", "value4"]
        )
        self.assertArgsValue(task, ["value1", "value2", "value3", "value4"])

    def test_parser_none_value(self):
        def my_func(arg0=False, arg1=None):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func", "--arg1", "value1"])
        self.assertArgsValue(task, [False, "value1"])

        # check if we can call parser twice and value are reinitialized
        task = z.parse(["wcli.py", "plug", "my_func", "--arg0"])
        self.assertArgsValue(task, [True, None])

    def test_parser_boolean(self):
        def my_func(arg0=False, arg1=True):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertArgsValue(task, [False, True])

        task = z.parse(["wcli.py", "plug", "my_func", "--arg0", "--no-arg1"])
        self.assertArgsValue(task, [True, False])

    def test_parse_int(self):
        def my_func(arg0=10):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertArgsValue(task, [10])

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func", "42"])
        self.assertArgsValue(task, [42])

    def test_parse_float(self):
        def my_func(arg0=0.5):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertArgsValue(task, [0.5])

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func", "42.42"])
        self.assertArgsValue(task, [42.42])

    def test_multiple_parameters(self):
        def my_func(
            some_string="blah",
            some_int=42,
            some_float=10.10,
            some_boolean=True,
            another_string="mm",
            some_none=None,
        ):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func"])
        self.assertArgsValue(task, ["blah", 42, 10.10, True, "mm", None])

        self._load_task("plug", my_func)
        task = z.parse(
            [
                "wcli.py",
                "plug",
                "my_func",
                "zz",
                "822",
                "20.20",
                "--no-some_boolean",
                "--another_string",
                "gg",
            ]
        )
        self.assertArgsValue(task, ["zz", 822, 20.20, False, "gg", None])

    def test_settings(self):
        def my_func():
            pass

        self._load_task("plug", my_func)

        z.parse(
            [
                "wcli.py",
                "-s",
                "setting1",
                "value1",
                "-s",
                "setting2",
                "value2",
                "plug",
                "my_func",
            ]
        )
        self.assertEqual(z.settings, {"setting1": "value1", "setting2": "value2"})

    def test_list(self):
        def my_func(arg=[]):
            pass

        self._load_task("plug", my_func)
        task = z.parse(["wcli.py", "plug", "my_func", "a,b,c"])
        self.assertArgsValue(task, [["a", "b", "c"]])


if __name__ == "__main__":
    print(zversion)
    unittest.main()
