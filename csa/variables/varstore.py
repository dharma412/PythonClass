# $Id: //prod/main/sarf_centos/variables/varstore.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

""" This module allows suites to create dictionary-like objects to persist
beyond the suite run session. This would allow the other suites to pick the
values of the variables stored before.

*Parameters:*

- `store_path`: path to file to persist dictionary. If existing file given
  then it will be loaded otherwise file with empty pickled dictionary will be
  created.
- `varname`: optional argument, default value 'VARSTORE'. Variable name to
  assign varstore to.

*Usage:*

Varstore behaves as regular dict. Therefore in order to manipulate varstore you
may use any keyword from BuiltIn and Collections library.

*Examples:*

`Importing`

In this case variable ${VARSTORE} will be imported storing its data in the file
located at ${FILE_PATH}:

| *** Settings *** |
| Variables | varstore.py | ${FILE_PATH} |

In this case variable ${OTHER_VAR} will be imported storing its data in the
file located at ${OTHER_PATH}

| *** Settings *** |
| Variables | varstore.py | ${OTHER_PATH} | OTHER_VAR |

`Using`

| Set To Dictionary | ${VARSTORE} | KEY1 | VALUE1 |
| Dictionary Should Contain Key | ${VARSTORE} | KEY1 |
| ${value} | Get From Dictionary | ${VARSTORE} | KEY1 |
| Delete From Dictionary | ${VARSTORE} | KEY1 |
"""

import pickle
from os import path


class VarstoreMeta(type):
    """ Using this meta we're able to decorate all methods that are critical to
    state to initiate save or load. If we use __getattribute__ to achieve this
    goal we won't be able to intercept calls to magic methods.
    """

    _write_on = ['__delitem__', '__setitem__', 'clear', 'fromkeys', 'pop',
                 'popitem', 'setdefault', 'update']

    _read_on = ['__cmp__', '__contains__', '__delitem__', '__eq__',
                '__format__', '__ge__', '__getitem__', '__gt__', '__hash__',
                '__iter__', '__le__', '__len__', '__lt__', '__ne__',
                '__repr__', '__setitem__', '__str__', 'clear', 'copy',
                'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys',
                'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update',
                'values', 'viewitems', 'viewkeys', 'viewvalues']

    def __new__(cls, name, bases, dct):
        def write(func):
            def wrapped(self, *args, **kwargs):
                res = func(self, *args, **kwargs)
                self._save()
                return res
            return wrapped
        def read(func):
            def wrapped(self, *args, **kwargs):
                self._load()
                return func(self, *args, **kwargs)
            return wrapped

        for key in cls._write_on:
            # Fetching attributes from first base class is sufficient for
            # achieving the goal
            func = dct.get(key) or bases[0].__dict__.get(key)
            dct[key] = write(func)

        for key in cls._read_on:
            func = dct.get(key) or bases[0].__dict__.get(key)
            dct[key] = read(func)

        return type.__new__(cls, name, bases, dct)


class Varstore(dict):

    __metaclass__ = VarstoreMeta

    def __init__(self, store_path):
        self._store_path = store_path
        self._load()

    def __getstate__(self):
        return super(Varstore, self).copy()

    def __setstate__(self, state):
        super(Varstore, self).clear()
        super(Varstore, self).update(state)

    def _load(self):
        if not path.exists(self._store_path):
            self._save({})
        with open(self._store_path, 'rb') as source:
            self.__setstate__(pickle.load(source))

    def _save(self, data=None):
        if data is None:
            data = self
        with open(self._store_path, 'wb') as destination:
            pickle.dump(data, destination)

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)


opened_varstores = {}

def get_variables(store_path, varname='VARSTORE'):
    global opened_varstores
    if store_path not in opened_varstores:
        opened_varstores[store_path] = Varstore(store_path)
    return {varname: opened_varstores[store_path]}

