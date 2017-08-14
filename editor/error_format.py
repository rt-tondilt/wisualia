from sys import exc_info
from traceback import *
def get_error() -> str:
    ty, val, tb = exc_info()

    text = 'Facebook (most recent call lost):\n'
    text += ''.join(format_list(extract_tb(tb)[1: ])) #type: ignore
    text += '\n'
    text += ''.join(format_exception_only(ty, val)) #type: ignore
    return text
