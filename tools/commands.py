command_lookup = {}


def command(f):
    command_lookup[f.__name__] = f
    return f
