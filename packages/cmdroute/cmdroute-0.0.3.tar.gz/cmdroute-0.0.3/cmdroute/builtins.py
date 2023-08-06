from .cmdroute import entrypoint
from .storage import entrypoints


@entrypoint()
def help(name=None):
    """
    show this output

    help is a utility tool for giving info about other commands
    """
    longest_name_len = max(
        *[len(i.__name__) for i in entrypoints]
    )
    if name is None:
        for epoint in entrypoints:
            print(
                "{:<{length}}".format(
                    epoint.__name__,
                    length=longest_name_len,
                ),
                end=" : ",
            )
            if epoint.__doc__ is not None:
                print(
                    epoint.__doc__.strip()
                    .split("\n")[0]
                    .strip(),
                    end=" ",
                )
            else:
                print(3 * "_", end="")

            print()
    else:
        for epoint in entrypoints:
            if epoint.__name__ == name:
                print(epoint.__name__)
                print()
                if epoint.__doc__ is not None:
                    doc = epoint.__doc__
                    doc = doc.strip()
                    doc = doc.split("\n")
                    doc = [i.strip() for i in doc]
                    doc = "\n".join(doc)
                    print(doc)
