from rich.console import Console


_console = None


def get_console(stderr=False):
    """
    Singelton. -> Get the console instance.
    """
    global _console
    if _console:
        return _console
    _console = Console(
        record=True,
        stderr=stderr,
    )
    return _console
