#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/traceroute.py#1 $

import re
import socket
import clictorbase

class traceroute(clictorbase.IafCliConfiguratorBase):
    def __call__(self, interface='Auto', host=None):
        self._writeln('traceroute')
        self._query_select_list_item(interface)
        self._query_response(host)

        raw = self._read_until()
        # attempt to parse and return traceroute data
        return TracerouteData(raw)

class TracerouteData:
    def __init__(self, trace):
        self.output = trace

    def __str__(self):
        return self.output

    def parse(self):
        """ Extract (hostname, IP) tuples from traceroute output.
            Returns a list of the tuples.
        """

        # regexp that matches an individual hop in traceroute output
        # When invoking traceroute on the comparison machine, the header
        # line and timeouts ("*") get interleaved with the stuff we're
        # looking for.  (Note that those lines are terminated by "\r\n".)
        traceroute_hop = re.compile(r"""\d+[\s*]+(\S+) \(([0-9.]+)\)""")

        result = []
        for line in self.output.split('\n'):
            match = traceroute_hop.search(line)
            if match:
                result.append((match.group(1).lower(), match.group(2)))
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
