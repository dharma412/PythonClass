""" A modified Python list, where empty elements are cfgholder instances.
"""
from __future__ import absolute_import

#: Reference Symbols: datastructures

from sal.containers import cfgholder


class ScalarList(list):
    """This is a modified Python List.  It lets you do this:
            s_list = ScalarList(mga1, mga2, mga3)
            s_list.mga1_attr      # same as s_list[0].mga1_attr
            s_list.mga1_attr  = 1 # same as s_list[0].mga1_attr = 1

        ScalarList also grows dynamically. Accessing elements that
        do not exist results in empty cfgholder.CfgHolder objects appended to
        the ScalarList object.
    """

    def __getattr__(self, name):
        """self.attr becomes self[0].attr"""
        return getattr(self[0], name)

    def __setattr__(self, name, value):
        """self.attr = value becomes self[0].attr = value"""
        setattr(self[0], name, value)

    def __delattr__(self, name):
        """del self.attr becomes del self[0].attr"""
        delattr(self[0], name)

    def __getitem__(self, key):
        """self[n].attr causes element n to be created dynamically"""
        assert isinstance(key, int) and key >= 0
        if key >= len(self):
            self._expand_list(key)
        return super(ScalarList, self).__getitem__(key)

    def __setitem__(self, key, value):
        """self[n].attr = value causes element n to be created dynamically"""
        assert isinstance(key, int) and key >= 0
        if key >= len(self):
            self._expand_list(key)
        return super(ScalarList, self).__setitem__(key, value)

    def _expand_list(self, key):
        """expand list to be 'key' size."""
        expand_qty = key - len(self) + 1
        for i in xrange(expand_qty):
            ch = cfgholder.CfgHolder()
            self.append(ch)
