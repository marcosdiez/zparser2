#!/usr/bin/env python3

import sys
from zparser.zparser import z, ZExitException, zexit

def _init_parser():
    z.initialize()
    z.set_plugin_module(['plugins',])
    return z


if __name__ == '__main__':
    exit_code = 0
    # try:
    try:
        _init_parser()
        runner = z.parse(prog_name=sys.argv[0])
        # apply_settings(z.settings)
        runner.run()
    except ZExitException as exit_exception:
        exit_code = exit_exception.exit_code
    # finally:  # move that to zparser (part of run)
    sys.exit(exit_code)
