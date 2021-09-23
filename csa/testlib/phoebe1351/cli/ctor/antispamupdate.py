#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/antispamupdate.py#1 $

"""
    IAF 2 CLI ctor - antispamupdate
"""


import clictorbase as ccb
from sal.deprecated.expect import EXACT,REGEX

class antispamupdate(ccb.IafCliConfiguratorBase):
    """
    returns:
            1 - feature is not activated
            2 - can not do Brightmail
            3 - CASE restarting
            4 - either CASE or VOF must be enabled
            5 - update process not running
            6 - update in progress
            7 - update suspended
            8 - requesting forced update
            9 - requesting update
    """
    def __call__(self, vendor='ironport', force=False):
        """
           vendor - multiscan, ironport, cloudmark
        """
        if force:
            self._sess.writeln('antispamupdate %s force'%vendor)
        else:
            self._sess.writeln('antispamupdate')
            self._query_response(vendor)

        pats = [
            ("This feature requires activation with a software key", EXACT), #1
            ("Currently only IronPort Services are supported", EXACT),       #2
            ("CASE is restarting and cannot perform an update right", EXACT),#3
            ("Either IronPort Anti-Spam or Intelligent Multi-Scan or Virus Outbreak Filters", REGEX),  #4
            ("Spam update process not running", EXACT),                      #5
            ("CASE rules update in progress", EXACT),                        #6
            ("CASE definition updates suspended until", EXACT),              #7
            ("Forcing updates for", REGEX),			             #8
            ("Requesting updates for",REGEX),		          	     #9
            ("scanning is not enabled.",REGEX),        #10
        ]
        # Changed timeout to 15 because of non-error timeout issues
        self._expect(pats, timeout=15)
        self._wait_for_prompt()
        return self._sess.expectindex + 1

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    asu = antispamupdate(cli_sess)
    print asu(vendor='ironport',force=False)
    print asu(vendor='cloudmark',force=True)


