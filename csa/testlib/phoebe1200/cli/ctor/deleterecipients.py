#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/deleterecipients.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT, REGEX


class DeleteRecipientsError(clictorbase.IafCliError):
    """
    If there is an error when attempting to deleterecipients,
    this exception class should be raised. deleterecipients however
    does not use the new error checking (_set_local_err_dict) because
    it's faster to copy old code over.
    """
    pass


class deleterecipients(clictorbase.IafCliConfiguratorBase):

    def __call__(self, how='all', host=None, sender=None, sure=YES):
        if how.lower() == 'host':
            assert host
        elif how.lower() == 'sender':
            assert sender
            how = 'address'
        elif how.lower() == 'all':
            how = 'All'
        ans = host or sender

        self._writeln('deleterecipients')
        # Delete by host, sender, or All?
        self._query_select_list_item(how)
        # If not all, what do we delete?
        if how != 'All':
            self._query_response(ans)
        # are we are sure?
        self._query_response(sure)
        return self.process_output()

    def process_output(self):

        resplist = [('Failed to delete', EXACT),
                    ('The server is not responding.', EXACT),
                    ('Operation failed! (.*)', REGEX),
                    (r'(\d+) messages deleted.', REGEX),
                    (r'(\d+) recipients deleted.', REGEX),
                    ('No record of that host.', EXACT),
                    ('No recipients deleted.', EXACT),
                    ('No messages deleted.', EXACT)]
        # Look for one of these responses
        # this operation might take a while
        ei = self._query(timeout=300.0, *resplist)
        mo = self._get_last_mo()

        # Do we need the restart here?
        self._restart()
        if ei in (0, 1):
            raise DeleteRecipientsError, resplist[ei]
        elif ei == 2:
            raise DeleteRecipientsError, mo.group(1)
        elif ei in (3, 4):
            return int(mo.group(1))
        elif ei in (5, 6, 7):
            return 0


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    dr = deleterecipients(cli_sess)
    print dr(), 'should be 0'
    print dr(how='host', host='neverinthere.qa'), 'should be 0'
    print dr(how='sender', sender='blah@neverinthere.qa'), 'should be 0'
