#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/antivirusupdate.py#1 $

"""
    IAF 2 CLI ctor - antivirusupdate
"""

import clictorbase as ccb


class antivirusupdate(ccb.IafCliConfiguratorBase):
    """
    returns:
            1 - feature is not activated
            2 - for Sophos only
            3 - Anti-Virus not enabled (Sophos and McAfee)
            4 - update process not running
            5 - update in progress
            6 - update suspended
            7 - requesting forced update
            8 - requesting update (Sophos)
            9 - requesting update (McAfee)
    """

    def __call__(self, force=False, vendor='sophos'):

        pats = [
            "Choose the operation",  # 0
            "This feature requires activation with a software key",  # 1
            "Currently only Sophos Anti-Virus is supported",  # 2
            "Anti-Virus scanning not enabled.  Virus definitions",  # 3
            "Virus definition update process not running",  # 4
            "Virus definition update in progress",  # 5
            "Virus definition updates suspended until",  # 6
            "Requesting forced update of virus definitions",  # 7
            "Requesting check for new Sophos Anti-Virus updates",  # 8
            "Requesting update of virus definitions",  # 9
        ]

        if force:
            self._writeln('antivirusupdate force')
            lines = self._wait_for_prompt()
        else:

            vendor = vendor.lower()
            assert vendor in ('sophos', 'mcafee')
            self.clearbuf()
            self._writeln('antivirusupdate')
            self._expect([self._get_prompt(), 'Choose the operation'])
            lines = self.getbuf()

            if self._expectindex == 1:
                # vendor is requested
                self._query_response(vendor)
                # strangeness:  in validator world, sometimes this is needed
                # twice since the ctor inexplicably sends 'antivirusstatus'
                # twice, causing a failure.  Remove this once we figure out
                # why this is happening.
                try:
                    lines = self._wait_for_prompt()
                except ccb.IafUnknownOptionError:
                    lines = self._wait_for_prompt()

        for patt_num in xrange(len(pats)):
            if lines.find(pats[patt_num]) != -1:
                return patt_num


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    avu = antivirusupdate(cli_sess)
    print avu(vendor='McAfee')
    print avu(vendor='Sophos')
    print avu(force=True)
