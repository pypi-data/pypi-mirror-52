from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

from __hex_constants__ import __hex_letters, __alphabet


def _hextoint(target):
    if type(target) is not str:
        raise TypeError("Argument must be str (is %s)" % type(target))
    decimals = []
    isneg_mult = None
    if target[0] == "-":
        isneg_mult = -1
        target = target[1:]
    else:
        isneg_mult = 1
    if target[:2] is "0x":
        target = target[2:]
    power_of_sixteen = len(target)-1
    for item in target:
        try:
            decimals.append(int(item)*(16**power_of_sixteen))
            power_of_sixteen -= 1
        except:
            # if item is a letter
            if item.lower() in __hex_letters:
                decimals.append(__hex_letters[item.lower()]*(16**power_of_sixteen))
                # Letter correspondant value * 16**location in list (= n_th figure)
            else:
                # not a,b,c,d,e,f
                raise ValueError(item, "doesn't belong to hex system")
    else:
        return(sum(decimals) * isneg_mult)
