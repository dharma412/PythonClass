#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/traceroute6.py#1 $

import re
import socket
import clictorbase
from sal.deprecated.expect import EXACT

class CantResolveHostError(clictorbase.IafCliError): pass
class NoRouteError(clictorbase.IafCliError): pass

class traceroute6(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('hostname nor servname provided, or not known', EXACT) : CantResolveHostError,
             ('No route to host', EXACT) : NoRouteError,
        })

    def __call__(self, interface='Auto', host=None):
        self._writeln(self.__class__.__name__)
        self._query_select_list_item(interface)
        self._query_response(host)

        raw = self._wait_for_prompt()
        lines = '\n'.join(raw.splitlines()[:-1])

        # attempt to parse and return traceroute data
        return TracerouteData(lines)

class TracerouteData:
    def __init__(self, trace):
        self.output = trace

    def __str__(self):
        return self.output

    def parse(self):
        """ Extract (hop_number, host) tuples from traceroute output.
            Returns a list of the tuples.
        """

        # regexp that matches an individual hop in traceroute output
        # When invoking traceroute on the comparison machine, the header
        # line and timeouts ("*") get interleaved with the stuff we're
        # looking for.  (Note that those lines are terminated by "\r\n".)
        traceroute_hop = re.compile(r"""^(\d+)\s+(\S+)""")

        result = []
        for line in self.output.split('\n'):
            match = traceroute_hop.search(line)
            if match:
                result.append((match.group(1), match.group(2)))
        return result


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    drain_host = socket.gethostname()

    tr = traceroute(cli_sess)

    print 'test with drain host and auto interface'
    print tr(host=drain_host)
    print'traceroute DONE!'

# EOF
