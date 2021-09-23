#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/debugger.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import pdb
import sys

IO = lambda s: (s.stdin, s.stdout)


def rpdb(F):
    """
    Source:
    http://code.activestate.com/recipes/578073-rpdb-robotpythondebugger-a-smarter-way-to-debug-ro/
    http://groups.google.com/group/robotframework-users/browse_frm/month/2012-05?pli=1

    robot python debugger -- usage:
    @rpdb
    def keyword_method(self, arg1, arg2, ...):
        # stuff here ...
        rpdb.set_trace() # set breakpoint as usual
        # more code ...
    """
    setattr(rpdb, 'set_trace', pdb.set_trace)
    builtinIO = IO(sys)

    def _inner(*args, **kwargs):
        robotIO = IO(sys)  # robot has hijacked stdin/stdout
        pdb.sys.stdin, pdb.sys.stdout = builtinIO
        retval = F(*args, **kwargs)
        sys.stdin, sys.stdout = robotIO
        return retval

    return _inner
