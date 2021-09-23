#!/usr/bin/env python
"""CfhHolder is a modified dict, with uses list lookup syntax instead
of dict lookup syntax.
"""
#: Reference Symbols: cfgholder

from __future__ import absolute_import

import os
import pprint
import sys
import types


def _pprint_type(obj):
    """Misnamed: returns type dict for CfgHolder objects, or the
    actual type of any other object.
    """
    if isinstance(obj, CfgHolder):
        return type(dict())
    else:
        return type(obj)


def create_cfg(cfg_file):
    # TODO: expand_user
    assert os.path.exists(cfg_file), \
        "'%s' does not exist to be imported" \
        "" % cfg_file

    return CfgHolder(cfg_file)


class CfgHolder(dict):
    """ CfgHolder was created to make dictionaries easier to use to store
        configuration data by removing the syntax of dictionary lookups.
        All __*attr__ functions now call their __*item__ counterparts.

        dictobj['foo'] now becomes dictobj.foo

        We also override pprint._type() to recognize CfgHolder objects as
        dictionaries and to print them as such. In some later version of
        python, we want to allow dir(dictobj) to return a list of dictionary
        keys. (it does not currently)

        >>> ch = CfgHolder()
        >>> ch.foo
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        >>> ch
        {}
        >>> ch.foo = 'test'
        >>> ch
        {'foo': 'test'}
        >>> ch.foo
        'test'
        >>> ch['foo']
        'test'
    """

    def __init__(self, init=None):
        if isinstance(init, dict) or init is None:
            dict.__init__(self, init or {})
        else:
            self._import(init)

    def _import(self, import_file):
        execfile(import_file, {}, self)
        self._delete_modules()

    def _delete_modules(self):
        """Do cleanup. Delete module objects
        from 'self' (a namespace dictionary.)"""
        for k in self.keys():
            if isinstance(self[k], types.ModuleType):
                del self[k]

    def __getitem__(self, name):
        return dict.__getitem__(self, name)

    def __contains__(self, k):
        """ If k is hashable: D.__contains__(k) -> True
            if D has a key k, else False
            If k is a dictionary: D.__contains__(k) --> True
            if D.items() is a superset of k.items(), else False
            If k is a list: D.__contains__(k) --> True
            if D.keys() is a superset of k, else False
        """
        try:
            hash(k)
            return dict.__contains__(self, k)
        except TypeError, te:
            if isinstance(k, list):
                return self._list_contains(k)
            elif isinstance(k, dict):
                return self._dict_contains(k)
            # Other non-hashable objects (if any?) are not supported
            raise te

    def __copy__(self):
        """ CfgHolders are dicts of various structures - we need
            to recursively copy their elements to guarantee we
            get copies of the elements instead of references.
        """

        from copy import copy
        newcfg = CfgHolder()
        for key in self.keys():
            newcfg[key] = copy(self[key])

        return newcfg

    def _dict_contains(self, d):
        # Could use sets, but hashing dictionaries can't be done
        for k in d:
            if not self.has_key(k) or \
                    self[k] != d[k]:
                return False

        # All key-value pairs in d are in this dictionary
        return True

    def _list_contains(self, l):
        # Could use sets, but hashing dictionaries can't be done
        for k in l:
            # Lists can have unhashable items, and dicts can't, so
            # a list with an unhashable item cannot be contained by
            # a dictionary.
            try:
                if not self.has_key(k):
                    return False
            except TypeError:
                return False

        # All list items are a key in this dictionary
        return True

    def pprint(self, stream=None):
        """Pretty Print CfgHolder.
        Replace pprint._type() with our own _pprint_type()
        to coerce CfgHolder objects to be treated like dictionary types.

        stream defaults to sys.stdout when it's None"""
        old_type = pprint._type
        pprint._type = _pprint_type
        pprint.pprint(self, stream)
        # restore original _type()
        pprint._type = old_type

    __getattr__ = __getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class RecursiveCfgHolder(CfgHolder):
    """ RecursiveCfgHolder modifies __getitem__ to create a new
        RecursiveCfgHolder if you access a key that is does not
        currently exist.

        >>> ch = RecursiveCfgHolder()
        >>> ch.newch   #Accessing a key that does not exist.
        {}
        >>> type(ch.newch)
        <class 'sal.containers.cfgholder.RecursiveCfgHolder'>
        >>> print ch.newch
        {}
    """

    def __init__(self, init=None):
        CfgHolder.__init__(self, init or {})

    def __getitem__(self, name):
        if not self.has_key(name):
            if name in sys.modules['__builtin__'].__dict__.keys():
                # TBD: In Python 2.4 we need to raise this
                # exception when name is globals.  Not sure why.
                raise KeyError
            self.__setitem__(name, RecursiveCfgHolder())
        return dict.__getitem__(self, name)

    __getattr__ = __getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class LockingCfgHolder(RecursiveCfgHolder):
    """Allows locking a CfgHolder object.
    Once locked dynamic creation of new CfgHolder attributes results
    in a KeyError exception.  Existing attributes can still be modified
    """

    def __init__(self, init=None):
        RecursiveCfgHolder.__init__(self, init or {})
        dict.__setitem__(self, '_lock', False)

    def __getitem__(self, name):
        if (not self.has_key(name)) and (not self._lock):
            if not self.has_key(name):
                if name in sys.modules['__builtin__'].__dict__.keys():
                    # TBD: In Python 2.4 we need to raise this
                    # exception when name is globals.  Not sure why.
                    raise KeyError
                # create locking recursive CfgHolder
                self.__setitem__(name, LockingCfgHolder())
        return dict.__getitem__(self, name)

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    __getattr__ = __getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class RecursiveDefaultKeyCfgHolder(CfgHolder):
    """ RecursiveDefaultKeyCfgHolder is similar to the RecursiveCfgHolder
    with one small change. In addition to the getattr, the getitem
    method is also overriden. The recursive behavior is retained
    when the attributes are accessed using the '.' way. But when the
    attributes are indexed in the conventional dict lookup manner (using []),
    this class returns the value of a designated default key, in case of missing
    keys. This defaultkey is either set while creating an instance or is equal
    to 'ANY' if nothing is specified.


	>>> ch = cfgholder.RecursiveDefaultKeyCfgHolder()
	>>> ch.newch # create a non-existant key recursively
	{'defaultkey': 'ANY'}
	>>> type(ch.newch)
	<class 'cfgholder.RecursiveDefaultKeyCfgHolder'>
	>>> ch
	{'newch': {'defaultkey': 'ANY'}, 'defaultkey': 'ANY'}
	>>> ch.ANY = "U got default"
	>>> ch['nokey'] # Access a non-existent key to get the default value in return
	'U got default'
    """

    def __init__(self, init=None, defaultkey='ANY'):
        CfgHolder.__init__(self, init or {})
        self.defaultkey = defaultkey

    def __getitem__(self, name):
        if not self.has_key(name):
            if name in sys.modules['__builtin__'].__dict__.keys():
                # TBD: In Python 2.4 we need to raise this
                # exception when name is globals.  Not sure why.
                raise KeyError
            return dict.__getitem__(self, self.defaultkey)
        return dict.__getitem__(self, name)

    def __getattr__(self, name):
        if not self.has_key(name):
            if name in sys.modules['__builtin__'].__dict__.keys():
                # TBD: In Python 2.4 we need to raise this
                # exception when name is globals.  Not sure why.
                raise KeyError
            self.__setitem__(name, RecursiveDefaultKeyCfgHolder(defaultkey=self.defaultkey))
        return dict.__getitem__(self, name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
