from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from intohex import _intohex as intohex
from hextoint import _hextoint as hextoint

# +
def _hex_add(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
    result = hextoint(first) + hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


# -
def _hex_sub(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
    result = hextoint(first) - hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


# *
def _hex_mul(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
    result = hextoint(first) * hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


# //
def _hex_floordiv(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
    result = hextoint(first) // hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)


# /
_hex_truediv = _hex_floordiv


# %
def _hex_mod(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
        if (type(first) is not str) or (type(second) is not str):
            raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
        result = hextoint(first) % hextoint(second)
        if hex_output:
            return(intohex(result, hex_output_prefix, hex_output_upper))
        else:
            return(result)


# **
def _hex_power(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if (type(first) is not str) or (type(second) is not str):
        raise TypeError("Values type must be str (are %s). Use intohex(int value)" % [type(first), type(second)])
    result = hextoint(first) ** hextoint(second)
    if hex_output:
        return(intohex(result, hex_output_prefix, hex_output_upper))
    else:
        return(result)
