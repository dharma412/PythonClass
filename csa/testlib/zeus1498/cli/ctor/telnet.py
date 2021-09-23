#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/telnet.py#1 $

"""
    telnet IAF 2 configurator
"""
import clictorbase

from sal.exceptions import ConfigError

class telnet(clictorbase.IafCliConfiguratorBase):
    def __call__(self, interface, hostname, port=None, timeout=30):
        """telnet command, use telnet_validate() to make sure it worksi"""
        self._writeln('telnet')
        self._query_response(interface)
        self._query_response(hostname)
        self._query_response(port)
        self.telnet_validate(hostname, port, timeout)

    def telnet_validate(self, hostname, port, timeout):
        """telnet_validate - validates that a telnet command completed OK
           a ConfigError Exception is raised if the operation failed
           upon successful completion, the telnet session is left open
           and the user is responsible closing the session
        """

        idx = self._query('Connected',
                          'Unable to connect to remote host',
                          'Connection refused',
                          'Invalid arguments when processing telnet:',
                          '%s: hostname nor servname provided, or not known' % hostname,
                          timeout=timeout)
        if idx == 0:
            return

        if idx == 1:
            err = 'Unable to connect to remote host'
        elif idx == 2:
            err = 'Connection refused'
        elif idx == 3:
            err = "Invalid arguments - hostname=%s port=%s" % (hostname,port)
        elif idx == 4:
            err = '%s: No address associated with hostname' % hostname
        else:
            err = 'Unknown'
        self._restart()
        print err
        raise ConfigError, err

    def close(self):
        self._restart()
