# incolor
## Description
Very simple package that aims at adding some color to Your life.

## Quickstart
- Add color codes to text (uses color numbers)
``` python
>>> from incolor import incolor
>>> incolor(4, 'I\'m blue da ba dee')
"\x1b[34mI'm blue da ba dee\x1b[0m"
```

- Add color codes to text (uses color names)
``` python
>>> from incolor import incolor, Color
>>> incolor(Color.blue, 'I\'m blue da ba dee')
"\x1b[34mI'm blue da ba dee\x1b[0m"
```

- Join multiple arguments in colorful manner
``` python
>>> incolor(Color.brwhite, 'First', 2, 'third', list())
'\x1b[315mFirst 2 third []\x1b[0m'
```

- Color print function (behaves exactly like `print(incolor(...))` ) (__the is yellow here__)
``` python
>>> cprint(3, 'Yellow: 🚢', 123, 'yay')
Yellow: 🚢 123 yay
```

- Both functions accept `sep` argument
```python
>>> incolor(0, 'a', 1, 2, sep='\t')
'\x1b[30ma\t1\t2\x1b[0m'
>>> cprint(0, 'a', 1, 2, sep='\t')
a       1       2
```

## Tests

To run tests execute `test.sh` script
``` sh
./test.sh
```

Prerequisites:
- docker
- Internet connection 😃

## #TODO
- [x] add colors only if output is a TTY
- [ ] verify Windows support (probably not working?)
- [ ] add more ways to specify colors (f.e. from string: `'red'`)
- [ ] add support for `256 colors`
- [ ] add support for `Truecolor`
