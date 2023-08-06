from .storage import entrypoints


def entrypoint():
    def decorator(function):
        entrypoints.append(function)

        def gatherer(*args, **kwargs):

            result = function(*args, **kwargs)

            return result

        return gatherer

    return decorator


def dispatch(args=None):
    if args is None:
        import sys

        args = sys.argv
    target = args[1]
    target_args = []
    target_kwargs = {}
    for rawarg in args[2:]:
        if "=" in rawarg:
            kw, arg = rawarg.split("=")
            if "," in arg:
                arg = arg.split(",")
            target_kwargs[kw] = arg
        else:
            if "," in rawarg:
                arg = rawarg.split(",")
            else:
                arg = rawarg
            target_args.append(arg)

    for epoint in entrypoints:
        if not epoint.__name__ == target:
            continue
        epoint(*tuple(target_args), **dict(target_kwargs))
