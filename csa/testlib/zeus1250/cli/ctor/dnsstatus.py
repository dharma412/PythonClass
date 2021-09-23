#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/dnsstatus.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import clictorbase

class dnsstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('dnsstatus')
        # dnsstatus simply prints the DNS status to the
        # terminal, should we parse it intelligently or
        # just pass it back to the test script?
        #
        # XXX: For now just pass the text back
        return self.dns_status_parse(self._read_until())

    def dns_status_parse(self, dnsstatus_str):
        """ dns_status_parse(dnsstatus_str) --> String

        For now all this method does is return the parameter back. One day it
        may pass back some type of DNSStatus object. (Of course, that is not
        to be confused with the name of this class)
        """
        return dnsstatus_str

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    ds = dnsstatus(cli_sess)
    ds_str = ds()
    print "DNS STATUS:\n-------------------------------------------", ds_str
