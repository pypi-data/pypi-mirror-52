import os
from sys import stdout


class ColorError(Exception):
    pass


class Color:
    names = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']


for color_number, color_name in enumerate(Color.names):
    setattr(Color, color_name, color_number)


class ColorCode:
    prefix = {
        'posix': '\u001b',
        'windows': '^<ESC^>'
    }

    def __init__(self, number=0):
        self.number = number

    @property
    def os_prefix(self):
        try:
            return ColorCode.prefix[os.name]
        except KeyError:
            raise ColorError('Could not determine color code to use for ', os.name)

    @property
    def reset(self):
        return f'{self.os_prefix}[0m'

    @property
    def code(self):
        return f'{self.os_prefix}[3{self.number}m'


def incolor(color: int, *args, sep=' ', only_tty=True) -> str:
    text = sep.join(map(str, args))
    if only_tty and not stdout.isatty():
        return text
    return f'{ColorCode(color).code}{text}{ColorCode().reset}'


def cprint(*args, only_tty=True, end='\n', file=stdout, flush=False):
    print(incolor(*args, only_tty=only_tty), end=end, file=file, flush=flush)
