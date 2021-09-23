#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/nslookup.py#1 $

"""
IAF 2 CLI command: nslookup
"""
import clictorbase

from sal.exceptions import ConfigError

class nslookup(clictorbase.IafCliConfiguratorBase):

    def __call__(self, hostname='localhost', qtype=None):
        args = hostname
        if qtype is not None:
            args += ' ' + qtype
        self._sess.writeln('nslookup %s' % args)

        self._sess.readlines(2)          # skip the response
        msg = self._sess.read_until()    # read until prompt

        # check for invalid command

        if msg[:7] == 'Invalid':
            raise ConfigError, 'Invalid arguments for nslookup %s' % args
        if msg[:21] == 'Temporary query error':
            raise ConfigError, 'Temporary query error for nslookup %s' % args

        return msg

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    nsl = nslookup(cli_sess)
    resp = nsl(hostname='ironport.com', qtype='MX')
    print resp

