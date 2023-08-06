from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet


def _intohex(number, hex_prefix=False, uppercase=False):
    if type(number) is not int:
        raise TypeError("Value to convert must be int (is %s)" % type(number))
    isneg = None
    if number < 0:
        number = -number
        isneg = True

    def hexdivide(target):
        if target % 16 > 9:
            for item in __hex_letters:
                if __hex_letters[item] == (target % 16):
                    if uppercase:
                        return(item.upper())
                    else:
                        return(item)
            return(target % 16)
        return(target % 16)

    values = []
    while (number//16) is not 0:
        values.insert(0, hexdivide(number))
        number = number//16
    values.insert(0, hexdivide(number))
    if hex_prefix:
        return(("-" if isneg else '') + "0x" + ("".join(str(item) for item in values)))
    else:
        return(("-" if isneg else '') + "".join(str(item) for item in values))
