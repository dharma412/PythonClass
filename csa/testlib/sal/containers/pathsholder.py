#!/usr/local/bin/python
"""Dict like object for holding paths."""
from __future__ import absolute_import

#: Reference Symbols: pathsholder

import os.path


class PathsHolder(dict):
    def __init__(self, base, files=None):
        """
        >>> p = PathsHolder('/home/testuser', files={'one': 'aaa', 'two':'bbb'})
        >>> p
        {'one': '/home/testuser/aaa', '_base': '/home/testuser', 'two': '/home/testuser/bbb'}
        """
        self._base = base
        files = files or {}
        for k, v in files.items():
            self[k] = v

    def __setitem__(self, k, v):
        if k != '_base' and not v.startswith(self._base):
            v = os.path.join(self._base, v)

        # Have to use superclass __setitem__ to avoid
        # infinite recursion
        dict.__setitem__(self, k, v)

    # That is strange but python 2.3.4 needs this method defined
    def __getitem__(self, name):
        return dict.__getitem__(self, name)

    __setattr__ = __setitem__
    __getattr__ = __getitem__
    __delattr__ = dict.__delitem__

    def __str__(self):
        "Return just the base of the PathsHolder."
        return self._base
