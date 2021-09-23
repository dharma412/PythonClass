#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/bouncerecipients.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import clictorbase as ccb
import status

from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

class bouncerecipients(ccb.IafCliConfiguratorBase):

    class BRNoRecordError(ccb.IafCliError):
        """
        If there is an error when attempting to bouncerecipients,
        this exception class should be raised.
        """
        pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
                ('No record of that host', EXACT) : self.BRNoRecordError
        })

    def __call__(self, how='all', hostname=None,
                       address=None, sure=YES, check_status=False):
        option = {'host':hostname, 'sender':address}.get(how)
        how_choice = {'all':3, 'host':1, 'sender':2}[how]
        if how != 'all': assert option is not None
        deliv_suspend_check = False

        # If you are testing to verify that the user is warned
        # about bouncerecipients being run while delivery is
        # suspended, then pass check_status == True.
        if check_status:
            st = status.status(self._sess)()
            if 'uspended' in st.get_system('system_status'):
                deliv_suspend_check = True

        self._writeln('bouncerecipients')
        self._query_response(how_choice)
        if option:
            self._query_response(option)
        self._query_response(sure)
        return self.process_output(deliv_suspend_check)

    def process_output(self, deliv_suspend_check):
        num_bounced = 0
        resplist = [(r'(\d+) recipients bounced.', REGEX),
                    (r'No messages bounced.', REGEX)]

        # Look for one of these responses
        self._query(timeout=60, *resplist)
        mo = self._get_last_mo()

        if len(mo.groups()) > 0:
            num_bounced = int(mo.group(1))

        # Should there be a message about how deliveries are
        # currently suspended?
        if deliv_suspend_check and num_bounced != 0:
            self._query('currently suspended')

        self._wait_for_prompt()
        return num_bounced

if __name__ == '__main__':
    import suspenddel
    import resume

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    br = bouncerecipients(cli_sess)
    print br(how='all')
    print br(how='sender', address='test@abc.qa')
    try:
        print br(how='host', hostname='qa04.qa')
    except bouncerecipients.BRNoRecordError:
        print 'Received BRNoRecordError, as expected.'
    else:
        raise Exception('BRNoRecordError not received as expected.')

    suspenddel.suspenddel(cli_sess)()
    print br(how='all')
    resume.resume(cli_sess)()
