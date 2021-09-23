#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/testauthconfig.py#1 $

import clictorbase as ccb

class testauthconfig(ccb.IafCliConfiguratorBase):

    def __call__(self, realm_name):
        """ Test auth settings for a realm 

        :Parameters:   
         - `realm_name` : name of a configured authentication realm.

        """

        self.clearbuf()
        self._writeln('testauthconfig')
        self._query_select_list_item(realm_name, timeout=10)
        self._read_until('What realm do you want to test')

        # In CLI, execution of 'testauthconfig' keeps looping until
        # user enter 'Ctrl-C' to quit.  I am not sure how to handle 
        # it here.  So, I decided to make it a single pass through
        # and then quit.  Will update later on to behave like in CLI
        # if needed
        self.interrupt()
        self._wait_for_prompt()
        return self.getbuf()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    ta = testauthconfig(cli_sess)

    # assuming 'myLdapRealm' auth realm is already configured on WSA
    print ta('myLdapRealm')
