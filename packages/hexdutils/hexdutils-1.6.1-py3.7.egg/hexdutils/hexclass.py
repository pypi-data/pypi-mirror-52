from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet

import intohex
import hextoint
import hexabc
import hexops

class hexobj:
    def __init__(self, hex_initializer):
        if isinstance(hex_initializer, str):
            self.hexstr = hex_initializer
            self.int = hextoint._hextoint(hex_initializer)
        elif isinstance(hex_initializer, int):
            self.hexstr = intohex._intohex(hex_initializer)
            self.int = hex_initializer
        else:
            TypeError("Argument type must be <str> or <int> (is %s)" % type(hex_initializer))

    def __str__(self):
        return self.hexstr

# + add
    def __add__(self, other):
        if isinstance(other, hexobj):
            return hexops._hex_add(self.hexstr, other.hexstr, hex_output=True)
        elif isinstance(other, int):
            return hexops._hex_add(self.hexstr, intohex._intohex(other), hex_output=True)
    def __radd__(self, other):
        return self.__add__(other)

# - sub
    def __sub__(self, other):
        if isinstance(other, hexobj):
            return hexops._hex_sub(self.hexstr, other.hexstr, hex_output=True)
        elif isinstance(other, int):
            return hexops._hex_sub(self.hexstr, intohex._intohex(other), hex_output=True)
    def __rsub__(self, other):
        return self.__sub__(other)

# * mult
    def __mul__(self, other):
        if isinstance(other, hexobj):
            return hexops._hex_mul(self.hexstr, other.hexstr, hex_output=True)
        elif isinstance(other, int):
            return hexops._hex_mul(self.hexstr, intohex._intohex(other), hex_output=True)
    def __rmul__(self, other):
        return self.__mul__(other)


# //
    def __floordiv__(self, other):
        if isinstance(other, hexobj):
            return hexops._hex_floordiv(self.hexstr, other.hexstr, hex_output=True)
        elif isinstance(other, int):
            return hexops._hex_floordiv(self.hexstr, intohex._intohex(other), hex_output=True)
    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

# /
    __truediv__ = __floordiv__


# % mod
    def __mod__(self, other):
        if isinstance(other, hexobj):
            return hexops._hex_mod(self.hexstr, other.hexstr, hex_output=True)
        elif isinstance(other, int):
            return hexops._hex_mod(self.hexstr, intohex._intohex(other), hex_output=True)
    def __rmod__(self, other):
        return self.__mod__(other)

# <
    def __lt__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) < (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __rlt__(self, other):
        return self.__lt__(other)


# >
    def __gt__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) > (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __rgt__(self, other):
        return self.__gt__(other)


# <=
    def __le__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) <= (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __rle__(self, other):
        return self.__le__(other)


# >=
    def __ge__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) >= (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __rge__(self, other):
        return self.__ge__(other)


# ==
    def __eq__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) == (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __req__(self, other):
        return self.__eq__(other)


# !=
    def __ne__(self, other):
        if isinstance(other, hexobj) or isinstance(other, int):
            return hextoint._hextoint(self.hexstr) != (hextoint._hextoint(other.hexstr) if isinstance(other, hexobj) else other)
    def __rne__(self, other):
        return self.__ne__(other)

# -
    def __neg__(self):
        if isinstance(other, hexobj):
            return "-"+self.hexstr

# ~
    def __invert__(self):
        if isinstance(other, hexobj):
            return ~ hextoint._hextoint(self)
