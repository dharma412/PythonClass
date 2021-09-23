#!/usr/bin/env python
# $Id: isadminclirestricted.py,v 1.0
# $DateTime: 2017/03/15
# $Author: okurochk


import clictorbase


class isadminclirestricted(clictorbase.IafCliConfiguratorBase):
    """
        Utility to check if standard set of cli commands is restricted by running 'version' command.
        Returns 'True' if default password needs to be changed -
        in this case only limited set of commands is available.
    """
    def __call__(self):
        self._writeln('version')
        output = self._sess.read_until()
        result = None

        if "Current Version" in output:
            result = False
        elif "change the default passphrase" in output:
            result = True
        return result



