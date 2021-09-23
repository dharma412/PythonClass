#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/showchanges.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import clictorbase
import re
import string
import time
from sal.exceptions import ConfigError


class showchanges(clictorbase.IafCliConfiguratorBase):
    def __call__(self, smart=0):
        if smart:
            return self._smart_showchanges()
        else:
            return self._showchanges()

    def _read_result(self, cmd, timeout=None):
        self._writeln(cmd)
        rv = self._read_until(timeout=timeout)  # read until prompt
        return rv

    def _smart_showchanges(self):
        """Return the uncommited changes as a dictionary object."""
        data = self._read_result("showchanges")

        a = data.replace(" showchanges", "").replace('\r', '')
        a = a.strip()
        b = eval(a)

        if b:
            c = b['standalone']  # single item dict
            d = c['']  # single item dict
            return d  # return dict

        # nothin changed - the caller expects an empty dict
        return {}

    def _showchanges(self):
        data = self._read_result("showchanges")

        try:
            data = string.replace(data, '\': {\'', '.')
            data = string.replace(data, 'standalone..', '')
            data = string.replace(data, ' {\'', ' \'')
            data = string.replace(data, ': [', ' ,[')
            data = string.replace(data, ']}}', ']')
            data = string.replace(data, '}}}', '')
            data = string.replace(data, '\r', '')
            data = string.replace(data, '\'all\': {-1 ,[', '')
            data = string.replace(data, ']', '')
            # compatible with older scripts
            data = string.replace(data, 'system.alert.mailto_addrs', 'hermes.alert.mailto_addrs')
            _s = data.index('{')
            _e = data.rindex('}') + 1

            return eval(data[_s:_e], {}, {})

        except:
            _s = data.index('{')
            _e = data.rindex('}') + 1
            sanity_check_str = data[_s:_e]
            l_braces = sanity_check_str.count('{')
            r_braces = sanity_check_str.count('}')
            if l_braces != r_braces:
                print "Left Curly Braces=%d, Right Curly Braces=%d" % (l_braces, r_braces)
                raise ConfigError, "Parsing logic error in ironport.showchanges"
            else:
                raise ConfigError, "unable to cast %r into python object" % (data,)


if __name__ == '__main__':
    sc = showchanges(clictorbase.get_sess())

    # uncommitted setgateway
    sc._writeln('setgateway')
    sc._query_response('172.28.14.2')
    sc._wait_for_prompt()

    print 'showchanges with smart set to 1'
    out = sc(smart=1)
    print out

    print 'showchanges with smart set to 0'
    out = sc()
    print out
