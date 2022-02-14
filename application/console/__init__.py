from .getter import get_console

console = get_console(stderr=False)
errors = get_console(stderr=True)
