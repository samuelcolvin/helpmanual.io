#!/usr/bin/env python3
import sys

from tools.commands import command_lookup
from tools.db import db_main

import tools.legacy  # noqa
from tools.collect_man import collect_man  # noqa


if __name__ == '__main__':
    command_name = sys.argv[1] if len(sys.argv) > 1 else 'missing'
    try:
        coro = command_lookup[command_name]
    except KeyError:
        print(f'command "{command_name}" not found in commands:\n  {", ".join(sorted(command_lookup.keys()))}')
        sys.exit(1)

    db_main(coro)
