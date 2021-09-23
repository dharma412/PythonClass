"""
An Ordered Dictionary implementation

DETAIL from ASPN:

Title: Ordered Dictionary
Submitter: David Benjamin (other recipes)
Last Updated: 2002/01/21
Version no: 1.2
Category: Extending

Description: This dictionary class extends UserDict to record the
order in which items are added. Calling keys(), values(), items(),
etc. will return results in this order. Note that __str__ and __repr__
return the items in dictionary order.  This works similarly to the
array type in PHP.  Often it is useful to use a dictionary to store
information where the order of that information matters. In Python,
one must usually keep a list of keys and pass the list along with the
dictionary to any functions that need to maintain this order. This
implementation stores the list of keys internally and overrides the
usual accessor methods to keep the list up to date with each
operation.

Example:

>>> d = odict()
>>> d['a'] = 1
>>> d['b'] = 2
>>> d['c'] = 3
>>> d.items()
[('a', 1), ('b', 2), ('c', 3)]

>>> o = odict()
>>> o['c'] = 1
>>> o['b'] = 2
>>> o['a'] = 3
>>> o.items()
[('c', 1), ('b', 2), ('a', 3)]

popitem() has been fixed in this version to throw the correct exception on an empty dictionary.

Note that all operations on the key list are O(n).

REF: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/107747
"""
from __future__ import absolute_import

#: Reference Symbols: odict

from UserDict import UserDict


class odict(UserDict):
    def __init__(self, dict=None):
        """Initialize dictionary with 'dict'"""
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        """Remove item from dictionary"""
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        """Add or update item in dictionary"""
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        """Empty the contents of the dictionary.
        Return: None
        """
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        """Make a copy of the ordered dictionary and return it.
        """
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        """Return dictionary items in order"""
        return zip(self._keys, self.values())

    def keys(self):
        """Return dictionary keys in order"""
        return self._keys

    def popitem(self):
        """Remove newest item from the dictionary
Return: popped item which is a (key,value) tuple
Raise: KeyError if dictionary is empty
"""
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj=None):
        """setdefault() is like get(), except that if key is missing, failobj is both
        returned and inserted into the dictionary as the value of key."""
        return UserDict.setdefault(self, key, failobj)

    def update(self, dict):
        """Use 'dict' to overwrite the contents of the existing dictionary."""
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        """Return dictionary values in order"""
        return map(self.get, self._keys)
