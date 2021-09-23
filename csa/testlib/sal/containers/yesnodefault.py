from __future__ import absolute_import


#: Reference Symbols: yesnodefault

class YesNoDefault(int):
    __slots__ = ()

    def __str__(self):
        if self == 2:
            return 'D'
        if self == 1:
            return 'Y'
        if self == 0:
            return 'N'
        else:
            return int.__str__(self)

    def __getstate__(self):
        return tuple([getattr(self, attr) for attr in self.__slots__])


def is_yes(yes_or_other):
    s = str(yes_or_other).lower()
    if s == 'y' or s == 'yes':
        return True
    else:
        return False


def is_no(no_or_other):
    s = str(no_or_other).lower()
    if s == 'n' or s == 'no':
        return True
    else:
        return False


def is_default(default_or_other):
    s = str(default_or_other).lower()
    if s == '' or s == 'd' or s == 'default':
        return True
    else:
        return False


def is_yes_or_no(yes_no_or_other):
    return bool(is_yes(yes_no_or_other) or is_no(yes_no_or_other))


YES = YesNoDefault(1)
NO = YesNoDefault(0)
DEFAULT = YesNoDefault(2)
